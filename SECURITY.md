# Security policy

## Reporting a vulnerability

Please report suspected vulnerabilities **privately**:

- **GitHub:** use *Security → Report a vulnerability* on this repository
  (GitHub private vulnerability reporting), or
- **Email:** security@actionstate.ai with `[capsule-registry security]` in the
  subject.

Please do not open a public issue for a suspected vulnerability. We aim to
acknowledge reports within 72 hours.

## Scope (highest-priority classes)

- **CI secret exposure.** The neutrality gate (`.github/workflows/neutrality.yml`)
  runs under `pull_request_target` specifically so it can see the
  `NEUTRALITY_TERMS` secret on fork PRs. Any change that causes a step to
  execute, build, install, or source content from a pull request's own
  files is the **highest-priority** issue — see the warning block in that
  workflow file before proposing changes to it.
- **Neutrality-gate bypass.** Content that carries reserved vocabulary but
  is not flagged by the scan (`.github/neutrality_scan.py`) — an encoding,
  file-type, or allow-phrase-span gap that lets reserved terms land on
  `main`.
- **Registration-authority confusion.** Any change that makes a promotion
  read as ruled on by an individual rather than the Registry Editor role
  stated in `REGISTRATION-POLICY.md`, or that misstates the change
  controller.
- **Digest Context restatement.** An entry that duplicates a Home-1
  (`scitt-payload-binding`) Digest Context table here instead of citing it —
  not a memory-safety issue, but a correctness regression this registry
  exists to prevent (two copies of the same mechanical fact can drift).

## Out of scope

This repository holds no running service and no keys — it is documents plus
CI. Vulnerabilities in the Agent Action Capsule reference implementation or
the SCITT anchor service belong in
[`agent-action-capsule`](https://github.com/action-state-group/agent-action-capsule)
or
[`capsule-anchor`](https://github.com/action-state-group/capsule-anchor)
respectively. Ambiguities or honest-but-misleading prose about standards
status are not security issues — raise those as public issues.

## Supported versions

The latest state of `main` receives fixes; there are no released versions.
