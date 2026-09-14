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

- **Home-1 — mechanical.** The Canonical Payload Binding (CPB) registries, in
  [`scitt-payload-binding`](https://github.com/action-state-group/scitt-payload-binding).
  **Narrower than earlier text here assumed, restated against the live
  draft.** CPB-04's IANA Considerations
  (`spec/draft-mih-sokolov-scitt-payload-binding-04.md`, lines 1186–1196)
  requests exactly two IANA actions — one Canonicalization Algorithm
  Registry and one `cpb-refs` COSE Header Parameter — and states plainly:
  *"This document neither creates nor depends on an artifact-type registry.
  Artifact-type and digest-context declarations are owned and selected by
  profiles"* (same draft, Cross-Profile Comparability, lines 831–832:
  *"CPB creates no artifact-type registry"*). `scitt-payload-binding/
  REGISTRY.md` — the file this charter previously named as the citation
  target for every Digest Context table — now opens with its own
  supersession notice: for CPB-04 it is not a registry of record and
  creates no artifact-type registry either; it retains pre-03 material for
  audit only. **Consequence:** Home-1 remains the citation target for
  canonicalization-algorithm/token material (its Canonicalization Algorithm
  Registry section is live and normative). It is **not** a valid citation
  target for artifact-type or digest-context material — under CPB-04 that
  is profile-owned, and which document is the owning profile's normative
  source for it is an open question, tracked as NEEDS-STEVEN and
  coordinated with `[cpb-aac-entry-nonlive-repair]` Q1 so the two items
  return the same answer. No meaning lives at Home-1 either way — only how
  bytes are turned into a digest.
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

> **An entry's Digest Context table is never Home-2 content — it is always
> cited by reference, never duplicated, from whichever registry actually
> owns it.** That is CPB's Home-1 Canonicalization Algorithm Registry for an
> algorithm/token. For an artifact-type or digest-context declaration it is
> the owning profile's own normative registry, since CPB-04 creates no
> artifact-type registry of its own (see the Home-1 bullet above) —
> currently an open question for which document that is. Everything else
> that gives the entry's fields their agreed meaning — vocabulary, purpose,
> producer invariants, outcome semantics — is Home-2 content and is
> registered here, once an entry is promoted.

See [`REGISTRY.md`](REGISTRY.md) for the full entry format and the reserved
registry sections, and [`REGISTRATION-POLICY.md`](REGISTRATION-POLICY.md) for
how an entry moves from provisional to promoted.

## Why a third registry — the axis that separates it from AAC's own

There are, in total, **three** registries in the Agent Action Capsule family
today, and the "two registry homes" framing above needs one more line: the
Agent Action Capsule (AAC) profile keeps its **own** interim registry of
record,
[`agent-action-capsule/spec/REGISTRY.md`](https://github.com/action-state-group/agent-action-capsule/blob/main/spec/REGISTRY.md)
— `verdict_class`, `disposition.decision`, `effect.type`,
`irreversibility_class`, `effect_attestation`, `chain.relation`,
`citation_purpose` — which is neither Home-1 nor Home-2.

The axis that separates AAC's own registry from this one is **IANA-track vs
community-track**, not "capsule vs mechanics":

- **AAC's `spec/REGISTRY.md`** is *descriptive, not generative* — it records
  a vocabulary defined **normatively inside an Internet-Draft's IANA
  Considerations** (`draft-mih-scitt-agent-action-capsule`, §12) that
  travels to an IANA registry the moment that draft publishes. Change
  controller: Action State Group, Inc. (interim) → the IETF on publication.
- **This registry (Home-2)** is *generative* — a `Source:` line here may
  read `originates in this registry`. Change controller: Action State
  Group, Inc. (interim) → a neutral foundation home on donation, and it is
  **never** IANA-bound: composition slot profiles, action-type/outcome
  conventions, and the pack ecosystem are conventions that parties who will
  never file an Internet-Draft — pack publishers, adopters composing slot
  profiles — need to be able to extend.

**The test:** a vocabulary whose values are defined normatively in an
Internet-Draft's IANA Considerations belongs to that draft's own registry
and travels to IANA on publication. A convention that must stay extensible
by parties who will never file an Internet-Draft belongs here, and never
goes to IANA. **Consequence:** an entry registered here is **not** a
candidate for IANA transfer, unlike an entry in AAC's own registry or in
Home-1.

**Open naming question (NEEDS-STEVEN).** Three files are named `REGISTRY.md`
across three repositories, and the name `capsule-registry` reads as *the*
registry for capsules — when AAC's own `spec/REGISTRY.md` is the one whose
vocabularies a capsule's fields actually draw on. Whether repo/doc titles
should disambiguate (e.g. titling this one for *composition & semantics
conventions* rather than *capsule*) is flagged for Steven's call; this task
does not rename anything.

## No entries here yet

This repository is activation, not migration. No semantic content has moved
from CPB's provisional registry into this repository. An entry that
currently incubates whole in
[`scitt-payload-binding/spec/cpb-provisional-registry.md`](https://github.com/action-state-group/scitt-payload-binding/blob/main/spec/cpb-provisional-registry.md)
stays there, unsplit, until it receives its own promotion ruling — see
`REGISTRATION-POLICY.md`.
