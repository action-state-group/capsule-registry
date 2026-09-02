# Registration Policy

**Status.** This document is the interim registration policy for
capsule-registry. It governs how an entry moves through this registry's
lifecycle. It does not yet accept registrations — see
[`REGISTRY.md`](REGISTRY.md) for the reserved sections awaiting activation.

## Scope

This policy covers Home-2 content only: composition slot profiles,
action-type conventions, outcome conventions, cross-profile purpose labels,
and the pack ecosystem (publishers, packs, fold envelopes, adapters). It
never covers algorithms, digest contexts, or canonicalization profiles —
that is CPB's Home-1 policy, in
[`scitt-payload-binding/REGISTRY.md`](https://github.com/action-state-group/scitt-payload-binding/blob/main/REGISTRY.md).

## Entry lifecycle

Entries move through exactly two states:

```
provisional  →  promoted
```

- **`provisional`.** An entry that exists — referenced from code, a
  companion specification, or a CPB provisional-registry entry's non-Digest-
  Context content — but has not yet received a promotion ruling. A
  provisional entry is *proposed*, not registered: nothing in this registry
  verifies against it, and no verifier is entitled to rely on it.
- **`promoted`.** An entry Steven (or, once delegated, the spec-tier gate)
  has ruled on, per entry. Promotion is a **per-entry ruling, not a batch
  operation** — an entry does not become `promoted` by virtue of a sibling
  entry's promotion, and a pull request proposing more than one entry gets
  more than one ruling.

There is no Designated Expert ladder here, unlike CPB's Home-1 registry.
Home-2's registration authority is Steven's ruling (or the spec-tier gate,
once this repository's governance is formally delegated) — not an open
third-party-documented / owner-confirmed rung system. This is a deliberate
simplification: Home-1's ladder exists because IANA eventually inherits that
registry and needs an auditable provenance trail for entries it did not
write; Home-2 records ecosystem convention, not IANA-bound registrations.

## What a promotion ruling requires

A promotion ruling names, per entry:

1. The entry's semantic content (vocabulary, purpose, producer invariants,
   outcome conventions — never a Digest Context table; see the within-entry
   rule in `README.md`).
2. Its Home-1 citation, if the entry has a mechanical counterpart already
   registered or provisional in CPB's registries — a Home-2 entry MUST cite
   Home-1 by reference for any digest-context content it depends on, never
   restate it.
3. The reserved section it activates or extends (see `REGISTRY.md`).

## No entries migrate without a per-entry ruling

An entry that exists today in CPB's provisional registry
(`scitt-payload-binding/spec/cpb-provisional-registry.md`) — carrying both a
Digest Context table and semantic content in the same entry — is **not**
split by default when this policy activates. It stays whole, in place, in
CPB's provisional registry, until it receives its own promotion ruling. On
that ruling, the Digest Context table stays in CPB (Home-1); the semantic
content is what routes here.
