# Registration Policy

**Status.** This document is the interim registration policy for
capsule-registry. It governs how an entry moves through this registry's
lifecycle. It does not yet accept registrations — see
[`REGISTRY.md`](REGISTRY.md) for the reserved sections awaiting activation.

## Scope

This policy covers Home-2 content only: composition slot profiles,
action-type conventions, outcome conventions, cross-profile purpose labels,
and the pack ecosystem (publishers, packs, fold envelopes, adapters). It
never covers algorithms, digest contexts, or canonicalization profiles.
Algorithm/canonicalization-token content is CPB's Home-1 policy (see
[`scitt-payload-binding/REGISTRY.md`](https://github.com/action-state-group/scitt-payload-binding/blob/main/REGISTRY.md)
for its live Canonicalization Algorithm Registry section); artifact-type and
digest-context content is profile-owned under CPB-04 and its citation
target is not yet settled — see
[`README.md`](README.md#two-registry-homes-split-by-layer) for the full
restatement and the open NEEDS-STEVEN.

For why this registry exists as a **third** home distinct from CPB's Home-1
and from the Agent Action Capsule profile's own `spec/REGISTRY.md`, see
[`README.md`](README.md#why-a-third-registry--the-axis-that-separates-it-from-aacs-own).

A purpose label registered here is one belonging to the composition model's
own slot bindings. A purpose vocabulary that is a registered member of
another profile's wire format registers with that profile —
`citation_purpose` is a member of the Agent Action Capsule profile and
registers in that profile's registry, not here.

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

A promoted entry is immutable in meaning. If a convention changes, a new
entry is registered; a promoted entry's registered semantics are never
modified retroactively. A bibliographic correction or a lifecycle status
transition is not a change of meaning.

There is no Designated Expert ladder here, unlike CPB's Home-1 registry.
Home-2's registration authority is the **Registry Editor** role — not an
open third-party-documented / owner-confirmed rung system, and not any named
individual's standing authority. This is a deliberate simplification:
Home-1's ladder exists because IANA eventually inherits that registry and
needs an auditable provenance trail for entries it did not write; Home-2
records ecosystem convention, not IANA-bound registrations.

**Change controller: Action State Group, Inc. (interim).** Home-2 is not
IANA-bound *today*, so there is no present RFC-publication handoff of the
kind Home-1 states — claiming one now would misdescribe this registry. That
is a present-tense fact with a named condition, not a permanent property:
the composition slot profiles and cross-profile purpose labels back an
Internet-Draft that reserves the right to propose a slot-identifier registry
in a later revision; if it does, those sections become that document's
interim registry of record and follow it to IANA on publication, exactly as
the Agent Action Capsule profile's registry does. The pack schema and
`pack_id` namespace have no standards-track document and remain here in
every case. (The Agent Action Capsule ↔ TRACE citation work now under way is
itself cross-document coordination of the kind that eventually calls for
that registry.)

The stated succession is: on donation of this registry to a neutral
foundation home (the same donation path stated in the Agent Action Capsule
project's
[`GOVERNANCE.md`](https://github.com/action-state-group/agent-action-capsule/blob/main/GOVERNANCE.md)),
change control transfers to that home. Until then, Action State Group, Inc.
holds change control, exercised through the Registry Editor role.

If Action State Group, Inc. transfers, merges, is acquired, or ceases to
operate before that donation, change control passes to a successor that
maintains this registry under the same license and the same policy. Absent
such a successor, the license governs and any party may fork and continue
it. In every case a registered identifier keeps its registered meaning: **no
successor and no fork may reuse a registered identifier for different
semantics.**

## What a promotion ruling requires

A promotion ruling names, per entry:

1. The entry's semantic content (vocabulary, purpose, producer invariants,
   outcome conventions — never a Digest Context table; see the within-entry
   rule in `README.md`).
2. Its citation to whichever registry actually owns the entry's mechanical
   counterpart, if it has one — CPB's Home-1 Canonicalization Algorithm
   Registry for an algorithm/token, or the owning profile's own normative
   registry for an artifact-type/digest-context declaration (CPB-04 creates
   no artifact-type registry of its own; see `README.md`). A Home-2 entry
   MUST cite that source by reference for any such content it depends on,
   never restate it.
3. The reserved section it activates or extends (see `REGISTRY.md`).

## No entries migrate without a per-entry ruling

An entry that exists today in CPB's provisional registry
(`scitt-payload-binding/spec/cpb-provisional-registry.md`) — carrying both a
Digest Context table and semantic content in the same entry — is **not**
split by default when this policy activates. It stays whole, in place, in
CPB's provisional registry, until it receives its own promotion ruling. On
that ruling, the Digest Context table does **not** route here in any case —
it stays wherever it normatively belongs (CPB's provisional registry today;
see `README.md` for the open question of whether that is its lasting home
under CPB-04). Only the semantic content routes here.

## Continuity

This registry does not depend on the continued existence of its custodian.

- It is Apache-2.0. No transfer, dissolution, or change of steward can remove
  its contents from the ecosystem.
- Promoted entries are immutable in meaning, so a successor or a fork inherits
  a record it cannot rewrite.
- Its state is plain files in a public git repository. Any party can hold a
  complete copy today.
- **Every entry declares its source** — either a commit-pinned external
  reference, which stays resolvable from the party that owns it, or an
  explicit declaration that the convention originates here, in which case it
  travels with this registry under its license.

These are properties a reader can check, not undertakings this project asks to
be trusted on. The succession statement above says who is expected to carry
it; these say why the record survives regardless.
