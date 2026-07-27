---
name: work
description: Use in a Workbench-owned project to scope, clarify, implement, fix, refactor, simplify, clean up, review, audit, continue, finish one epic, drive several epics to done, or complete ready work inside a named delivery boundary. Gather consequential requirements from the human, route substantial implementation-shaping design through design, coordinate execution, park valuable out-of-scope findings, verify behavior at the configured review weight, reconcile project truth, and continue until the full requested scope is complete or genuinely blocked.
---

# Work

Carry the user's natural-language boundary to its requested finish line. Never
require them to choose a phase, worker topology, or workflow skill.

Read `.work/CONVENTIONS.md`, relevant work items, project instructions,
foundation documents, `.knowledge/index.json` when present, and affected code
before structural decisions. If the substrate is absent or owned by another
system, stop and offer `setup`; do not invoke destructive conversion without
the user's explicit choice.

If inspection shows that the intended outcome, ownership boundary, or basic
success shape is too ambiguous to form coherent work, route through `ideate`.
Do not create or reshape work items while ideating; resume `work` only after the
user explicitly selects a Workbench handoff.

Load references only as needed:

- requirements or consequential ambiguity →
  [references/requirements.md](references/requirements.md);
- item creation, relationships, blocking, completion, or summaries →
  [references/lifecycle.md](references/lifecycle.md);
- multi-unit or multi-epic execution →
  [references/execution.md](references/execution.md);
- nontrivial UI or journey uncertainty →
  [references/ui-ux.md](references/ui-ux.md);
- substantial implementation, refactoring, or recurrence →
  [references/maintenance.md](references/maintenance.md);
- implementation completion or review →
  [references/verification.md](references/verification.md) and
  [references/review.md](references/review.md).

When substantive external investigation is necessary, use Workbench's
`research` skill rather than creating an ungrounded project note.

## Resolve the requested boundary

Keep narrow requests narrow. Treat “finish,” “drive to done,” and “handle end
to end” as instructions to reach the requested finish line.

For an epic, include required children and integration. For several epics,
resolve the complete named target set. For a delivery outcome, discover
necessary work inside that boundary without silently draining unrelated queues.
If the boundary is unclear, ask which items are in scope. A multi-epic request
does not require a synthetic program item.

Keep clarification inside `work` when the outcome is clear and only a small
number of consequential requirements remain. Use `ideate` when selecting the
outcome or boundary requires collaborative exploration, competing directions,
or several foundational decisions.

## Gather requirements from the human

Learn discoverable facts from the repository and current sources. Ask the user
at least one focused question for product direction, preferences, supported
behavior, consequential trade-offs, or other choices only they can settle, then
pause for the answer. Never treat missing structured-question tooling as
permission to guess or continue.

Record accepted outcomes, constraints, exclusions, and acceptance evidence
without manufacturing a large template.

## Shape durable work

Use one active item for one coherent outcome. Create hierarchy only when
independent status or cross-session relationships matter. Temporary agent units
belong in an execution approach, not automatically in `.work/active/`.

Use `blocked_by` only when work would otherwise be invalid. Use `related_to` for
useful context. A blocked item must name the concrete condition that unblocks
it.

A standalone cleanup, simplification, or refactor is normal Workbench work when
it has a coherent boundary and observable completion evidence. Use tags such as
`cleanup` or `refactor`; do not add another item kind. Split independent
subsystems only when their status or verification can meaningfully diverge.

## Execute to the requested finish line

Order work from real prerequisites. Research only to the depth needed. Route
substantial implementation-shaping design through Workbench's `design` skill;
keep obvious local design inline. A direct user request to design stops after
design, while an end-to-end delivery request resumes implementation after the
design and its required review. Parallelize only genuinely independent units
with clear ownership and integration points.

Inspect actual changes and returned evidence. The orchestrating agent owns
integration, acceptance, and the full requested scope. Do not stop because one
child finished, implementation ended before review, a worker returned, or a
former stage boundary was reached.

Pause when discovered work materially exceeds the requested boundary, requires
a new epic-sized outcome, or reaches an irreversible, production, or real-data
action. Park useful findings outside the current scope with evidence instead of
expanding silently.

Continue until every item in the requested boundary is complete or a concrete
external blocker prevents meaningful progress.

## Verify, review, and close

Verify behavior at stable interfaces, run required project checks, and exercise
meaningful user journeys. Read [references/review.md](references/review.md),
resolve the effective `review_weight`, and apply its implementation-review
policy. An explicit user request overrides the repository default. Verify and
adjudicate reviewer findings rather than accepting them blindly.

Reconcile affected foundation assertions before completion. Close every
completed item immediately:

- `completed_items: summarize` → replace it with a compact completed stub;
- `completed_items: discard` → remove it.

Before closing, remove the completed id from remaining `blocked_by` and
`related_to` lists; a parent cannot close while active children remain. Run
`validate-workbench.py` after creating, reshaping, or closing ledger items.
Resolve it from the loaded Workbench plugin package using setup's
identity-verification rule; stop rather than guessing among ambiguous
installations. Never leave completed items active.

Before interruption, handoff, or context loss, update affected items with
settled requirements, completed outcomes, current evidence, next actions, and
blockers. On resume, reconcile that state against Git and code before acting.

Report completed outcomes, meaningful decisions, verification, closure
disposition, blockers, and intentionally parked follow-ups.
