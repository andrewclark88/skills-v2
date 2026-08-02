---
name: research-program
description: >
  Coordinate several decision-linked research engagements as a research epic. Retains the familiar
  program entrypoint while using separately registered agentic-research engagements rather than a
  second nested research engine.
---

# Research Program

A program is work-side coordination across several research arcs, not a fourth
research tier. Read `${CLAUDE_PLUGIN_ROOT}/docs/research-composition.md`, project
intent, the knowledge index, and the Agentic Research handoff contract.

Use the retained agile-workflow substrate:

1. Define the program's downstream decisions and boundaries.
2. Create or refine a `[research]` epic whose children are separately scoped
   `[research]` features. The epic itself carries no engagement registration.
3. Give each feature one `research_dials:` block, explicit decision-relevance
   prose, expected output kind, and dependencies on earlier research arcs.
4. Confirm the decomposition and sequencing with the user.
5. Invoke `agentic-research:research-orchestrator` once per ready feature. Each
   feature is one independently registered, verified engagement.
6. Cite outputs through `research_refs:` and let the orchestrator close or route
   each commissioning item according to project conventions.

Cross-arc synthesis is itself a separately registered engagement consuming the
prior arcs as lenses. It must trace claims to source attestations and must not
launder analytical artifacts into citations.

Do not recreate the legacy `.research/programs/` hierarchy, nested campaign
engine, fixed cost bands, or vendored verification stack. Existing programs stay
discoverable and migrate only through operator-confirmed conversion.
