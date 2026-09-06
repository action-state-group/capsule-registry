# Provenance — registry tooling port

## Source

The registry filing mechanism in this repository (`registry/entry.schema.json`,
`registry/entries/TEMPLATE.yaml`, `.github/validate_registry_entries.py`,
`.github/test_validate_registry_entries.py`, `.github/workflows/registry-entries.yml`)
is ported from `scitt-payload-binding`'s CPB Home-1 registry filing tooling:

- **Source repository:** `action-state-group/scitt-payload-binding`
- **Source branch:** `cpb-registry-operational-standup` (GitHub PR #77)
- **Source commit (branch head at port time):** `e136bf8012a5222c77784f428aa359af42f69956`
- **PR #77 status at port time:** **OPEN**, title `[HELD — Steven+Anton ratify]
  registry: operational standup — template, policy, CI validation, first
  entries, site scaffold`. **Not merged to `scitt-payload-binding` main.**

  This corrects an earlier live clarification in this task's coordination
  history that stated PR #77 "IS merged" and instructed porting from CPB's
  `main` branch. That instruction was checked against the actual repository
  state (`gh pr view 77`, `git merge-base --is-ancestor`) before acting on it
  and found to be factually incorrect — `main` at the time of this port
  (`bb648e15d4826ff78e7d71eb4f3cc87ec5e6713c` on `agent-action-capsule`,
  separately; `scitt-payload-binding` `main` carries none of PR #77's
  registry-entries commits) does not contain any of this tooling. This port
  follows the ORIGINAL inbox task's instruction instead: port from #77's
  branch head, cite the SHA, and re-sync if Anton's review changes it. See
  this task's outbox entry for the full note.

- **Relevant source commits, in order** (`scitt-payload-binding main..e136bf8`):
  - `5ba79e7` registry: add entry template, machine schema, and CI vector-execution gate
  - `9a2d6d0` registry: wire fork-safe CI + first four conformant entries
  - `d5d5a21` spec: draft CPB registry operational policy (HELD — Steven+Anton ratify)
  - `412d504` site: add self-contained static HTML build
  - `a8fe484` site: scaffold canonicalpayloadbinding.org content
  - `8704c46` site+entry: neutrality review fixes
  - `e136bf8` site: soften Neutrality to draft-proposes

- **agent-action-capsule commit pinned for `agent_action_capsule.verify`
  and example generation:** `bb648e15d4826ff78e7d71eb4f3cc87ec5e6713c`
  (`action-state-group/agent-action-capsule`, `main` at port time).

## Vendored copy, not a fork of the logic core

Per the `[neutrality-gate-canonical-superset]` pattern (copy the canonical
group's mechanism rather than build a competing third variant): this repo's
`entry.schema.json`, `TEMPLATE.yaml`, and `validate_registry_entries.py` are
a **vendored, adapted copy** of CPB's shape (schema-validate an entry file +
run every declared example through a verifier + reject on mismatch,
including MUST-FAIL must actually fail) — not an independent reimplementation
that could silently drift into a different discipline. See `registry/README.md`
("Three differences from the CPB mechanism this mirrors") for exactly what
changed and why (Steven's 2026-09-05 ruling): examples are verifier-graded
records instead of digest fixtures; promotion is a per-entry ruling instead
of a Designated Expert panel; no IANA-forwarding clause.

## Drift check

Because the source (PR #77) is **unmerged and HELD pending Steven+Anton
ratification**, its shape can still change before it lands. Before treating
this repository's tooling as settled:

1. Re-check PR #77's status: `gh pr view 77 --repo action-state-group/scitt-payload-binding`.
2. If merged, or if the branch head has moved past `e136bf8`, diff the
   relevant files (`registry/entry.schema.json`, `registry/entries/TEMPLATE.yaml`,
   `.github/validate_registry_entries.py`) between `e136bf8` and the new head:
   ```
   git diff e136bf8..<new-head> -- registry/entry.schema.json registry/entries/TEMPLATE.yaml .github/validate_registry_entries.py
   ```
3. Fold in any shape change that isn't one of Home-2's three deliberate
   differences (above), and update this file's "Source commit" line.

No entry in this repository promotes or otherwise depends on this drift
check being current — it only affects whether the FILING TOOLING itself
still mirrors CPB's mechanism faithfully.
