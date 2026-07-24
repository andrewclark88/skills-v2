# Workbench

A compact requirements-first delivery and grounded-research plugin for Claude
Code, OpenAI Codex, and Pi.

## Skills

| Skill | Purpose |
|---|---|
| `setup` | Convert any repository into one clean Workbench state and align conventions with the user. |
| `work` | Scope and drive a clear outcome, one epic, or several epics through verified completion. |
| `ideate` | Collaboratively clarify an uncertain direction before creating project state. |
| `park` | Preserve useful out-of-scope context in the backlog. |
| `release` | Collapse completed outcome stubs into a release summary; it does not publish or deploy. |
| `research` | Produce externally sourced, attested research and a deterministic knowledge index. |
| `research-handoff` | Propose research-grounded work and emit only items the user confirms. |

## Core behavior

- Natural language is the workflow surface; Workbench has no mandatory stages.
- Human requirements gathering remains explicit. Ambiguous outcomes may route
  through `ideate`; ordinary scoping stays in `work`.
- Work may carry one or multiple epics to the requested finish line.
- Useful findings outside the current scope are parked instead of silently
  expanding delivery.
- Testing focuses on meaningful behavior, contracts, boundaries, risks, and
  regressions. Tests must earn their maintenance cost.
- Cleanup and refactors are ordinary feature or story outcomes tagged
  `cleanup` or `refactor`; behavior changes are not hidden inside refactors.
- Root and sub-project foundations may live in `docs/`, `docs/<sub-project>/`,
  or `<sub-project>/docs/` according to repository convention.
- Research attestations ground externally fetched sources. Repository files are
  project context, not external source attestations.
- Setup removes superseded workflow files after verified conversion and leaves
  one clean final state.

Workbench and `agile-workflow` use mutually exclusive `.work/` schemas.

## Installation

```bash
# Claude Code
/plugin marketplace add nklisch/skills
/plugin install workbench@nklisch-skills

# OpenAI Codex
codex plugin marketplace add https://github.com/nklisch/skills
codex plugin install workbench

# Pi
pi install npm:@nklisch/pi-workbench
```

Start with `/workbench:setup`, or use `ideate` first when the intended project
or outcome is still unclear.
