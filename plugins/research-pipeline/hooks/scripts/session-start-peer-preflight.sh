#!/usr/bin/env bash
# SessionStart hook: cross-model peer-review preflight.
#
# The agile-workflow + research-pipeline skills (autopilot, epic-design,
# feature-design, review/deep-review, perf-scout, principles) use peeragent to
# run a *cross-model* peer-review pass — but only "when a different model class
# is available." Their availability check is just `command -v peeragent`; none
# of them verify that the peer CLI is actually authenticated. So if Codex isn't
# logged in, the peeragent call fails mid-run and the skills' "non-blocking
# advisory" escape hatch SILENTLY falls back to same-model local review.
#
# This hook surfaces that state at session start so a logged-out Codex is loud,
# not silent. Stays quiet in the happy path (logged in) and inert where the
# peer mechanism isn't installed.
set -euo pipefail

# Only relevant if the peer mechanism is present. No peeragent → nothing to warn about.
command -v peeragent >/dev/null 2>&1 || exit 0

# peeragent installed but no codex CLI: cross-model peer (the default --agent) can't run.
if ! command -v codex >/dev/null 2>&1; then
  echo "=== ⚠️  peer-review preflight ==="
  echo "peeragent is installed but the 'codex' CLI is not on PATH. The workflow's"
  echo "cross-model peer-review will fall back to same-model local review."
  echo "Fix: install Codex (https://github.com/openai/codex) — or set a different"
  echo "default peer (gemini/claude) if that's intended."
  echo "=== END peer-review preflight ==="
  exit 0
fi

# codex present — is it authenticated? `codex login status` exits 0 when logged in.
if codex login status >/dev/null 2>&1; then
  exit 0  # logged in: silent happy path
fi

echo "=== ⚠️  peer-review preflight: Codex NOT authenticated ==="
echo "Cross-model peer-review (autopilot, epic-design, feature-design, review,"
echo "perf-scout — all delegate to 'peeragent --agent codex') will SILENTLY fall"
echo "back to same-model local review until you log in. The skills treat the"
echo "missing peer as a non-blocking advisory skip, so you won't be prompted later."
echo ""
echo "Fix before relying on peer-review:  codex login"
echo "=== END peer-review preflight ==="
exit 0
