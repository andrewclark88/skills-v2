#!/bin/sh
set -eu

# Resolve the companion plugin without assuming that plugin caches share a
# version directory. An explicit root always wins; source checkouts use the
# sibling plugin; installed hosts fall back to a bounded cache search.

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
pipeline_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

is_agentic_root() {
  candidate=$1
  test -f "$candidate/ard-core/kernel/lint-citations.py" &&
    test -f "$candidate/.claude-plugin/plugin.json"
}

if test -n "${AGENTIC_RESEARCH_PLUGIN_ROOT:-}"; then
  if is_agentic_root "$AGENTIC_RESEARCH_PLUGIN_ROOT"; then
    printf '%s\n' "$AGENTIC_RESEARCH_PLUGIN_ROOT"
    exit 0
  fi
  printf '%s\n' "AGENTIC_RESEARCH_PLUGIN_ROOT does not identify an agentic-research plugin: $AGENTIC_RESEARCH_PLUGIN_ROOT" >&2
  exit 2
fi

sibling_root=$(CDPATH= cd -- "$pipeline_root/.." && pwd)/agentic-research
if is_agentic_root "$sibling_root"; then
  printf '%s\n' "$sibling_root"
  exit 0
fi

search_roots=""
for root in \
  "${CLAUDE_PLUGIN_CACHE_DIR:-}" \
  "${CODEX_PLUGIN_CACHE_DIR:-}" \
  "${HOME:-}/.claude/plugins/cache" \
  "${HOME:-}/.codex/plugins"; do
  if test -n "$root" && test -d "$root"; then
    search_roots="$search_roots
$root"
  fi
done

match=""
old_ifs=$IFS
IFS='
'
for root in $search_roots; do
  candidate=$(find "$root" -maxdepth 7 -type f \
    \( -path '*/agentic-research/ard-core/kernel/lint-citations.py' \
       -o -path '*/agentic-research/*/ard-core/kernel/lint-citations.py' \) \
    -print 2>/dev/null | LC_ALL=C sort | tail -n 1 || true)
  if test -n "$candidate"; then
    candidate=${candidate%/ard-core/kernel/lint-citations.py}
    if is_agentic_root "$candidate"; then
      match=$candidate
    fi
  fi
done
IFS=$old_ifs

if test -n "$match"; then
  printf '%s\n' "$match"
  exit 0
fi

printf '%s\n' "agentic-research is required but could not be resolved." >&2
printf '%s\n' "Install and enable agentic-research, or set AGENTIC_RESEARCH_PLUGIN_ROOT to its plugin directory." >&2
exit 2
