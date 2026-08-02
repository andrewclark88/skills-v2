#!/usr/bin/env bash
# SessionStart hook: warn when the configured cross-model peer cannot run.
#
# Peer review is host-relative: Claude drives Codex, and Codex drives Claude.
# Detect the invoking host from the hook payload and fail open when it cannot be
# identified. The hook is advisory and must never block session startup.

set -u

input="$(cat 2>/dev/null || true)"

json_field() {
  local field="$1"
  if command -v jq >/dev/null 2>&1 && [[ -n "$input" ]]; then
    printf '%s' "$input" | jq -r ".${field} // empty" 2>/dev/null || true
  elif [[ -n "$input" ]]; then
    printf '%s' "$input" \
      | grep -o "\"${field}\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" \
      | head -1 \
      | sed "s/.*\"${field}\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/" \
      || true
  fi
}

model="$(json_field model)"
transcript_path="$(json_field transcript_path)"
host=""

case "$model" in
  claude-*) host="claude" ;;
  gpt-*|codex*|luna|terra|sol) host="codex" ;;
esac

if [[ -z "$host" ]]; then
  case "$transcript_path" in
    */.claude/*) host="claude" ;;
    */.codex/*) host="codex" ;;
  esac
fi

# An unknown host is not evidence of a broken peer setup.
[[ -n "$host" ]] || exit 0

peeragent_enabled() {
  if [[ -n "${PEERAGENT_BIN:-}" && -x "${PEERAGENT_BIN}" ]]; then
    return 0
  fi
  command -v peeragent >/dev/null 2>&1 && return 0

  if [[ "$host" == "codex" && -f "${HOME}/.codex/config.toml" ]]; then
    grep -A2 -E '^\[plugins\."peeragent@' "${HOME}/.codex/config.toml" 2>/dev/null \
      | grep -q '^enabled[[:space:]]*=[[:space:]]*true' && return 0
  fi

  if [[ "$host" == "claude" && -f "${HOME}/.claude/settings.json" ]]; then
    grep -Eq '"peeragent@[^\"]+"[[:space:]]*:[[:space:]]*true' \
      "${HOME}/.claude/settings.json" 2>/dev/null && return 0
  fi

  return 1
}

# Research Pipeline can run without peeragent; stay silent in that configuration.
peeragent_enabled || exit 0

if [[ "$host" == "claude" ]]; then
  peer_name="Codex"
  peer_cli="codex"
  auth_hint="codex login"
else
  peer_name="Claude"
  peer_cli="claude"
  auth_hint="claude auth login"
fi

if ! command -v "$peer_cli" >/dev/null 2>&1; then
  echo "=== ⚠️  peer-review preflight ==="
  echo "${peer_name} is the configured cross-model peer for this ${host} session,"
  echo "but '${peer_cli}' is not on PATH. The active workflow will apply its"
  echo "documented no-peer fallback. Install ${peer_name} or select another peer class."
  echo "=== END peer-review preflight ==="
  exit 0
fi

if [[ "$peer_cli" == "codex" ]]; then
  "$peer_cli" login status >/dev/null 2>&1 && exit 0
else
  "$peer_cli" auth status >/dev/null 2>&1 && exit 0
fi

echo "=== ⚠️  peer-review preflight: ${peer_name} NOT authenticated ==="
echo "${peer_name} is the configured cross-model peer for this ${host} session,"
echo "but its subscription-backed CLI is not authenticated. The active workflow"
echo "will apply its documented no-peer fallback until authentication succeeds."
echo ""
echo "Fix before relying on peer review:  ${auth_hint}"
echo "=== END peer-review preflight ==="
exit 0
