#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate registry/entries/*.yaml against registry/entry.schema.json, and
mechanically grade every declared example record.

Ported from scitt-payload-binding's CPB registry filing tooling
(PR #77, branch head e136bf8 -- HELD, unmerged, pending Steven+Anton
ratification as of this port; see PROVENANCE.md). Three differences from
that source, per Steven's 2026-09-05 ruling:

  1. An entry's examples are EXAMPLE RECORDS graded by the reference
     verifier (`agent_action_capsule.verify`), not CPB-style digest
     fixtures run through check_vectors.py.
  2. Promotion is Steven's (or the spec-tier gate's) per-entry ruling, not a
     >=2-organization Designated Expert panel.
  3. No IANA-forwarding clause; not applicable to this script.

Two independent things are checked per entry file:

  1. Schema shape -- the entry itself validates against
     registry/entry.schema.json.

  2. Example grading -- for every example under the entry's `examples_dir`
     (positive.json, boundary.json, must-fail.json, each shaped
     {kind, expected: {record_schema_valid, verify_ok, notes}, record}):

       a. The subject block at `record_schema.record_path` (a key path into
          `record`; empty path means `record` IS the subject) is validated
          against the entry's own declared `record_schema.path`. The ACTUAL
          pass/fail is compared to `expected.record_schema_valid`.
       b. The full `record` is run through `agent_action_capsule.verify`.
          The ACTUAL `ok` value is compared to `expected.verify_ok`.

     A mismatch in either direction is a HARD FAILURE -- including a
     must_fail example whose declared expectation of failure does NOT
     materialize (the Home-2 analog of CPB check_vectors.py's "a MUST-FAIL
     vector that passes is rejected, never silently accepted").

This script does not evaluate whether an entry SHOULD promote past
provisional -- that is Steven's (or the spec-tier gate's) per-entry ruling,
REGISTRATION-POLICY.md, never a mechanical check.

Usage:
    python3 .github/validate_registry_entries.py [ENTRIES_DIR]
