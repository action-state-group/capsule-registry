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
- **`promoted`.** An entry the **Registry Editor** — this registry's
  spec-tier gate — has ruled on, per entry. Promotion is a **per-entry
  ruling, not a batch operation** — an entry does not become `promoted` by
  virtue of a sibling entry's promotion, and a pull request proposing more
  than one entry gets more than one ruling.

There is no Designated Expert ladder here, unlike CPB's Home-1 registry.
Home-2's registration authority is the **Registry Editor** role — not an
open third-party-documented / owner-confirmed rung system, and not any named
individual's standing authority. This is a deliberate simplification:
Home-1's ladder exists because IANA eventually inherits that registry and
needs an auditable provenance trail for entries it did not write; Home-2
records ecosystem convention, not IANA-bound registrations.

**Change controller: Action State Group, Inc. (interim).** Home-2 is not
IANA-bound, so there is no RFC-publication handoff of the kind Home-1
states — that would misdescribe this registry. The stated succession is:
on donation of this registry to a neutral foundation home (the same
donation path stated in the Agent Action Capsule project's
[`GOVERNANCE.md`](https://github.com/action-state-group/agent-action-capsule/blob/main/GOVERNANCE.md)),
change control transfers to that home. Until then, Action State Group, Inc.
holds change control, exercised through the Registry Editor role.

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
