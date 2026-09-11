# Contributing to capsule-registry

`capsule-registry` is the **Home-2 semantics registry** for the Agent Action
Capsule (AAC) ecosystem — the record of what capsule fields and conventions
*mean*, as against
[`scitt-payload-binding`](https://github.com/action-state-group/scitt-payload-binding)
(Home-1), which records how bytes are canonicalized and digested.
Contributions are welcome.

## License (Apache-2.0)

All contributions are licensed under the **Apache License 2.0** (see `LICENSE`).

### Developer Certificate of Origin (DCO)

This project uses the [Developer Certificate of Origin 1.1](https://developercertificate.org/).
Sign off every commit:

```bash
git commit -s -m "your message"
```

No CLA is required — the DCO is the whole agreement.

## How an entry is proposed

An entry moves from `provisional` to `promoted` under
[`REGISTRATION-POLICY.md`](REGISTRATION-POLICY.md). To propose one:

1. Open a pull request against the relevant reserved section in
   [`REGISTRY.md`](REGISTRY.md), following the within-entry format stated
   there.
2. **The pull request is the consent record.** Opening it, and any
   subsequent commit to it, is the proposer's record of agreeing to this
   entry's text under the license above — there is no separate sign-off
   form.
3. **Cite Home-1, never restate it.** If the entry has a mechanical
   counterpart already registered or provisional in CPB's registries
   (`scitt-payload-binding`), the pull request MUST cite that entry by
   reference for its Digest Context table (algorithm, field set, exclusion
   set, domain separation, pre-image encoding, representation). Reproducing
   that table here, even partially, is out of scope for this repository —
   fix it by linking to Home-1 instead.
4. A pull request proposing more than one entry gets more than one
   promotion ruling — see the per-entry rule in `REGISTRATION-POLICY.md`.

## Scope discipline (review gates, not preferences)

1. **Semantics only.** This registry never records algorithms, digest
   contexts, or canonicalization profiles — that is Home-1's registry, in
   `scitt-payload-binding`. A PR that adds mechanical content belongs there,
   not here.
2. **Product-free.** This registry carries composition and semantic
   vocabulary only — nothing tenant-specific, billing-specific, or internal
   to a downstream product.
3. **Neutrality is enforced.** A CI gate scans every PR for a
   reserved-vocabulary set (held in a repo secret, not listed here). Keep
   contributions vendor-neutral.
4. **No entries migrate without a per-entry ruling.** An entry that
   currently incubates whole in CPB's provisional registry
   (`scitt-payload-binding/spec/cpb-provisional-registry.md`) stays there
   until it receives its own promotion ruling — a PR that splits it
   preemptively will be declined.

## Where discussion happens

Open an issue or PR on this repository for registry-specific questions. The
underlying Agent Action Capsule profile is discussed against
[`agent-action-capsule`](https://github.com/action-state-group/agent-action-capsule)
and, for the SCITT/COSE substrate, the IETF **SCITT** Working Group
(`scitt@ietf.org`).
