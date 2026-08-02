#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
plugin_root=$(CDPATH= cd -- "$script_dir/../.." && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

mkdir -p "$tmp_dir/project/docs"
printf '%s\n' 'total_docs: 3' > "$tmp_dir/project/docs/knowledge-index-nav.yaml"

payload=$(printf '{"cwd":"%s/project","hook_event_name":"SessionStart"}' "$tmp_dir")
output=$(printf '%s' "$payload" | "$script_dir/session-start-nav.sh")
printf '%s' "$output" | grep -q 'total_docs: 3'

# Missing indexes are deliberately silent.
mkdir -p "$tmp_dir/empty"
payload=$(printf '{"cwd":"%s/empty","hook_event_name":"SessionStart"}' "$tmp_dir")
output=$(printf '%s' "$payload" | "$script_dir/session-start-nav.sh")
test -z "$output"

# Oversized navigators produce a pointer rather than truncated YAML.
dd if=/dev/zero bs=10000 count=1 2>/dev/null | tr '\0' x > "$tmp_dir/project/docs/knowledge-index-nav.yaml"
payload=$(printf '{"cwd":"%s/project","hook_event_name":"PostCompact"}' "$tmp_dir")
output=$(printf '%s' "$payload" | "$script_dir/session-start-nav.sh")
printf '%s' "$output" | grep -q 'above the safe inline budget'
if printf '%s' "$output" | grep -q 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'; then
  printf '%s\n' 'oversized navigator content was inlined' >&2
  exit 1
fi

# The manifest must wire reorientation on both startup and compaction.
python3 - "$plugin_root/hooks/hooks.json" <<'PY'
import json, sys
hooks = json.load(open(sys.argv[1], encoding="utf-8"))["hooks"]
assert "SessionStart" in hooks
assert "PostCompact" in hooks
post = hooks["PostCompact"][0]
assert post["matcher"] == "manual|auto"
commands = [h["command"] for h in post["hooks"]]
assert any("session-start-nav.sh" in c for c in commands)
assert any("session-start-substrate.sh" in c for c in commands)
PY

printf '%s\n' 'session-context hooks: ok'