Exit 0 = every entry validates and every example grades as declared;
1 = at least one entry failed; 2 = misconfiguration (missing schema, no
PyYAML/jsonschema/agent-action-capsule, etc).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in a misconfigured env
    print("error: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

try:
    import jsonschema
except ImportError:  # pragma: no cover
    print("error: jsonschema is required (pip install jsonschema)", file=sys.stderr)
    sys.exit(2)

try:
    from agent_action_capsule import verify as verify_capsule
except ImportError:  # pragma: no cover
    print(
        "error: agent-action-capsule is required "
        "(pip install \"agent-action-capsule @ git+https://github.com/action-state-group/"
        "agent-action-capsule.git@<pinned-sha>#subdirectory=python\")",
        file=sys.stderr,
    )
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "registry" / "entry.schema.json"
DEFAULT_ENTRIES_DIR = REPO_ROOT / "registry" / "entries"
TEMPLATE_NAME = "TEMPLATE.yaml"
REQUIRED_EXAMPLE_KINDS = ("positive", "boundary", "must-fail")


class EntryError(Exception):
    """A single entry file failed validation; message is human-readable."""


def load_schema(path: Path) -> dict:
    if not path.is_file():
        print(f"error: schema not found at {path}", file=sys.stderr)
        sys.exit(2)
    return json.loads(path.read_text(encoding="utf-8"))


def iter_entry_files(entries_dir: Path) -> list[Path]:
    return sorted(p for p in entries_dir.glob("*.yaml") if p.name != TEMPLATE_NAME)


def validate_against_schema(instance: object, schema: dict) -> list[str]:
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    msgs = []
    for e in errors:
        where = "/".join(str(p) for p in e.path) or "<root>"
        msgs.append(f"{where}: {e.message}")
    return msgs


def _extract_record_path(record: Any, record_path: list[str], example_name: str) -> Any:
    node = record
    for key in record_path:
        if not isinstance(node, dict) or key not in node:
            raise EntryError(
                f"{example_name}: record_path {record_path!r} does not resolve "
                f"inside `record` -- missing key {key!r}"
            )
        node = node[key]
    return node


def validate_example(
    example_path: Path,
    record_schema: dict,
    record_path: list[str],
) -> None:
    try:
        example = json.loads(example_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise EntryError(f"{example_path.name}: invalid JSON: {exc}") from exc

    for key in ("kind", "expected", "record"):
        if key not in example:
            raise EntryError(f"{example_path.name}: missing required key {key!r}")

    expected = example["expected"]
    for key in ("record_schema_valid", "verify_ok"):
        if key not in expected:
            raise EntryError(f"{example_path.name}: expected.{key} is required")

    subject = _extract_record_path(example["record"], record_path, example_path.name)
    schema_errors = validate_against_schema(subject, record_schema)
    actual_schema_valid = not schema_errors
    if actual_schema_valid != expected["record_schema_valid"]:
        raise EntryError(
            f"{example_path.name}: record_schema_valid mismatch -- declared "
            f"{expected['record_schema_valid']}, actual {actual_schema_valid} "
            f"(schema errors: {schema_errors})"
        )

    result = verify_capsule(example["record"])
    if result.ok != expected["verify_ok"]:
        findings = [f"[{f.severity}] {f.code}: {f.detail}" for f in result.findings]
        raise EntryError(
            f"{example_path.name}: verify_ok mismatch -- declared "
            f"{expected['verify_ok']}, actual {result.ok} (findings: {findings})"
        )


def validate_examples_dir(entry: dict, entry_path: Path) -> None:
    examples_dir = REPO_ROOT / entry["examples_dir"]
    if not examples_dir.is_dir():
        raise EntryError(
            f"{entry_path.name}: examples_dir {entry['examples_dir']!r} does not exist"
        )

    record_schema_path = REPO_ROOT / entry["record_schema"]["path"]
    if not record_schema_path.is_file():
        raise EntryError(
            f"{entry_path.name}: record_schema.path {entry['record_schema']['path']!r} "
            f"does not exist"
        )
    record_schema = load_schema(record_schema_path)
    record_path = entry["record_schema"]["record_path"]

    missing = [
        kind for kind in REQUIRED_EXAMPLE_KINDS
        if not (examples_dir / f"{kind}.json").is_file()
    ]
    if missing:
        raise EntryError(
            f"{entry_path.name}: examples_dir is missing required case(s) "
            f"{missing} (need positive.json, boundary.json, must-fail.json)"
        )

    for kind in REQUIRED_EXAMPLE_KINDS:
        validate_example(examples_dir / f"{kind}.json", record_schema, record_path)


def validate_entry_file(path: Path, schema: dict) -> None:
    try:
        entry = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise EntryError(f"{path.name}: invalid YAML: {exc}") from exc

    if not isinstance(entry, dict):
        raise EntryError(f"{path.name}: top-level document must be a mapping")

    errors = validate_against_schema(entry, schema)
    if errors:
        raise EntryError("\n".join(f"{path.name}: {e}" for e in errors))

    validate_examples_dir(entry, path)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    entries_dir = Path(argv[0]) if argv else DEFAULT_ENTRIES_DIR

    if not entries_dir.is_dir():
        print(f"error: {entries_dir} is not a directory", file=sys.stderr)
        return 2

    schema = load_schema(SCHEMA_PATH)
    entry_files = iter_entry_files(entries_dir)
    if not entry_files:
        print(f"no *.yaml entry files under {entries_dir} (TEMPLATE.yaml excluded)")
        return 0

    problems: list[str] = []
    for path in entry_files:
        try:
            validate_entry_file(path, schema)
        except EntryError as exc:
            problems.append(str(exc))
            continue
        entry = yaml.safe_load(path.read_text(encoding="utf-8"))
        print(f"OK   {path.name}  ({entry['kind']} / {entry['status']})")

    if problems:
        print("\nFAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print(f"\n{len(entry_files)} registry entry file(s) validated clean.")
    print(
        "Mechanical checks only -- whether an entry SHOULD promote past "
        "provisional is Steven's (or the spec-tier gate's) per-entry ruling "
        "(REGISTRATION-POLICY.md), never checked here."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
