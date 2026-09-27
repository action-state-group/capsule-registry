# `nostr-pubkey` host-principal profile + first Buzz Evidence Contract profiles

**Status: field sets ruled; staged, not yet a registered entry.** The field sets and
moderation-record semantics below were drafted from Evidence Contract v3 §7 and EvidenceBook v3
§3/§12/§14/§18.1 (both not yet published). The subject shape is ruled (below); three narrower
points stay explicitly **UNRULED** and are flagged where they occur.

**Field-set ruling, 2026-09-23 (quoted; editorial elision in brackets):**

> UNIFORM `semantic_digest`: the EvidenceRecord subject is `{event_id, semantic_digest}` for
> EVERY profile — NO per-profile digest names ([the three per-profile subject digest names used
> in earlier drafts] withdrawn). "What kind" is carried by the profile id + epistemic types,
> never the field name. Extra digested facts go as NAMED digests in the record BODY/epistemic
> payload, never by renaming the subject digest. Rationale: uniform neutral verify surface (one
> field for every profile/connector; no special-casing).

Applied throughout Entries 2–4 below: every record under every profile here carries exactly
`subject: {event_id, semantic_digest}`.

**Still UNRULED (flagged, not decided here):**
- Entry 1's `relay_hint` companion field — proposed by this draft, not yet ruled.
- The `minimum_assurance` / `retention_check` placeholder values in Entries 2–4's evidence
  requirements — placeholders, to be confirmed.
- Registry **placement** — which reserved section, if any, these entries land in (see the next
  section). Until placement is ruled, this file stays a staged `drafts/` file, not a
  `REGISTRY.md` entry.

## Why this file, not `REGISTRY.md` directly

