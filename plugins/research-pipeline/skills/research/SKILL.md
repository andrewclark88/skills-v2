---
name: research
description: >
  Answer a bounded external technology or domain question that can change a project decision.
  Keeps the familiar research-pipeline entrypoint while delegating grounded execution and ARD
  verification to agentic-research:research-orchestrator.
user-invocable: true
allowed-tools: Read, Glob, Grep, Skill, AskUserQuestion
model: opus
---

# Research

Use this for a bounded implementation or domain question. This skill owns the
project-facing setup; `agentic-research:research-orchestrator` owns the research.

Read `${CLAUDE_PLUGIN_ROOT}/docs/research-composition.md` and the project's
knowledge index first. Search for overlapping work and surface whether the
engagement is new, a gap-fill, or a refresh.

Before invoking the orchestrator:

1. Read the relevant project and work-item context.
2. State the question and the downstream decision it can change.
3. Propose a focused synthesis brief as `output_kind`; do not pre-commit fan-out.
4. If an existing artifact is the starting point, pass it as a refresh input
   rather than treating it as source substrate.

Then invoke `agentic-research:research-orchestrator` with the seed, project
constraints, decision-relevance hypothesis, known prior artifacts, and proposed
output shape. Let it conduct kickoff, settle dials with the user, discover
topology, write current `.research/` artifacts, and run its verification stack.

After completion, regenerate or update the knowledge index so the artifact is
discoverable. If the result is actionable, suggest the orchestrator's
operator-confirmed research handoff; never emit work automatically.
