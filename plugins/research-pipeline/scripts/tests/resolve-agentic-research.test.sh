#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
resolver=$script_dir/../resolve-agentic-research.sh
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

make_plugin() {
  root=$1
  mkdir -p "$root/ard-core/kernel" "$root/.claude-plugin"
  : > "$root/ard-core/kernel/lint-citations.py"
  printf '%s\n' '{"name":"agentic-research"}' > "$root/.claude-plugin/plugin.json"
}

explicit_root=$tmp_dir/explicit
make_plugin "$explicit_root"
actual=$(AGENTIC_RESEARCH_PLUGIN_ROOT=$explicit_root "$resolver")
test "$actual" = "$explicit_root"

cache_root=$tmp_dir/cache
cached_plugin=$cache_root/market/agentic-research/0.6.5
make_plugin "$cached_plugin"
isolated_resolver=$tmp_dir/installed/research-pipeline/scripts/resolve-agentic-research.sh
mkdir -p "$(dirname "$isolated_resolver")"
cp "$resolver" "$isolated_resolver"
chmod +x "$isolated_resolver"
actual=$(env -u AGENTIC_RESEARCH_PLUGIN_ROOT \
  CLAUDE_PLUGIN_CACHE_DIR=$cache_root \
  CODEX_PLUGIN_CACHE_DIR=$tmp_dir/missing \
  HOME=$tmp_dir/home "$isolated_resolver")
test "$actual" = "$cached_plugin"

if AGENTIC_RESEARCH_PLUGIN_ROOT=$tmp_dir/missing "$resolver" >/dev/null 2>&1; then
  printf '%s\n' 'expected invalid explicit root to fail' >&2
  exit 1
fi

printf '%s\n' 'resolve-agentic-research: ok'