`REGISTRY.md`'s five reserved sections (Composition Slot Profiles, Action-Type Conventions,
Outcome Conventions, Cross-Profile Purpose Labels, Pack Schema & `pack_id` Namespace) do not name a
home for either kind of entry drafted below, and `REGISTRATION-POLICY.md`'s stated scope line
("composition slot profiles, action-type conventions, outcome conventions, cross-profile purpose
labels, and the pack ecosystem") does not cover them either. Checked explicitly against the
Composition Model's own WHO slot (`agent-accountability-composition`'s
`draft-mih-sato-agent-accountability-composition.md`, "The WHO Slot: Named-Human Authorization") —
that slot is pre-execution named-human *authorization*, a different concept from EvidenceBook's
`principal_ref` *identity* binding (EvidenceBook v3 §12 draws this same distinction explicitly: "A
host-principal binding does not change [the CLL/custody] rule... which `principal_ref` a record
carries is an identity question"). A `nostr-pubkey` host-principal profile is not a WHO-slot
profile and does not belong in that reserved section.

This is a registry-structure gap, not a field-set question, and adding a sixth reserved section (or
widening `REGISTRATION-POLICY.md`'s scope line) is a bigger call than "register an entry" — it is
left **UNRULED** for the Registry Editor. This file stages the drafted content in registry
entry-format (`REGISTRY.md`'s within-entry rule) so it is ready to move the moment placement is
ruled.

## Entry 1 — `nostr-pubkey` (host-principal profile)

**Status:** the `pubkey` field is settled; `relay_hint` is **UNRULED** (see below). Would be
`provisional` once placed under a ruled section.
**Source:** EvidenceBook v3 §12 ("Host-principal model"), §18.1 (worked example) — not yet
published; not yet a commit-pinned public reference.
**Promoted by:** — (none yet)

`principal_ref` under this profile identifies "the holder of a Nostr public key," nothing more
(EvidenceBook v3 §12).

**Carries:**
- `pubkey` (required) — a Nostr public key (secp256k1 / BIP-340 Schnorr), the same identity
  primitive Buzz/mesh nodes already use for discovery (EvidenceBook v3 §13, §18.1). Wire encoding:
  64-char lowercase hex (the raw x-only public key). A `bech32` `npub` string is a display
  encoding only and is never the wire value this profile registers.
- `relay_hint` (optional) — **new field proposed by this draft, not present in EvidenceBook v3
  §3/§12 today** — a relay URL where events signed by this key are commonly found. Strictly
  informational: it is never load-bearing for identity, verification, or authority, and its
  absence, staleness, or falsity never changes what this profile does or does not establish. This
  draft carries it as a companion field alongside `principal_ref` (e.g.
  `principal_ref_relay_hint` on the EvidenceBook record header) rather than folding it into the
  `principal_ref` string itself, so that `principal_ref`'s existing `scheme:value` shape
  (Evidence Contract v3 §3.1: `"nostr-pubkey:<hex>"`) is unchanged. **UNRULED** — this field is
  proposed by this draft, is not found in either source spec, and needs its own ruling.

**Does NOT assert (EvidenceBook v3 §9, §12, restated normatively for this entry):**
- **Not authority.** Key control is never authority (Evidence Contract v3 §3.1; EvidenceBook v3 §12).
  That a signature verifies against a `principal_ref` under this profile establishes only that the
  signer controlled the named private key at signing time — never that the key-holder was
  authorized to act in any community, role, or organizational capacity.
- **Any community/role authority-context binding.** Such a binding (e.g. "this pubkey moderates
  this Buzz community") is a separate, host-managed mapping, referenced if at all via
  `actor_role_ref` or `counterparty_ref` on the record header — never inferred from `principal_ref`
  alone (EvidenceBook v3 §12).
- **Continuity of the person/agent behind the key across time.** A principal may rotate keys; this
  profile records one key's holder as of the signature it accompanies, nothing longer-lived.

**Boundary.** This entry does not define the Nostr signer implementation (EvidenceBook v3 §13) or
Evidence Contract's `principal` block (Evidence Contract v3 §3.1, `principal.principal_ref` /
`principal.authority_context`) — it registers only what a `principal_ref` value under this scheme
means, per the within-entry rule.

---

## Entries 2–4 — first Buzz Evidence Contract profiles (Evidence Contract v3 §7)

Evidence Contract v3 §7 names these three profiles and states one paragraph of intent each,
explicitly deferring field sets to the profile work. The field sets below are that deferred work,
drafted from §7's intent paragraphs plus the worked-example conventions already ratified in that
document's Appendix A (outcome / process + obligation / human_role shapes). **The subject shape of
all three is ruled** (uniform `semantic_digest`, 2026-09-23, quoted above); the placeholders
marked **UNRULED** below are not.

Common rules across all three (restated normatively for every entry below):
- **Key control is never authority** — every principal reference in these profiles is a
  `nostr-pubkey` `principal_ref` (Entry 1) and inherits that entry's "does NOT assert" list in
  full.
- **One uniform subject: `subject: {event_id, semantic_digest}` — the same two fields, with the
  same names, under every profile.** `event_id` is the Buzz transport event id (a specific
  transmission on the Nostr transport, not recomputable from bytes alone; EvidenceBook v3 §14).
  `semantic_digest` is the content identity of that event's payload (recomputable). They are kept
  DISTINCT — two REQUIRED fields, never one: a conforming producer MUST NOT emit a record where one
  value stands in for the other, and a conforming validator MUST reject one that does. No profile
  renames `semantic_digest` or adds a per-profile digest field to `subject`; "what kind" of
  subject a record is about is carried by `contract_ref` (the profile id) + `epistemic_type`,
  never by the field name.
- **Extra digested facts are NAMED body digests.** A digested fact beyond the subject (e.g. the
  content a moderation decision was made over, the decision itself, or a release's approval
  record) is carried as a separate, named entry in the record body's `payload_commitments`
  (`{digest_alg, digest, role}`, with `role` naming the fact) — never as a second `subject` field.
- **Digest construction is out of scope here.** This registry records which digested facts a
  record names and what they mean; how any digest is computed is defined outside this
  registry.
- **No message text in any record — digests only.** No field on a record under any of these three
  profiles carries moderated content, job output, or release-note free text; every content
  reference is a `{digest_alg, digest}` pair.
- **No per-user history and no scores.** No field aggregates a principal's history across records,
  and no field carries a numeric score or rating of any kind.

### Entry 2 — `buzz.agent-job/v1`

**Status:** subject shape ruled (uniform `semantic_digest`, 2026-09-23); would be `provisional`
once placed under a ruled section.
**Source:** Evidence Contract v3 §7 — not yet published.
**Promoted by:** — (none yet)

**Intent (§7, quoted):** *"an outcome-profile contract over a Buzz agent job: did the job produce
the required effect, evaluated against Buzz-native evidence (Nostr event refs, agent-job records)
rather than an Action-State-native capsule. First concrete consumer of the `nostr-pubkey`
host-principal profile."*

**Profile:** `outcome` (Evidence Contract v3 §3.2).

**Subject shape:**

Evidence Contract subject (population level; unchanged by this ruling):
```
subject:
  job_type: "buzz.agent-job"
  population_selector: <host-defined — e.g. "agent jobs closed in evaluation_period">
```

EvidenceRecord subject (uniform, per the 2026-09-23 ruling — the same two fields for every profile
in this file):
```
subject:
  event_id: <Nostr event id of the job's terminal event — transport reference, EvidenceBook v3 §14>
  semantic_digest: <semantic digest of the job-outcome payload — content identity, §14>
```

**Evidence requirements (illustrative, mirrors Appendix A.1's outcome shape):**
```
evidence_requirements:
  accepted_epistemic_types: [OBSERVED_EVENT, SYSTEM_OF_RECORD_FACT]
  required_sources: [buzz-agent-job-record, nostr-event-log]
  minimum_assurance: [self-attested]   # UNRULED placeholder — to confirm whether a stronger floor applies
  coverage: "all closed agent jobs in population"
```

**Obligation refs:** none identified as real for this profile — an agent-job outcome contract is
not, by itself, evidence toward a named regulatory obligation. If a specific deployment ties an
agent-job outcome to an obligation, that binding is `obligation_refs` on the *contract*
(Evidence Contract v3 §3.1), stated by that deployment, not by this profile entry.

### Entry 3 — `buzz.moderation/v1`

**Status:** subject shape ruled (uniform `semantic_digest`, 2026-09-23); would be `provisional`
once placed under a ruled section.
**Source:** Evidence Contract v3 §7 — not yet published.
**Promoted by:** — (none yet)

**Intent (§7, quoted):** *"a human_role/process blend: what moderation review, override, or
escalation occurred over a piece of content or an agent action, and whether the required
moderation step was followed. Buzz's own judgment source (fabric v3 §17, 'Mesh judgment
source')."*

**Profile:** `human_role` / `process` blend (Evidence Contract v3 §3.4, §3.6).

**Subject shape:**

Evidence Contract subject (population level; unchanged by this ruling):
```
subject:
  job_type: "buzz.moderation"
  population_selector: <host-defined — e.g. "moderation actions closed in evaluation_period">
```

EvidenceRecord subject (uniform, per the 2026-09-23 ruling — same two fields as Entry 2's). The
subject is the **moderation action event** itself:
```
subject:
  event_id: <Nostr event id of the moderation action event — transport reference, §14>
  semantic_digest: <semantic digest of the moderation action event's payload — content identity,
                    §14>
```

**Content vs. decision — two NAMED body digests, never subject fields.** A moderation record binds
*what was moderated* and *what was decided about it*. Neither gets a `subject` field or a renamed
`semantic_digest`; both are separate, NAMED digests in the record body's `payload_commitments`:
```
payload_commitments:
  - role: "moderated-content"     # digest of the moderated content — NEVER the content itself
    digest_alg: <...>
    digest: <...>
  - role: "moderation-decision"   # digest of the disposition-and-provenance payload
    digest_alg: <...>
    digest: <...>
judgment:
  disposition: "removed" | "labeled" | "no_action"
  evaluator_model_ref: <...>
  calibration_ref: <...>
```
Collapsing the content digest into `subject`, or the transport id into either digest, is exactly
the case that would also leak the moderated text through a mis-typed field; keeping every fact
named and distinct is what makes the "digests only" rule checkable. One worked vector
(`vectors/profiles/buzz.moderation/v1/positive-semantic-judgment.json` in `agent-action-capsule`)
carries all three: `subject.{event_id, semantic_digest}` for the moderation action, and the
`moderated-content` + `moderation-decision` body digests.

**Required epistemic types — the three-part evidentiary basis:**

A `buzz.moderation/v1` requirement's `accepted_epistemic_types` MUST include all three of:
1. **`SEMANTIC_JUDGMENT`** — the moderation determination itself (e.g. a disposition such as
   `removed` / `labeled` / `no_action`), carried with evaluator/model/version and calibration
   provenance per Evidence Contract v3 §3.6's rule for qualitative interpretation. Never the
   moderated content — the determination only, plus the `moderated-content` body digest it was
   made over.
2. **`HUMAN_REPORT`** (review) — a human reviewer's own report over the determination (Evidence
   Contract v3 §3.6's `review: { rate, events }` shape), typed `HUMAN_REPORT` per v2 §7 (carried
   forward, Contract v3 §10): human experience/judgment measures never get typed as anything
   stronger than the report they are.
3. **`OBLIGATION_REFERENCE`** — a reference into the obligation register row this moderation
   action evidences toward (see obligation refs below), never itself a compliance conclusion
   (Contract v3 §3.3, §9).

A record satisfying only one or two of the three types is `INSUFFICIENT` sufficiency for a
`buzz.moderation/v1` requirement that names all three as required — this profile's evidentiary
basis is the combination, not any single record.

```
evidence_requirements:
  accepted_epistemic_types: [SEMANTIC_JUDGMENT, HUMAN_REPORT, OBLIGATION_REFERENCE]
  required_sources: [buzz-moderation-judgment-record, buzz-moderator-review-record, obligation-register]
  minimum_assurance: [self-attested]   # UNRULED placeholder — to confirm
```

**Obligation refs — where real:** DSA Art. 17 (statement of reasons) and Art. 24(5) (transparency
database) — reported as evidence present / missing / insufficient, never "compliant".
```
obligation_refs:
  - "dsa:article-17"      # statement-of-reasons obligation for a content-moderation decision
  - "dsa:article-24-5"    # transparency-database reporting obligation
```
Per Evidence Contract v3 §9 (carried from v2 §6, unchanged): a `buzz.moderation/v1` result reports
that supporting evidence for either obligation reference is present, missing, insufficient,
contradicted, stale, or withheld. **It MUST NOT report either as "compliant."** This is a
restatement of an existing rule, not a new one this entry introduces.

### Entry 4 — `buzz.release/v1`

**Status:** subject shape ruled (uniform `semantic_digest`, 2026-09-23); would be `provisional`
once placed under a ruled section.
**Source:** Evidence Contract v3 §7 — not yet published.
**Promoted by:** — (none yet)

**Intent (§7, quoted):** *"an obligation/process blend: whether a required release-control step
(review, approval, staged rollout gate) was evidenced before a change went live. Same shape as the
dogfood change-control example in §2 [Appendix A.2 in the current draft], applied to a Buzz
release."*

**Profile:** `process` / `obligation` blend (Evidence Contract v3 §3.3, §3.4) — field shape mirrors
Appendix A.2's dogfood change-control example directly, substituting the Buzz release subject.

**Subject shape:**

Evidence Contract subject (population level; unchanged by this ruling):
```
subject:
  job_type: "buzz.release"
  population_selector: <host-defined — e.g. "releases shipped in evaluation_period">
```

EvidenceRecord subject (uniform, per the 2026-09-23 ruling — same two fields as Entries 2 and 3).
The release's separate approval record is a NAMED body digest (`payload_commitments[]` with
`role: "approval-record"`), not a second subject field:
```
subject:
  event_id: <Nostr event id of the release-gate event — transport reference, §14>
  semantic_digest: <semantic digest of the release-gate record — content identity, §14>
```

**Requirements (mirrors Appendix A.2's two-requirement shape):**
```
requirements:
  - id: req-process-1
    profile: process
    statement: "a required release-control step preceded the change going live"
    required_sequence: ["review-requested", "review-approved", "rolled-out"]
    approvals: ["at least one non-author reviewer"]
    evidence_requirements:
      accepted_epistemic_types: [OBSERVED_EVENT, SYSTEM_OF_RECORD_FACT]
      required_sources: [ buzz-release-gate-record ]
  - id: req-obligation-1
    profile: obligation
    statement: "the release-control policy's review-before-rollout control was evidenced"
    clause_ref: <host-defined release-control policy ref, e.g. "buzz-internal-release-policy/section-2/v1">
    evidence_requirements:
      accepted_epistemic_types: [OBSERVED_EVENT]
      required_sources: [ buzz-release-gate-record ]
    retention_check: "release-gate events retained for evaluation_period + P1Y"   # UNRULED placeholder value
```

**Obligation refs — where real:** unlike `buzz.moderation/v1`, no DSA article is named for
release-control in Evidence Contract v3 §7's intent paragraph. `clause_ref` above is a host-defined
internal release-control policy reference (mirroring Appendix A.2's
`internal-change-control-policy/section-3/v2`), not a named external regulatory obligation. If a
specific deployment has a real external obligation for release control, that reference is supplied
by that deployment, not invented here.

---

## CLL and composition drafts — no new relation

**No new relation is needed.** Checked against both:
- **CLL** (`checkpointed-local-log`): EvidenceBook v3 §6 states CLL "MUST NOT need to understand
  Evidence Contract, human reports, semantic judgments, attribution, settlement, or disclosure
  policy" and §7 states a host-principal binding does not change which CLL a record lands in
  (custody) versus which `principal_ref` it carries (identity) — the two stay independent, and
  neither the `nostr-pubkey` profile nor the three Buzz profiles above touch CLL's append/MMR/
  checkpoint/witness algorithms at all.
- **Composition** (`agent-accountability-composition`): checked directly against the WHO slot's
  named-human-authorization definition (see the placement note above) — `nostr-pubkey` is an
  identity binding, not a pre-execution authorization receipt, and the three Buzz profiles are
  Evidence Contract requirement profiles, not composition slots. No composition relation is
  extended or introduced by this draft.

No paragraph is added to either draft. If the placement ruling (above) later decides one
of these entries actually needs a composition or CLL relation, that is a change to this section on
re-draft, not a silent addition elsewhere.
