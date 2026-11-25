#!/usr/bin/env bash
# Local check run before every push: the commands the pull_request and main CI jobs run.
# Not run here: dco (commit sign-off) and the neutrality term scan, which needs the
# NEUTRALITY_TERMS secret; the scanner's self-test runs.
set -euo pipefail
cd "$(dirname "$0")/.."

# leak-lint.yml
python3 .github/leak_lint.py .
# neutrality.yml
python3 .github/neutrality_scan.py --self-test
