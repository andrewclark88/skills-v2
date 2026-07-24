# Execution and Continuation

For a multi-unit or multi-epic boundary, write only the coordination detail
needed to maintain ownership and integration:

```markdown
## Execution approach

- **Unit** — outcome and owned write surface
  - Produces:
  - Blocked by:
  - Related context:
  - Isolation:
  - Verification:
```

Keep tightly coupled work in one context. Delegate or parallelize only when
independent focus, specialized capability, isolation, or throughput exceeds
handoff and integration cost.

Assign non-overlapping write surfaces and explicit output evidence. Use
worktrees when isolation materially improves collision avoidance or rollback,
not merely because several units exist.

The orchestrator must inspect returned changes, reconcile interfaces and
assumptions, run integrated checks, and continue across completed units until
the user's full boundary is satisfied.

Before a context limit, interruption, or deliberate handoff, update affected
active items with settled requirements, current repository evidence, delivered
outcomes, remaining next actions, and blockers. On resume, compare that state to
Git and code before continuing.
