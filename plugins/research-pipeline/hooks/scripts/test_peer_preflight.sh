#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

mkdir -p "$tmp_dir/bin" "$tmp_dir/home/.codex" "$tmp_dir/home/.claude"

cat > "$tmp_dir/home/.codex/config.toml" <<'EOF'
[plugins."peeragent@test"]
enabled = true
EOF

cat > "$tmp_dir/home/.claude/settings.json" <<'EOF'
{"enabledPlugins":{"peeragent@test":true}}
EOF

run_hook() {
  payload=$1
  HOME="$tmp_dir/home" PATH="$tmp_dir/bin:/usr/bin:/bin" \
    sh "$script_dir/session-start-peer-preflight.sh" <<EOF
$payload
EOF
}

# Unknown host and an installation without peeragent are silent.
test -z "$(run_hook '{"hook_event_name":"SessionStart"}')"
mv "$tmp_dir/home/.codex/config.toml" "$tmp_dir/home/.codex/config.disabled"
test -z "$(run_hook '{"model":"gpt-5.6-sol","hook_event_name":"SessionStart"}')"
mv "$tmp_dir/home/.codex/config.disabled" "$tmp_dir/home/.codex/config.toml"

# Codex host selects Claude and reports a missing CLI.
output=$(run_hook '{"model":"gpt-5.6-sol","hook_event_name":"SessionStart"}')
printf '%s' "$output" | grep -q "Claude is the configured cross-model peer"
printf '%s' "$output" | grep -q "'claude' is not on PATH"

cat > "$tmp_dir/bin/claude" <<'EOF'
#!/bin/sh
test "${1:-}" = auth && test "${2:-}" = status && exit "${CLAUDE_AUTH_EXIT:-0}"
exit 2
EOF
chmod +x "$tmp_dir/bin/claude"

# A ready Claude peer is silent; a failed auth probe is actionable.
test -z "$(run_hook '{"model":"gpt-5.6-sol","hook_event_name":"SessionStart"}')"
output=$(CLAUDE_AUTH_EXIT=1 run_hook '{"model":"gpt-5.6-sol","hook_event_name":"SessionStart"}')
printf '%s' "$output" | grep -q "Claude NOT authenticated"
printf '%s' "$output" | grep -q "claude auth login"

# Claude host reports a missing Codex CLI.
output=$(run_hook '{"model":"claude-fable-5","hook_event_name":"SessionStart"}')
printf '%s' "$output" | grep -q "Codex is the configured cross-model peer"
printf '%s' "$output" | grep -q "'codex' is not on PATH"

# Claude host selects Codex, including transcript-path fallback detection.
cat > "$tmp_dir/bin/codex" <<'EOF'
#!/bin/sh
test "${1:-}" = login && test "${2:-}" = status && exit "${CODEX_AUTH_EXIT:-0}"
exit 2
EOF
chmod +x "$tmp_dir/bin/codex"

test -z "$(run_hook '{"model":"claude-fable-5","hook_event_name":"SessionStart"}')"
output=$(CODEX_AUTH_EXIT=1 run_hook '{"transcript_path":"/tmp/.claude/session.jsonl","hook_event_name":"SessionStart"}')
printf '%s' "$output" | grep -q "Codex NOT authenticated"
printf '%s' "$output" | grep -q "codex login"

# Codex transcript-path fallback selects Claude too.
test -z "$(run_hook '{"transcript_path":"/tmp/.codex/session.jsonl","hook_event_name":"SessionStart"}')"

printf '%s\n' 'peer preflight: ok'
