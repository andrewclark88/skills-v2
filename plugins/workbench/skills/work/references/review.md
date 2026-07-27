# Independent Review

Resolve one effective `review_weight` from explicit user instruction,
`.work/CONVENTIONS.md`, then `standard`. The same weight governs design and
implementation review so the repository has one understandable rigor control.

| Weight | Review policy |
|---|---|
| `none` | Self-review only. Independent review is skipped, but verification and acceptance evidence remain mandatory. |
| `light` | At most one focused fresh-context pass when consequence, uncertainty, breadth, or reversibility warrants it. Fix and verify without re-review. |
| `standard` | Default. Run one balanced fresh-context pass for substantive implementation-shaping designs and substantive completed changes. Fix and verify without a second pass. |
| `thorough` | Repeat review, adjudication, correction, and verification until no receiver-confirmed material issue remains. |
| `maximum` | Use the thorough convergence loop with complementary and adversarial perspectives and cross-model coverage when available. |

An explicit request for cross-model review selects reviewer diversity, not
automatically a heavier pass count. Under `standard`, broader lenses still fit
inside one pass. Only `thorough` and `maximum` repeat independent review.
When the effective weight requires independent review and no fresh-context path
is available, disclose the limitation and stop for the user's direction rather
than silently approving inline or claiming a lower weight.

Review a design after it is stable enough to constrain implementation and
before implementation becomes expensive to reverse. Review completed work at
the integrated contract boundary. Small reversible work does not need a
ceremonial design review merely because a design section exists.

Read [foundation-truth.md](foundation-truth.md) when the design or implementation
may affect durable project truth.

Give reviewers the raw requirements, artifacts, diff, and verification
evidence available at that point. Do not lead them with the suspected answer.
For design, ask about requirements coverage, boundaries, alternatives,
assumptions, failure modes, verification feasibility, migration or rollback,
unnecessary complexity, and accurate foundation roll-forward. For
implementation, ask about correctness, missing behavior, safety, integration
risk, simplification, foundation drift, and relevant security, privacy,
accessibility, performance, compatibility, data-integrity, and operational
concerns.

Treat findings as proposals. Reproduce or verify each substantive claim,
accept changes that improve the work, and explain rejected material findings in
the current conversation. When a rejection reflects a durable constraint, fold
that constraint into the design's chosen approach or risks; keep no separate
record of the adjudication. Review never substitutes for behavioral
verification, and a reviewer saying “looks good” is not evidence.
