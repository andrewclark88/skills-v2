---
name: brief
description: >
  Produce implementation-curated domain knowledge that unblocks a work item. Retains the familiar
  pipeline brief entrypoint while delegating grounded research and verification to
  agentic-research:research-orchestrator.
---

# Brief

A brief answers “what does the builder need to know to implement this work
correctly?” It is precise, evidence-backed, implementation-relevant domain
knowledge—not architecture, a tutorial, or a general landscape.

Read `${CLAUDE_PLUGIN_ROOT}/docs/research-composition.md`, the commissioning work
item, architecture, related code, existing briefs, and the knowledge index.
Identify:

- the downstream implementation decision;
- the assumptions or edge cases that could invalidate the build;
- what the codebase already answers; and
- the smallest useful scope for the missing knowledge.

When durable coordination is warranted, use a `[research]` commissioning item
with `research_dials:` and explicit decision-relevance prose. Propose a focused,
implementation-curated brief as the output kind, then invoke
`agentic-research:research-orchestrator`. The orchestrator owns kickoff, source
work, attestations, current output paths, citation lint, and semantic review.

The resulting brief should favor exact rules, API shapes, worked edge cases,
project implications, and test-relevant examples. It should distinguish domain
facts from design choices and call out unresolved gaps.

After the engagement:

1. add the artifact slug to the commissioning item's `research_refs:`;
2. record how it unblocks the item;
3. update knowledge discovery; and
4. let the orchestrator close or route the commissioning item according to
   `.work/CONVENTIONS.md`.

If decomposition discovers several consequential facets, accept the
orchestrator's campaign shape. If it discovers several decision-linked arcs,
route coordination through `research-program`; do not run a duplicate research
workflow inside this skill.
