#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Regenerate registry/entries/examples/*/{positive,boundary,must-fail}.json
from the REAL upstream libraries (capsule-emit-mesh, capsule-emit,
agent-action-capsule), rather than hand-typing capsule JSON that might not
match production shape.

**Dev-time only -- NOT part of CI.** CI (.github/validate_registry_entries.py)
only re-verifies the already-committed example files against
agent-action-capsule; it does not regenerate them and does not depend on
capsule-emit-mesh or capsule-emit being importable at all. Re-run this
script by hand (and re-commit its output) when the source libraries'
schema-tagged shapes change.

Requires sibling checkouts, at the commits this repo's PROVENANCE.md
records, of:
  - agent-action-capsule  (python/ subdirectory on PYTHONPATH)
  - capsule-emit-mesh     (repo root on PYTHONPATH)
  - capsule-emit          (repo root on PYTHONPATH)

Usage (from a workspace with all four repos as siblings):
    PYTHONPATH=../agent-action-capsule/python:../capsule-emit:../capsule-emit-mesh \\
        python3 scripts/generate_examples.py
"""
from __future__ import annotations

import copy
import json
import pathlib
import tempfile

from agent_action_capsule.canonical import compute_capsule_id
from agent_action_capsule.verify import verify as verify_capsule

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
EXAMPLES_ROOT = REPO_ROOT / "registry" / "entries" / "examples"

# Fixed so regenerated fixtures are stable byte-for-byte modulo the upstream
# libraries' own non-determinism (uuid4 action_ids, ephemeral signing keys).
FIXED_TIMESTAMP = "2026-09-05T00:00:00Z"


def _write_example(name: str, case: str, kind: str, record: dict, *, schema_valid: bool, verify_ok: bool, notes: str) -> None:
    result = verify_capsule(record)
    assert result.ok == verify_ok, (
        f"{name}/{case}: agent-action-capsule verify returned ok={result.ok}, "
        f"expected {verify_ok} -- fix the generator or the declared expectation "
        f"before committing (findings: {[(f.severity, f.code, f.detail) for f in result.findings]})"
    )
    out_dir = EXAMPLES_ROOT / name
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": kind,
        "expected": {
            "record_schema_valid": schema_valid,
            "verify_ok": verify_ok,
            "notes": notes,
        },
        "record": record,
    }
    path = out_dir / f"{case}.json"
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(f"wrote {path}  (verify ok={result.ok}, {len(result.findings)} finding(s))")


def _stamp(cap: dict) -> dict:
    cap["timestamp"] = FIXED_TIMESTAMP
    cap["capsule_id"] = compute_capsule_id(cap)
    return cap


# ============================================================== mesh-join-card
def generate_mesh_join_card() -> None:
    from join_card import ModelRef, build_card, seal_card

    card_pos = build_card(
        node_id="mesh-node-demo-1",
        hardware_inventory={
            "source": "os_reported", "capture_method": "system_profiler",
            "grade": "os_measured", "chip": "Apple M4 Max", "memory_bytes": 42_949_672_960,
        },
        models=[ModelRef(name="meta/Llama-3.2-3B", weights_digest="a" * 64)],
        measurement_rung="os_measured",
        announcement_digest="d" * 64,
    )
    cap_pos = _stamp(seal_card(card_pos, operator="op", developer="dev", signing_node_id="mesh-node-demo-1"))
    _write_example(
        "mesh-join-card", "positive", "positive", cap_pos,
        schema_valid=True, verify_ok=True,
        notes="Node join card with one served model at os_measured rung; validates and grades ok.",
    )

    card_bnd = build_card(
        node_id="mesh-node-demo-2",
        hardware_inventory={
            "source": "os_reported", "capture_method": "system_profiler",
            "grade": "reported", "chip": "unknown", "memory_bytes": 0,
        },
        models=[],
        measurement_rung="reported",
        announcement_digest="e" * 64,
    )
    cap_bnd = _stamp(seal_card(card_bnd, operator="op", developer="dev", signing_node_id="mesh-node-demo-2"))
    _write_example(
        "mesh-join-card", "boundary", "boundary", cap_bnd,
        schema_valid=True, verify_ok=True,
        notes="Node with an empty served-model list at the lowest measurement rung (reported) -- an honest not-yet-serving node, not an error.",
    )

    cap_bad = copy.deepcopy(cap_pos)
    subject = cap_bad["model_attestation"]["compute_attestation"]["x-mesh-join-card-v1"]["card"]
    del subject["hardware_inventory"]["chip"]
    subject["measurement_rung"] = "trust-me-bro"
    cap_bad["capsule_id"] = compute_capsule_id(cap_bad)
    _write_example(
        "mesh-join-card", "must-fail", "must_fail", cap_bad,
        schema_valid=False, verify_ok=True,
        notes=(
            "hardware_inventory.chip missing (required by the entry's schema) and "
            "measurement_rung set to an unregistered token -- MUST fail record-schema "
            "validation. AAC's generic capsule verify still reports ok=true (card content "
            "is Home-2 semantics, invisible to Home-1's mechanics), which is exactly why "
            "this registry entry's own schema has to catch it."
        ),
    )


# =========================================================== mesh-history-card
def generate_mesh_history_card() -> None:
    import checkpointing
    from capsule_emit.checkpoint import CheckpointConfig, WitnessRecord
    from checkpointing import CheckpointState, Ed25519Signer, JsonlLogSource
    from history_card import build_history_card, seal_history_card

    calls = []

    def _fake_register_checkpoint(checkpoint_cose, ts_url, *, timeout=30.0):
        calls.append((checkpoint_cose, ts_url))
        return WitnessRecord(
            ts_url=ts_url, entry_hash=f"fake-entry-hash-{len(calls)}",
            receipt_b64="ZmFrZS1yZWNlaXB0", leaf_index=len(calls) - 1, tree_size=len(calls),
        )

    checkpointing.register_checkpoint = _fake_register_checkpoint

    tmp = pathlib.Path(tempfile.mkdtemp())
    log = JsonlLogSource(tmp / "capsules.jsonl")
    cfg = CheckpointConfig(cadence_entries=2, max_lag_entries=10_000, ts_urls=["https://fake-ts.example"])
    signer = Ed25519Signer(tmp / "node-a.pem")
    state = CheckpointState.load(ledger_dir=tmp, log_source=log, cfg=cfg, signer=signer, log_id="log-demo-1")
    n = made = 0
    while made < 3:
        log.append({"capsule_id": f"{n:064x}", "n": n})
        n += 1
        if state.record_appended() is not None:
            made += 1
    lines = [json.loads(l) for l in (tmp / "checkpoints.jsonl").read_text().splitlines()]

    # since_size pinned to the SECOND checkpoint's own mmr_size, leaving
    # exactly ONE checkpoint in range -- a real >=2-checkpoint range's cadence
    # stats include real-valued span/interval seconds (floats), which trips
    # agent_action_capsule.canonical.FloatInDigestError once digest-bearing
    # (see mesh-history-card.yaml's open_questions -- a capsule-emit-mesh bug,
    # out of scope here). A single-checkpoint cadence is int-only
    # ({"checkpoints": N}), avoiding the bug while still producing a REAL,
    # non-empty positive example.
    card_pos = build_history_card(
        node_id="mesh-node-demo-1", log_id="log-demo-1",
        checkpoint_lines=lines, since_size=lines[1]["mmr_size"],
    )
    cap_pos = _stamp(seal_history_card(card_pos, operator="op", developer="dev", signing_node_id="mesh-node-demo-1"))
    _write_example(
        "mesh-history-card", "positive", "positive", cap_pos,
        schema_valid=True, verify_ok=True,
        notes="A one-checkpoint chain segment since a prior pin, unbroken continuity, witnessed -- validates and grades ok.",
    )

    card_bnd = build_history_card(node_id="mesh-node-demo-2", log_id="log-demo-2", checkpoint_lines=[], since_size=0)
    cap_bnd = _stamp(seal_history_card(card_bnd, operator="op", developer="dev", signing_node_id="mesh-node-demo-2"))
    _write_example(
        "mesh-history-card", "boundary", "boundary", cap_bnd,
        schema_valid=True, verify_ok=True,
        notes="Honestly-empty card: no checkpoints exist yet since the requested size. continuity/unforked still hold meaningful values (never null/omitted) for a log with no history yet.",
    )

    cap_bad = copy.deepcopy(cap_pos)
    subj = cap_bad["model_attestation"]["compute_attestation"]["x-mesh-history-v1"]["history"]
    subj["coverage"]["checkpoint_count"] = -1
    subj["derivation"]["properties"]["unforked"] = "yes"
    cap_bad["capsule_id"] = compute_capsule_id(cap_bad)
    _write_example(
        "mesh-history-card", "must-fail", "must_fail", cap_bad,
        schema_valid=False, verify_ok=True,
        notes="coverage.checkpoint_count is negative and derivation.properties.unforked is a string instead of a boolean -- MUST fail record-schema validation. AAC's generic verify still reports ok=true.",
    )


# ================================================================ adjudication
def generate_adjudication_verdict() -> None:
    from capsule_emit.adjudication import VERDICT_CORROBORATED, VERDICT_INCONCLUSIVE, seal_adjudication

    def _sealed(ledger_path: str, **kwargs) -> dict:
        open(ledger_path, "w").close()
        cap = seal_adjudication(ledger=ledger_path, operator="op", developer="dev", **kwargs).capsule
        cap["timestamp"] = FIXED_TIMESTAMP
        # Recompute over the post-stamp body, then drop signature/key_id: the
        # original signature was over the pre-stamp timestamp and would no
        # longer verify. AAC's Class-1 verify does not require a present
        # signature for a standalone/self_attested capsule, so ok stays true.
        cap["capsule_id"] = compute_capsule_id({k: v for k, v in cap.items() if k not in ("signature", "key_id")})
        cap.pop("signature", None)
        cap.pop("key_id", None)
        return cap

    cap_pos = _sealed(
        "/tmp/capsule-registry-adj-ledger-positive.jsonl",
        half_a_capsule_id="a" * 64, half_b_capsule_id="b" * 64,
        verdict=VERDICT_CORROBORATED, margin=1.0, margin_tau=0.9,
        divergence_index=None, twin_owner_distinct=True, weights_digest="c" * 64,
    )
    _write_example(
        "adjudication-verdict", "positive", "positive", cap_pos,
        schema_valid=True, verify_ok=True,
        notes="verdict=corroborated over two distinct-owner twin halves -- validates and grades ok.",
    )

    cap_bnd = _sealed(
        "/tmp/capsule-registry-adj-ledger-boundary.jsonl",
        half_a_capsule_id="d" * 64, half_b_capsule_id="e" * 64,
        verdict=VERDICT_INCONCLUSIVE, margin=0.42, margin_tau=0.9,
        divergence_index=17, twin_owner_distinct=None, weights_digest=None,
    )
    _write_example(
        "adjudication-verdict", "boundary", "boundary", cap_bnd,
        schema_valid=True, verify_ok=True,
        notes="verdict=inconclusive with weights_digest honestly absent (stubbed pending [E5], never fabricated as a placeholder) -- the boundary the verdict enum's third shape exists for.",
    )

    cap_bad = copy.deepcopy(cap_pos)
    cap_bad["model_attestation"]["compute_attestation"]["adjudication"]["verdict"] = "probably"
    cap_bad["capsule_id"] = compute_capsule_id(cap_bad)
    _write_example(
        "adjudication-verdict", "must-fail", "must_fail", cap_bad,
        schema_valid=False, verify_ok=True,
        notes=(
            "verdict='probably' is outside the closed set {corroborated, inconclusive, "
            "contradicted:<owner_id>} -- MUST fail record-schema validation. The real "
            "seal_adjudication() helper refuses this at call time (_validate_verdict); "
            "this example simulates a non-conforming producer that bypassed it, which is "
            "exactly the case this registry entry's schema exists to catch downstream."
        ),
    )


if __name__ == "__main__":
    generate_mesh_join_card()
    generate_mesh_history_card()
    generate_adjudication_verdict()
