---
name: ideate
description: Collaboratively clarify, explore, or stress-test an uncertain project, feature, problem, or design before work is scoped. Use when the user asks to brainstorm, think something through, explore prior art, be grilled, challenge assumptions, bootstrap a project, or define a substantial sub-project within a monorepo. Inspect discoverable context, ask one load-bearing question at a time, and write nothing until the user explicitly chooses a Workbench, research, backlog, or root- or sub-project-foundation handoff.
---

# Ideate

Help the user discover what they actually want before turning the conversation
into project state.

Unless an instruction names a repository path or artifact, communicate with the
user in the current conversation, including questions, offers, proposals,
recommendations, explanations, summaries, and reports. Do not create report
files or durable no-op records unless the user requests them.

## Explore

Inspect relevant files, documents, code, `.knowledge/index.json` when present,
and recent decisions before asking questions the repository can answer.

Identify the most load-bearing open decision thread and ask one question at a time.
Include a working recommendation and rationale when it gives the user something
useful to challenge. Follow the current decision thread deeply before moving
sideways.
When the user asks to be grilled, increase the pressure on assumptions and
trade-offs without changing the workflow.

Select only useful lenses:

- intent, audience, and desired outcome;
- scope, exclusions, and success evidence;
- ownership boundary and relationship to sibling or root projects;
- prior art and alternatives;
- feasibility and dependencies;
- failure, safety, and operations;
- evidence gaps;
- privacy, compliance, and data handling.

Use current-source research for unstable facts, but hand substantive
investigation to Workbench's `research` skill.

Every several exchanges, summarize in the current conversation:

- settled decisions;
- explicitly deferred decision threads;
- open decision threads;
- the decision thread currently under examination.

Stop when the next concrete action is clear, no meaningful question remains, or
the user stops the process.

## Preserve the no-write boundary

Do not create files, edit foundations, bootstrap a project, or scope work during
exploration. Conversational summaries are not project artifacts. At the end,
offer only relevant handoffs:

- activate a Workbench item;
- park the idea;
- commission research;
- write root foundation documents for repository-wide truth;
- write sub-project foundation documents for a durable, independently coherent
  scope within a monorepo or larger repository.

Write only the handoffs the user explicitly selects. Project setup is one
possible result, never the assumed result.

Place a sub-project foundation at that scope's established documentation
location, such as `<sub-project>/docs/` or `docs/<sub-project>/`, and follow its
local instructions. Use unscoped root foundations only for repository-wide
truth. Link the levels where their contracts meet; do not duplicate the same
assertion across locations or create a competing foundation for a scope that
has no durable ownership boundary.
