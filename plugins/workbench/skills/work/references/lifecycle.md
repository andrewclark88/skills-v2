# Work Lifecycle

## Relationships

- `parent` expresses outcome hierarchy, not scheduling.
- `blocked_by` names active prerequisites without which useful execution is
  invalid.
- `related_to` communicates useful context without controlling readiness.
- `status: blocked` requires either an active prerequisite in `blocked_by` or
  an exact `## Blocker` body section naming the concrete external blocker and
  unblock condition.

Structured relationships resolve to active items. Before closing an item,
remove its id from remaining `blocked_by` and `related_to` lists. Do not close a
parent while active children remain. Completed context belongs in the
completion-stub body or version summary, not the active readiness graph.

## Item shape

Use an epic only when several independently meaningful outcomes benefit from a
durable parent. Use a feature or story when independent status or relationship
matters across sessions. These are outcome-hierarchy tiers only; they imply no
stages or ceremonies. Do not mirror temporary agent tasks into the ledger.

Active items use:

```yaml
---
id: <stable-kebab-id>
kind: epic|feature|story
status: active|blocked
tags: []
parent: null
blocked_by: []
related_to: []
research_refs: []
mock_refs: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Ids are unique across all `.work/`. Keep one coherent outcome in one item.
Split only when separate status, relationship, ownership, or summary treatment
provides durable value. Use tags such as `audit`, `security`, or `performance`
for focused investigations rather than another item kind.

## Completion sweep

At entry and exit, inspect `.work/active/` for stale completion claims or
interrupted work. Verify actual repository evidence before closing; never infer
completion from a stale label.

Close atomically:

- `completed_items: summarize` → replace the active item with one
  `.work/completed/` stub;
- `completed_items: discard` → remove the active item.

Run the Workbench validator after structural ledger changes. Never leave done
or completed items active. Commit at coherent delivery boundaries when
repository policy permits; item edits do not require their own commits.
