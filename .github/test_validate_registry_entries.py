# SPDX-License-Identifier: Apache-2.0
"""Mutation-style tests for validate_registry_entries.py: every hard-failure
path must actually fire on the mutant it exists to catch, run against a
throwaway copy of the repo's real entries/examples/schemas -- never against
the committed fixtures in place (a prior mistake while authoring this
script: mutating a committed must-fail.json in place and forgetting to
restore it from the generator would have silently shipped a broken fixture).
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_registry_entries as vre  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
REAL_ENTRIES_DIR = REPO_ROOT / "registry" / "entries"


@pytest.fixture
def schema():
    return vre.load_schema(vre.SCHEMA_PATH)


def test_real_entries_validate_clean(schema):
    """Sanity check: the actual committed entries must pass before any
    mutant test below is meaningful."""
    for path in vre.iter_entry_files(REAL_ENTRIES_DIR):
        vre.validate_entry_file(path, schema)  # raises EntryError on failure


def test_entry_missing_required_field_rejected(schema):
    entry = yaml_load(REAL_ENTRIES_DIR / "mesh-join-card.yaml")
    del entry["owner"]
    errors = vre.validate_against_schema(entry, schema)
    assert any("owner" in e for e in errors)


def test_entry_bad_kind_enum_rejected(schema):
    entry = yaml_load(REAL_ENTRIES_DIR / "mesh-join-card.yaml")
    entry["kind"] = "not-a-real-kind"
    errors = vre.validate_against_schema(entry, schema)
    assert errors


def test_promoted_without_promoted_by_rejected(schema):
    entry = yaml_load(REAL_ENTRIES_DIR / "mesh-join-card.yaml")
    entry["status"] = "promoted"
    errors = vre.validate_against_schema(entry, schema)
    assert any("promoted_by" in e for e in errors)


def test_must_fail_example_declared_valid_is_rejected(tmp_path):
    """The core MUST-FAIL discipline: an example that actually fails schema
    validation but is DECLARED as passing must be a hard failure, not a
    silent pass-through."""
    examples_dir, record_schema, record_path = _copy_entry_fixtures(
        tmp_path, "mesh-join-card"
    )
    must_fail_path = examples_dir / "must-fail.json"
    data = json.loads(must_fail_path.read_text())
    data["expected"]["record_schema_valid"] = True  # mutant: lies about the outcome
    must_fail_path.write_text(json.dumps(data))

    with pytest.raises(vre.EntryError, match="record_schema_valid mismatch"):
        vre.validate_example(must_fail_path, record_schema, record_path)


def test_positive_example_declared_invalid_is_rejected(tmp_path):
    """The reverse direction: an example that actually PASSES schema
    validation but is declared as failing must also be a hard failure --
    two-sidedness cuts both ways."""
    examples_dir, record_schema, record_path = _copy_entry_fixtures(
        tmp_path, "mesh-join-card"
    )
    positive_path = examples_dir / "positive.json"
    data = json.loads(positive_path.read_text())
    data["expected"]["record_schema_valid"] = False  # mutant
    positive_path.write_text(json.dumps(data))

    with pytest.raises(vre.EntryError, match="record_schema_valid mismatch"):
        vre.validate_example(positive_path, record_schema, record_path)


def test_verify_ok_mismatch_is_rejected(tmp_path):
    examples_dir, record_schema, record_path = _copy_entry_fixtures(
        tmp_path, "mesh-join-card"
    )
    positive_path = examples_dir / "positive.json"
    data = json.loads(positive_path.read_text())
    data["expected"]["verify_ok"] = False  # mutant: the real capsule verifies ok=true
    positive_path.write_text(json.dumps(data))

    with pytest.raises(vre.EntryError, match="verify_ok mismatch"):
        vre.validate_example(positive_path, record_schema, record_path)


def test_missing_example_case_is_rejected():
    """validate_examples_dir resolves examples_dir relative to REPO_ROOT (so
    an entry's declared path always means the same thing regardless of how
    the validator was invoked) -- so the throwaway copy for this mutant must
    live under REPO_ROOT too, not under pytest's tmp_path."""
    dest = REAL_ENTRIES_DIR / "examples" / "_mutant_missing_case"
    shutil.copytree(REAL_ENTRIES_DIR / "examples" / "mesh-join-card", dest)
    try:
        (dest / "must-fail.json").unlink()

        entry = copy.deepcopy(yaml_load(REAL_ENTRIES_DIR / "mesh-join-card.yaml"))
        entry["examples_dir"] = str(dest.relative_to(vre.REPO_ROOT))

        with pytest.raises(vre.EntryError, match="missing required case"):
            vre.validate_examples_dir(entry, Path("mesh-join-card.yaml"))
    finally:
        shutil.rmtree(dest)


def test_bad_record_path_is_rejected(tmp_path):
    examples_dir, record_schema, _ = _copy_entry_fixtures(tmp_path, "mesh-join-card")
    positive_path = examples_dir / "positive.json"
    with pytest.raises(vre.EntryError, match="does not resolve"):
        vre.validate_example(positive_path, record_schema, ["nonexistent", "path"])


def yaml_load(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _copy_entry_fixtures(tmp_path: Path, name: str):
    """Copy one entry's examples dir under tmp_path (relative to vre.REPO_ROOT
    so validate_examples_dir's REPO_ROOT-relative resolution keeps working),
    returning (examples_dir, record_schema_dict, record_path)."""
    real_examples_dir = vre.REPO_ROOT / "registry" / "entries" / "examples" / name
    dest = tmp_path / "examples" / name
    shutil.copytree(real_examples_dir, dest)

    entry = yaml_load(REAL_ENTRIES_DIR / f"{name}.yaml")
    record_schema = vre.load_schema(vre.REPO_ROOT / entry["record_schema"]["path"])
    record_path = entry["record_schema"]["record_path"]
    return dest, record_schema, record_path
