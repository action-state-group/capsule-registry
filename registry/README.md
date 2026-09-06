# capsule-registry entries — the machine-checkable filing path

This directory is the machine-checkable half of a Home-2 semantics filing.
**REGISTRY.md remains the normative record** — its reserved sections are
where a promoted entry ultimately lives, and REGISTRATION-POLICY.md remains
the normative record of the (two-state: provisional → promoted) lifecycle.
Nothing here changes that. What this directory adds is a **structured,
schema-validated filing format**, mirroring the one built for CPB's Home-1
registry (`scitt-payload-binding` PR #77 — see [`PROVENANCE.md`](../PROVENANCE.md)
for the exact source and what changed for Home-2), so a filer does not have
to hand-reproduce REGISTRY.md's within-entry rule and REGISTRATION-POLICY.md's
lifecycle correctly before their first PR can go green.

## The idea

1. Copy [`entries/TEMPLATE.yaml`](entries/TEMPLATE.yaml) to `entries/<name>.yaml`.
2. Fill in the metadata (owner, reference, kind, `home1_reference` if a CPB
   Home-1 counterpart exists), name your closed enums with their meanings,
   and point `record_schema` at a JSON Schema you add under
   [`schemas/`](../registry/schemas/) covering the entry's semantic content
   only — never a Digest Context table (REGISTRY.md's within-entry rule).
3. Add three example records under `entries/examples/<name>/`: `positive.json`,
   `boundary.json`, `must-fail.json`, each shaped
   ```
   {"kind": "positive"|"boundary"|"must_fail",
    "expected": {"record_schema_valid": bool, "verify_ok": bool, "notes": str},
    "record": <the example capsule, or the bare record if record_schema.record_path is []>}
   ```
4. Open a PR. [`.github/workflows/registry-entries.yml`](../.github/workflows/registry-entries.yml)
   runs [`.github/validate_registry_entries.py`](../.github/validate_registry_entries.py),
   which:
   - validates your file against [`entry.schema.json`](entry.schema.json);
   - for each example, validates the record at `record_schema.record_path`
     against your declared schema, and runs the full record through
     `agent-action-capsule verify` — comparing BOTH actual outcomes against
     your example's declared `expected` block, and **rejecting the entry**
     if a `must_fail` example does not actually fail, or a `positive`/
     `boundary` example does not actually pass, either check.
5. Green CI gets this entry to `provisional`. It does **not** promote it —
   promotion past `provisional` is Steven's (or the spec-tier gate's, once
   delegated) per-entry ruling, REGISTRATION-POLICY.md — never a batch
   operation, never inferred from a sibling entry, and there is no
   ≥2-organization Designated Expert panel here (unlike CPB's Home-1) unless
   and until a second organization files a semantics entry.

## Three differences from the CPB mechanism this mirrors

Steven's ruling, 2026-09-05 (see [`PROVENANCE.md`](../PROVENANCE.md)):

1. **Examples are graded records, not digest fixtures.** An entry's
   `positive.json`/`boundary.json`/`must-fail.json` are full example records
   that validate against the entry's own declared schema *and* grade as
   expected through `agent-action-capsule verify` — never CPB-style digest
   fixtures run through `check_vectors.py`.
2. **Promotion is a per-entry ruling, not a Designated Expert panel** —
   REGISTRATION-POLICY.md already states this; this tooling does not
   introduce a DE ladder for Home-2.
3. **No IANA-forwarding clause.** AAC-04 creates no IANA registry for Home-2
   content, so none is implied by any entry here, unlike CPB's own
   (still-HELD) IANA-forwarding language.

## What this is not

- **Not a second source of truth.** `registry/entries/*.yaml` files are
  filings, not the registry. A promoted entry's normative text lives in
  REGISTRY.md, cited from there, never duplicated by regenerating it from
  these files (there is no `gen_registry.py`-equivalent here yet — see
  [`../scripts/generate_index.py`](../scripts/generate_index.py) for the
  read-only site index generator, which is not that).
- **Not a policy change.** REGISTRATION-POLICY.md's lifecycle and the
  within-entry rule (REGISTRY.md) are exactly as those documents state them
  today. This directory is tooling built against that policy.
- **Not a substitute for a promotion ruling.** A `provisional` filing here is
  exactly as provisional as the equivalent prose filing would be. Nothing in
  this schema lets a filer assert `promoted` for their own entry — the
  schema requires a `promoted_by` line naming who ruled and when, and no
  filer names themself there.

## Filed entries

| File | Registers | Kind / status |
|---|---|---|
| [`entries/mesh-join-card.yaml`](entries/mesh-join-card.yaml) | `mesh-join-card/1` (capsule-emit-mesh) | record-schema / provisional |
| [`entries/mesh-history-card.yaml`](entries/mesh-history-card.yaml) | `mesh-history-card/1` (capsule-emit-mesh) | record-schema / provisional |
| [`entries/adjudication-verdict.yaml`](entries/adjudication-verdict.yaml) | adjudication `verdict` enum + `chain.relation=adjudicates` (capsule-emit) | outcome / provisional |

Each of these is a worked example of the template, including a real,
`agent-action-capsule verify`-graded example set — read them alongside
`TEMPLATE.yaml` if a field's intent isn't obvious from the template comments
alone. **None of these are promoted.** Each entry's `open_questions` lists
what a promotion ruling would need to settle — see the filing task's outbox
note for the consolidated list.
