# Vision: Workbench

Workbench is a compact, requirements-first environment for getting project work
done and preserving only the state another agent actually needs.

The user speaks naturally: clarify this idea, set up this repository, scope this
change, finish these epics, park that finding, research the prior art, or prepare
a release summary. Workbench adapts internally without asking the user to choose
workflow stages or an orchestration topology.

## Core commitments

- **Human requirements are load-bearing.** Learn repository facts first, then
  ask the user about consequential choices only they can settle.
- **Ideation precedes premature scope.** A clear outcome remains in `work`; an
  outcome too ambiguous to form coherent work routes through `ideate`, which
  writes nothing until the user chooses a handoff.
- **Design is available, not imposed.** A dedicated `design` skill selects a
  new-work, refactor, performance, defect, UI/UX, or data/integration lens and
  shapes implementation when that work materially benefits from design.
  Obvious local work remains inline.
- **Review depth is legible.** One repository `review_weight` governs design
  and implementation review, while explicit user direction can override it for
  a request. `standard` gives substantive work one independent pass without
  manufacturing convergence.
- **The ledger stays small.** `.work/` tracks active outcomes, deferred context,
  completion summaries, and release summaries with three item kinds and two
  active statuses.
- **One request may span several epics.** The orchestrating agent owns
  requirements, integration, verification, closure, and durable continuation
  across the full named boundary.
- **Research has a separate authority.** `.research/` contains attestations of
  externally fetched sources and grounded synthesis. It informs work without
  being rewritten to match project decisions.
- **Knowledge is discoverable, not duplicated.** A committed deterministic
  `.knowledge/index.json` indexes durable docs, research, and work while each
  source retains its own authority.
- **Foundations follow ownership.** Repository-wide truth belongs in root
  foundations; durable sub-project truth may live in `docs/<sub-project>/` or
  `<sub-project>/docs/` according to repository convention.
- **Tests earn their keep.** Prefer meaningful behavior, contracts, boundaries,
  risks, and regressions over line coverage and implementation coupling.
- **Maintenance follows evidence.** Cohesive cleanup can travel with delivery;
  standalone cleanup and refactors are normal bounded work; broader findings
  are parked.
- **Setup converges.** Existing systems are semantically converted, validated,
  and removed. Workbench does not preserve parallel workflow substrates,
  migration archives, or compatibility copies.
