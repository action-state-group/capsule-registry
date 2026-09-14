# Registry of record — capsule composition & semantics (Home-2)

**Status.** Skeleton only. Every section below is **reserved** — its name
and shape are fixed so entries have a stable place to land, but no section
carries entries yet. See [`REGISTRATION-POLICY.md`](REGISTRATION-POLICY.md)
for how a section moves from reserved to accepting entries, and for how an
individual entry moves from `provisional` to `promoted`.

This registry never records algorithms, digest contexts, or
canonicalization profiles, under any reading. Canonicalization-algorithm
material is CPB's Home-1 registry, in
[`scitt-payload-binding/REGISTRY.md`](https://github.com/action-state-group/scitt-payload-binding/blob/main/REGISTRY.md)
(its live Canonicalization Algorithm Registry section). Artifact-type and
digest-context material is, under CPB-04, profile-owned rather than a CPB
registry — its citation target is not yet settled; see
[`README.md`](README.md#two-registry-homes-split-by-layer) for the full
restatement and the open NEEDS-STEVEN.

## Entry format — the within-entry rule

Every entry in this registry follows one rule, stated in full in
[`README.md`](README.md#two-registry-homes-split-by-layer):

> **An entry's Digest Context table is never Home-2 content — it is always
> cited by reference, never duplicated, from whichever registry actually
> owns it** (CPB's Home-1 Canonicalization Algorithm Registry for an
> algorithm/token; the owning profile's own registry for an artifact-type or
> digest-context declaration, since CPB-04 creates no artifact-type registry
> of its own). Everything else that gives the entry's fields their agreed
> meaning is Home-2 content and is registered here.

Concretely, an entry that has a mechanical counterpart takes this shape:

```
### `<name>`

**Digest-context reference:** <link to whichever registry normatively owns
this name's Digest Context table — CPB's Home-1 Canonicalization Algorithm
Registry entry, a CPB provisional-registry entry, or the owning profile's
own registry>
**Status:** provisional | promoted
**Source:** a commit-pinned external reference — `owner-org/owner-repo @ <full-commit-hash>`, an I-D revision, or an RFC — or the literal `originates in this registry` for a convention with no external source. A branch or tag alone is not a pin; both can move after the fact.
**Promoted by:** <Registry Editor ruling, date> — provisional entries omit this line

<Semantic content: vocabulary, purpose, producer invariants, outcome
conventions. NEVER a Digest Context table — that table lives at the
Digest-context reference above and is cited, not copied.>
```

An entry with no mechanical counterpart (e.g. a pack, a publisher
namespace claim) omits the `Digest-context reference` line entirely — there
is nothing to cite. The `Source` line is never omitted: an entry with no
external source declares `originates in this registry`, so every entry
states its provenance either way. The `Digest-context reference`, when
present, is an internal cross-link to the owning registry's digest-context
content, not this provenance pin — the two are distinct lines.

---

## Reserved sections

The sections below are named and scoped now so that when an entry is
promoted, it has an unambiguous place to go. **None of them accept entries
yet.**

### Composition Slot Profiles (WHO / CAN / DID / AUDIT + WHAT)

Reserved for the registered slot profiles of the composition model — the
WHO / CAN / DID / AUDIT slots plus the WHAT slot's self-reference binding.
No profiles are registered yet.

### Action-Type Conventions

Reserved for the controlled vocabulary of action-type names (e.g. the
`payment.*`, `comms.*`, `authority.*` families) — the Agent Action Semantics
layer, community-extensible. No conventions are registered yet.

### Outcome Conventions

Reserved for the controlled vocabulary of outcome values and their
semantics (e.g. closed-set terminal/outcome states and what each one means
for a verifier reading a composed record). No conventions are registered
yet.

### Cross-Profile Purpose Labels

Reserved for the shared vocabulary of purpose labels used across composition
profiles at the WHAT slot's self-reference binding, so that a purpose label
means the same thing regardless of which profile emitted it. No labels are
registered yet.

### Pack Schema & `pack_id` Namespace

Reserved for the pack ecosystem: publisher namespace claims, pack
definitions (`publisher/name/semver`), fold envelope definitions, and
adapter/implementation conformance listings. No publishers, packs, fold
envelopes, or adapters are registered yet.

---

## No entries migrate without a per-entry ruling

See [`REGISTRATION-POLICY.md`](REGISTRATION-POLICY.md#no-entries-migrate-without-a-per-entry-ruling).
An entry that exists today, whole, in CPB's provisional registry is not
split into these sections by default — each one waits for its own
promotion ruling.
