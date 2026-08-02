# skills-v2 contributor guidance

## Primary workflow

This fork retains `agile-workflow + research-pipeline` as its project process.
`agentic-research` is the authoritative grounded-research engine. Workbench is
available upstream prior art, not this repository's active workflow and not a
migration target.

For substantive repository work:

1. Read `.work/CONVENTIONS.md` and query `.work/bin/work-view`.
2. Track scope, decisions, implementation notes, and review findings in the
   relevant `.work/` item.
3. Use Research Pipeline for project-process concerns and Agentic Research for
   grounded research execution.
4. Commit stage transitions and coherent implementation increments.
5. Validate affected plugin surfaces in both Claude and Codex shapes.

Do not create Workbench-owned state in this repository. Do not convert the
existing `.work/`, `.research/`, or knowledge artifacts to Workbench schemas.

## Ownership

- Nathan's upstream owns all plugins except `research-pipeline` and explicitly
  documented fork patches.
- Andrew's fork owns `research-pipeline`, marketplace identity/composition, and
  this repository's retained `.work/` history.
- `agentic-research` owns ARD. Never copy its kernel, discipline, validators,
  templates, or research orchestration into `research-pipeline`.
- Research Pipeline may wrap Agentic Research with process intent, knowledge
  discovery, and operator-confirmed work coordination.

## Skill authoring

Portable `SKILL.md` frontmatter contains only `name` and `description`. Put
Codex presentation and invocation policy in `agents/openai.yaml`. Keep shared
skill prose harness-neutral and prefer public skill namespaces over host-only
tool names.

Keep skills focused. Move deep catalogs into directly linked references. Make
cross-plugin prerequisites explicit and fail clearly when they are absent.

## Hooks and generated knowledge

Hook commands use `${PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}` and must degrade to a
silent no-op when their activating substrate is absent. Test SessionStart and
PostCompact behavior. Codex PostCompact cannot inject context directly; compact
or resume SessionStart is its reinjection path.

Knowledge index files are generated from source artifacts. Never hand-edit
them. New Agentic Research analytical paths and retained legacy pipeline paths
must both remain discoverable until an operator-confirmed conversion completes.

## Safety and tests

Preserve user-authored work and existing corpora. Migrations are additive and
operator-confirmed. Do not make production changes or publish plugin versions
without explicit scope and passing validation.

Prefer tests at stable interfaces: manifest parity, marketplace parity, skill
shape, resolver behavior, knowledge generation, hook activation/silence/size,
and upstream-tree drift.
