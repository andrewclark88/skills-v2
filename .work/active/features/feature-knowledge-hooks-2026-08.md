---
id: feature-knowledge-hooks-2026-08
kind: feature
stage: drafting
tags: [research-pipeline, knowledge-index, hooks]
parent: epic-upstream-reconciliation-2026-08
depends_on: [feature-research-composition-2026-08]
release_binding: null
gate_origin: null
created: 2026-08-01
updated: 2026-08-01
---

# Preserve and modernize knowledge context hooks

Retain the three-layer knowledge index and graph where they add value, align
them with the current research substrate, and make session orientation reliable
across Claude and Codex.

## Acceptance

- Navigator generation and size limits are tested.
- SessionStart injects navigator context in Claude and Codex.
- Long-session/PostCompact behavior is explicit and tested.
- Missing indexes and empty substrates remain silent.
- Generated knowledge artifacts have one source of truth.
