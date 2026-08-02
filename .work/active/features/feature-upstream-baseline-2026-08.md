---
id: feature-upstream-baseline-2026-08
kind: feature
stage: drafting
tags: [upstream-sync, agile-workflow]
parent: epic-upstream-reconciliation-2026-08
depends_on: []
release_binding: null
gate_origin: null
created: 2026-08-01
updated: 2026-08-01
---

# Establish the current upstream baseline

Adopt current upstream content for upstream-owned plugins and shared tooling,
without replaying obsolete fork snapshot commits or dropping fork-owned plugins,
marketplace identity, substrate history, or local process artifacts.

## Acceptance

- Upstream-owned plugin content matches the selected upstream commit except for
  explicitly documented extensions.
- `research-pipeline` and its history remain present.
- Root marketplace metadata exposes the intended combined plugin catalog.
- The worktree contains no unresolved merge artifacts.
