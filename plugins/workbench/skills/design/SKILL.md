---
name: design
description: >
  Design or stress-test implementation-shaping work before execution. Use when the user asks to
  design, architect, plan, or technically shape new work, a refactor, cleanup, performance change,
  defect correction, UI journey, data change, or integration. Grounds the design in repository
  truth, applies the relevant design lens, records a proportionate design in the Workbench item,
  and reviews it at the configured review weight without making design a mandatory project stage.
---

# Design

Shape work enough to make implementation safe, coherent, and economical.
Design is an optional capability, not a mandatory stage. A direct design
request stops after the reviewed design; `work` may route here and then continue
through implementation.

## Resolve the design boundary

Read `.work/CONVENTIONS.md`, the target item when present, project instructions,
foundation documents, relevant code and tests, and `.knowledge/index.json` when
present. Reconcile stale item claims against the repository before designing.
If `.work/` is absent or owned by another system, stop and offer `setup`; do not
create Workbench state or convert a competing substrate implicitly.

Keep a clear narrow request narrow. If the outcome, ownership boundary, or
success shape cannot yet form coherent work, route through `ideate`. If a clear
request has no active item, create the smallest coherent feature or story needed
to hold durable design state; do not create hierarchy merely to represent
design activity.

Use substantive external investigation through Workbench's `research` skill.
Do not disguise uncertain external claims as design decisions.

## Select lenses

Read [references/lenses.md](references/lenses.md). Select one primary lens:

- new work;
- refactor or cleanup;
- performance;
- defect or reliability;
- UI/UX;
- data, migration, or integration.

Apply only relevant overlays such as security, privacy, accessibility,
operations, or compatibility. State the selected lens in the item. If the work
mixes materially different lenses, separate independently verifiable outcomes
or name which lens governs each unit.

## Resolve decisions

Separate facts, requirements, assumptions, and decisions. Learn discoverable
facts from the repository. Do not re-ask choices already settled by the user,
the item, or foundation truth.

Ask the human about product direction, supported behavior, external contracts,
irreversible choices, or expensive trade-offs only they can settle, then pause
for the answer. Resolve routine reversible implementation choices with judgment
and record the rationale.

Prefer the smallest design that satisfies the accepted outcome. Name meaningful
alternatives when the choice is consequential; do not manufacture options for
obvious local work.

## Record the design

Keep outcome-specific design in the active item rather than a parallel design
document. Add only useful sections:

```markdown
## Design

**Primary lens:** <lens>

### Outcome and constraints
<requirements, exclusions, and success evidence>

### Chosen approach
<boundaries, contracts, data flow, and rationale>

### Alternatives
<meaningful rejected options and trade-offs, when consequential>

### Implementation units
<coherent units, owned surfaces, dependencies, and integration points>

### Verification
<behavior, contract, benchmark, migration, or journey evidence>

### Risks and recovery
<failure modes, assumptions, rollback, fallback, or observability>
```

Use exact paths, interfaces, or schemas only when they reduce implementation
ambiguity. Avoid speculative code listings that merely pre-write the change.

Update root or sub-project foundation assertions only when the design settles
durable current or intended truth. Replace stale assertions in place; Git
carries history.

## Review the design

Read [../work/references/review.md](../work/references/review.md). Resolve the
effective `review_weight` from an explicit user instruction, then
`.work/CONVENTIONS.md`, then `standard`.

Always self-check the design against requirements, repository evidence, the
selected lens, verification feasibility, unnecessary complexity, and reversal
cost. Apply independent review as required by the effective weight before
implementation becomes expensive to reverse. Give the reviewer raw
requirements, the design, relevant foundations and code, and known evidence;
do not lead with a suspected verdict.

Adjudicate findings rather than accepting them blindly. Revise confirmed
material problems and record rejected material proposals with a short
repository-grounded reason.

## Handoff

For a direct design request, report the chosen approach, decisive trade-offs,
effective review weight and evidence, unresolved decisions, and the next
implementation boundary. Do not implement unless the user also requested
delivery.

When called from `work`, return control after the design and its required
review are coherent. `work` owns implementation, integration, verification,
closure, and the full requested finish line.
