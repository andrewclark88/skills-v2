#!/usr/bin/env bash
# SessionStart hook: print a COMPACT .work/ substrate snapshot (counts + top-N ids).
#
# Why this exists (fork divergence, intentional): upstream agile-workflow stopped
# emitting a queue snapshot at session start in the 0.11.3 sync — its SessionStart
# hook (prompt-context.py) moved queue state to explicit `work-view`/`board` calls.
# This research-pipeline hook restores a compact session-start snapshot so the
# substrate's current queue surfaces passively, matching the build-process
# "session start" contract. The DRAINING skills (autopilot, implement-orchestrator,
# release-deploy) never depended on this; it is purely for passive awareness.
#
# Budget: the harness inlines hook output up to ~10,000 characters PER HOOK. This is
# a SEPARATE SessionStart hook from session-start-nav.sh, so it has its OWN budget —
# the (often near-cap) knowledge-index navigator does not compete with it. It also
# stays intrinsically tiny: counts + at most 5 ids per bucket, hard-capped at the end.
#
# Robustness: a SessionStart hook must NEVER break the session. No `set -e`; every
# external call is guarded; the script always exits 0 (and prints nothing when there
# is no substrate or the substrate is empty).

input="$(cat 2>/dev/null || true)"

# --- locate the hook cwd from the payload (mirrors session-start-nav.sh) ---
hook_cwd=""
if command -v jq >/dev/null 2>&1 && [ -n "$input" ]; then
  hook_cwd="$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null || true)"
elif [ -n "$input" ]; then
  hook_cwd="$(printf '%s' "$input" \
    | grep -o '"cwd"[[:space:]]*:[[:space:]]*"[^"]*"' \
    | head -1 \
    | sed 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' || true)"
fi

# --- walk up to the substrate root (.work/CONVENTIONS.md), like the agile-workflow hook ---
dir="${hook_cwd:-${CLAUDE_PROJECT_DIR:-$PWD}}"
root=""
while [ -n "$dir" ] && [ "$dir" != "/" ]; do
  if [ -f "$dir/.work/CONVENTIONS.md" ]; then root="$dir"; break; fi
  dir="$(dirname "$dir")"
done
[ -n "$root" ] || exit 0

wv="$root/.work/bin/work-view"
[ -x "$wv" ] || exit 0   # no queryable tool → stay silent rather than guess

# --- gather (guarded; one work-view call per active bucket, filesystem for backlog) ---
ready_paths="$(cd "$root" 2>/dev/null && "$wv" --ready --paths 2>/dev/null || true)"
review_paths="$(cd "$root" 2>/dev/null && "$wv" --stage review --paths 2>/dev/null || true)"
blocked_n="$(cd "$root" 2>/dev/null && "$wv" --blocked --count 2>/dev/null | tr -dc '0-9' || true)"; blocked_n="${blocked_n:-0}"
backlog_paths="$(ls "$root"/.work/backlog/*.md 2>/dev/null || true)"

nlines()  { printf '%s' "$1" | grep -c . 2>/dev/null || true; }   # grep -c prints 0 AND exits 1 on no-match; || true (NOT || echo 0, which double-prints)
top5ids() { printf '%s\n' "$1" | sed 's#.*/##; s#\.md$##' | head -5 | paste -sd, - 2>/dev/null || true; }

ready_n="$(nlines "$ready_paths")"
review_n="$(nlines "$review_paths")"
backlog_n="$(nlines "$backlog_paths")"

# nothing tracked → silent (don't clutter session start with an empty substrate)
[ "$(( ready_n + blocked_n + review_n + backlog_n ))" -gt 0 ] || exit 0

ready_ids="$(top5ids "$ready_paths")"
review_ids="$(top5ids "$review_paths")"
backlog_ids="$(top5ids "$backlog_paths")"

{
  echo "=== Work substrate (.work/) — passive snapshot; query with .work/bin/work-view ==="
  echo "ready: ${ready_n} · blocked: ${blocked_n} · at-review: ${review_n} · backlog: ${backlog_n}"
  [ -n "$ready_ids" ]   && echo "ready:       ${ready_ids}"
  [ -n "$review_ids" ]  && echo "at-review:   ${review_ids}"
  [ -n "$backlog_ids" ] && echo "backlog:     ${backlog_ids}"
  echo "(detail: work-view --ready | --blocked | --stage review | --cat <id>; >5 per bucket truncated)"
  echo "=== END substrate ==="
} | head -c 1800   # paranoia cap; content is already bounded to <=5 ids/bucket

exit 0
