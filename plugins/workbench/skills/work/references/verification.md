# Behavioral Verification

Verify the requested outcome at the most stable useful interface.

1. Check every accepted requirement and explicit exclusion.
2. Run required commands from `.work/CONVENTIONS.md`, CI, or project
   instructions.
3. Exercise meaningful user journeys or integration boundaries.
4. Inspect the final diff for accidental expansion, stale compatibility,
   sensitive data, and incomplete cleanup.
5. Review proportionately to consequence, uncertainty, and reversibility.
6. Reconcile affected foundation assertions.

Prefer tests that prove externally meaningful behavior at stable interfaces.
Avoid tautological mocks, implementation-detail assertions, and coverage-only
tests that cannot catch a real regression. When durable behavior changes, add
or update the smallest useful behavioral evidence.

Tests must earn their maintenance cost by protecting a meaningful behavior,
contract, boundary, risk, or reproduced regression. Do not test every line,
branch, implementation path, or trivial accessor. Concentrate evidence where a
failure would matter, and remove or reshape tests whose signal no longer
justifies their brittleness and upkeep.

Apply security, privacy, accessibility, performance, compatibility, data
integrity, and operational-readiness lenses when the affected surface or
discovered risk warrants them. These are lenses, not fixed gates.

For reported defects, reproduce before correction whenever possible. Preserve a
failing regression test or another repeatable before/after check, diagnose root
cause, correct the smallest coherent boundary, and prove the original behavior
now passes. Never weaken a test merely to obtain green output.

If a reported defect cannot be reproduced, do not make a speculative fix.
Investigate environment, state, timing, versions, and observability; otherwise
record what was attempted and leave the item active or blocked. Fix incidental
defects within scope only when they block or are caused by the delivery and the
correction is cohesive. Park unrelated defects with reproduction evidence.

Do not declare completion while required verification fails or a consequential
blocker remains.
