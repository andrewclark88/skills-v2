# Design Lenses

Choose one primary lens and only the overlays that affect the decision. Every
design still states the outcome, constraints, boundaries, verification, risks,
and simplest coherent implementation shape.

## New work

- Ground the design in existing architecture and demonstrated project patterns.
- Name two or three plausible approaches only when the choice is consequential.
- Choose explicitly and explain the trade-off.
- Design the riskiest or least-known unit first.
- Define contracts, ownership, state flow, failure behavior, and integration.
- Run a pre-mortem: identify the weakest assumption, likely production failure,
  and fallback.
- Eliminate unnecessary concepts, layers, options, compatibility paths, and
  tests before adding machinery.

## Refactor or cleanup

- Apply the black-box test: a refactor preserves observable behavior. Route
  intended behavior change through the new-work lens with explicit requirements.
- Describe the actual current state and the costly or unsafe property.
- Eliminate, inline, merge, or delete before extracting new abstractions.
- State invariants and contracts that must remain unchanged.
- Make steps independently understandable and verifiable when practical.
- Include rollback or migration handling where a step is not trivially
  reversible.
- Drop aesthetic churn whose payoff cannot be stated.

## Performance

- Do not design from intuition alone. Define a representative workload and
  include a baseline or the reason measurement is blocked in the recorded
  design.
- Profile the symptom with probes appropriate to CPU, memory, I/O,
  serialization, synchronization, cache behavior, or runtime overhead.
- Rank bottlenecks by measured impact and target the hot path.
- Prefer fixes in this order: eliminate work or improve the algorithm/data
  model; reduce I/O; improve locality; use better runtime idioms; add
  parallelism only when higher-level fixes do not apply.
- State expected metric movement and regression budget.
- Design repeatable benchmarks plus end-to-end evidence; a microbenchmark is
  evidence, not proof.
- Reuse existing benchmark and load-test machinery. Discuss a new performance
  laboratory or substantial harness before building it.

## Defect or reliability

- Reproduce the failure or define the missing observable before designing a fix.
- Trace the causal chain and correct the smallest coherent boundary, not merely
  the visible symptom.
- State affected states, timing, concurrency, retries, idempotency, and failure
  reporting where relevant.
- Preserve a regression check at the most stable useful interface.
- If reproduction is impossible, design observability or a bounded diagnostic
  step instead of a speculative correction.

## UI/UX

- Map the meaningful user journey, entry points, decisions, success, empty,
  loading, error, permission, and recovery states.
- Reuse established interaction and visual patterns unless evidence justifies a
  new one.
- Address accessibility, responsive behavior, keyboard behavior, content, and
  destructive-action recovery where relevant.
- Use existing `.mockups/` references or create a mockup only when visual
  alignment materially reduces ambiguity.
- Verify the journey, not only component snapshots.

## Data, migration, or integration

- Identify the source of truth, ownership boundary, schema or protocol, and
  consistency expectations.
- Verify actual external consumers before adding compatibility machinery.
- For owned disposable shapes, land the correct state directly. For external
  consumers or durable real data, define migration, rollback, version skew, and
  observability.
- Address retries, idempotency, partial failure, ordering, and reconciliation.
- Never execute a production or real-data migration without explicit user
  approval.

## Risk overlays

Apply only when evidence warrants them:

- **Security and privacy:** trust boundaries, authorization, input handling,
  secrets, sensitive data, abuse, and least privilege.
- **Accessibility:** assistive technology, focus, semantics, contrast, motion,
  and alternative interaction.
- **Operations:** rollout, monitoring, support, failure isolation, recovery,
  capacity, and incident diagnostics.
- **Compatibility:** verified external consumers, durable data, deployment
  skew, and contractual obligations.
- **Testing:** stable interfaces, meaningful behavior, demonstrated risks, and
  regression history. Every proposed test must earn its upkeep. Reuse existing
  machinery; add only small, cheap, contained evidence without discussion.
