---
id: feature-knowledge-hooks-2026-08
kind: feature
stage: done
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

## Implementation record

### 2026-08-01

- Extended discovery across current `.research/analysis/` artifacts and retained
  legacy `.research/briefs/` / `.research/programs/` paths.
- Preserved Agentic Research's own frontmatter contract instead of imposing the
  project-doc schema; excluded source tiers, scaffold files, and import holding.
- Added current and legacy containment handling to the knowledge graph.
- Made navigator generation fail above 10KB and made the hook emit a pointer
  instead of truncated YAML for oversized pre-existing indexes.
- Added PostCompact navigator and substrate reorientation. Claude can consume
  its output directly; Codex reinjects on compact/resume SessionStart because
  Codex PostCompact output is side-effect-only.
- Added tests for current/legacy discovery, exclusions, missing-substrate
  silence, navigator size enforcement, hook wiring, source checkout resolution,
  and installed-cache resolution.

The feature is ready for cross-host validation.

## Review outcome

Knowledge index and graph suites pass 19/19. Hook activation, missing-index
silence, PostCompact wiring, and oversized-navigator behavior pass. A fresh
Codex session received `total_docs: 488` without reading files; the installed
Claude 0.2.0 hook returned the same navigator from its real cache path.
