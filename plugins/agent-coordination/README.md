# agent-coordination

A sparse cross-agent coordination ledger for shared repositories. It defines
deliberate claim, handoff, blocker, review, and merge-summary events without
turning coordination into a second issue tracker.

## Install

```bash
# Claude Code
/plugin marketplace add nklisch/skills
/plugin install agent-coordination@nklisch-skills

# OpenAI Codex
codex plugin marketplace add https://github.com/nklisch/skills
codex plugin install agent-coordination

# Pi (via the pi-plugins manager)
pi install npm:@nklisch/pi-plugins
# then, inside Pi:
/plugins marketplace add nklisch/skills
/plugins add agent-coordination@nklisch-skills --scope user
```

This package contains portable skills only; it has no runtime extension.

## License

MIT
