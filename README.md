# capsule-registry

*An Action State Group project.*

**capsule-registry** is the composition/semantics registry for the Agent
Action Capsule (AAC) ecosystem — the record of what capsule fields and
conventions *mean*, as opposed to how they are canonicalized and digested.

> **Status.** Public, skeleton plus policy — **no entries yet**. This
> repository holds the registry structure and registration policy; entries
> arrive by per-entry ruling under [`REGISTRATION-POLICY.md`](REGISTRATION-POLICY.md),
> not on a schedule. Nothing here should be read as the registry already
> operating — it isn't, until its first entry is promoted.

## Two registry homes, split by layer

There are two registries in the Agent Action Capsule family, and they are
**not competing** — they are split by what kind of fact each one records:

- **Home-1 — mechanical.** The Canonical Payload Binding (CPB) registries of
  record, in
  [`scitt-payload-binding`](https://github.com/action-state-group/scitt-payload-binding)
  (see its [`REGISTRY.md`](https://github.com/action-state-group/scitt-payload-binding/blob/main/REGISTRY.md)).
  Algorithms, digest contexts, canonicalization profiles, byte widths. No
  meaning lives there — only how bytes are turned into a digest.
- **Home-2 — semantics (this repository).** Composition slot profiles,
  action-type and outcome conventions, cross-profile purpose labels, and the
  pack ecosystem (publishers, packs, fold envelopes, adapters) that gives
  capsule fields and compositions their agreed meaning.

**The within-entry rule (law).** A single registry entry frequently has both
kinds of content — for example, a proposed artifact type carries a
mechanical **Digest Context** table (algorithm, field set, exclusion set,
domain separation, pre-image encoding, representation) *and* semantic
content such as a closed vocabulary or a producer invariant. The rule that
resolves which home each part belongs to:

> **An entry's Digest Context table is Home-1 (CPB) content, always cited by
> reference from here, never duplicated.** Everything else that gives the
> entry's fields their agreed meaning — vocabulary, purpose, producer
> invariants, outcome semantics — is Home-2 content and is registered here,
> once an entry is promoted.

See [`REGISTRY.md`](REGISTRY.md) for the full entry format and the reserved
registry sections, and [`REGISTRATION-POLICY.md`](REGISTRATION-POLICY.md) for
how an entry moves from provisional to promoted.

## No entries here yet

This repository is activation, not migration. No semantic content has moved
from CPB's provisional registry into this repository. An entry that
currently incubates whole in
[`scitt-payload-binding/spec/cpb-provisional-registry.md`](https://github.com/action-state-group/scitt-payload-binding/blob/main/spec/cpb-provisional-registry.md)
stays there, unsplit, until it receives its own promotion ruling — see
`REGISTRATION-POLICY.md`.
