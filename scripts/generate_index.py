#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate site/index.html: a read-only listing of every filed entry under
registry/entries/. NOT a second source of truth -- REGISTRY.md and
REGISTRATION-POLICY.md remain normative; this is a rendering of the same
entry files validate_registry_entries.py already checks, for
agentactioncapsule.org (Home-2 is AAC-side by Steven's ruling). Re-run by
hand and commit the output; this repository has no publish/deploy step of
its own yet since it is still pre-flip/private.

Usage: python3 scripts/generate_index.py
"""
from __future__ import annotations

import html
import pathlib

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "registry" / "entries"
OUT_PATH = REPO_ROOT / "site" / "index.html"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>capsule-registry — Home-2 semantics filings</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 60rem; margin: 2rem auto; padding: 0 1rem; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccc; padding: 0.5rem; text-align: left; vertical-align: top; }}
  th {{ background: #f4f4f4; }}
  .status-provisional {{ color: #a86a00; }}
  .status-promoted {{ color: #157a15; }}
  code {{ background: #f4f4f4; padding: 0.1rem 0.3rem; }}
</style>
</head>
<body>
<h1>capsule-registry — Home-2 semantics filings</h1>
<p>
  Generated from <code>registry/entries/*.yaml</code> by
  <code>scripts/generate_index.py</code>. <strong>This is a rendering, not
  the registry</strong> — <code>REGISTRY.md</code> and
  <code>REGISTRATION-POLICY.md</code> are normative. No entry listed here is
  promoted unless its status column says so; a <code>provisional</code>
  entry is proposed, not registered, and nothing verifies against it.
</p>
<table>
<thead>
<tr><th>Name</th><th>Kind</th><th>Status</th><th>Owner</th><th>Home-1 reference</th><th>Open questions</th></tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>
"""

ROW_TEMPLATE = """<tr>
  <td><code>{name}</code></td>
  <td>{kind}</td>
  <td class="status-{status}">{status}</td>
  <td>{owner}</td>
  <td>{home1_reference}</td>
  <td>{open_question_count} open</td>
</tr>"""


def _esc(value: object) -> str:
    return html.escape(str(value))


def main() -> int:
    rows = []
    for path in sorted(ENTRIES_DIR.glob("*.yaml")):
        if path.name == "TEMPLATE.yaml":
            continue
        entry = yaml.safe_load(path.read_text(encoding="utf-8"))
        rows.append(
            ROW_TEMPLATE.format(
                name=_esc(entry["name"]),
                kind=_esc(entry["kind"]),
                status=_esc(entry["status"]),
                owner=_esc(entry["owner"]["name"]),
                home1_reference=_esc(entry.get("home1_reference") or "—"),
                open_question_count=len(entry.get("open_questions", [])),
            )
        )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(TEMPLATE.format(rows="\n".join(rows)), encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(rows)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
