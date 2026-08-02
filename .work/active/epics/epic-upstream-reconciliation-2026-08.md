---
id: epic-upstream-reconciliation-2026-08
kind: epic
stage: done
tags: [agile-workflow, research-pipeline, upstream-sync, process]
parent: null
depends_on: []
release_binding: null
gate_origin: null
created: 2026-08-01
updated: 2026-08-01
---

# Reconcile skills-v2 with Nathan's current upstream

Bring the fork forward from its June 2026 upstream snapshot without burying a
workflow redesign inside a mechanical merge.

## Evidence

- Fork `main` is 47 commits ahead of the common ancestor; upstream `main` is
  789 commits ahead.
- Local agile-workflow is 0.11.3; upstream is 0.16.14.
- Four fork commits are historical upstream-sync snapshots and should be
  superseded by the new upstream baseline, not replayed as extensions.
- Fork-owned durable capabilities include the project-process integration,
  knowledge navigator/index/graph, prior-art scout, research planning,
  architecture grounding, design-family overlays, quality checkpoint, and
  compact SessionStart context.
- The fork vendored ARD 0.4.1 into research-pipeline. Upstream has since absorbed
  and evolved ARD as `agentic-research` 0.6.5 with a native orchestrator,
  research-view, refresh/re-engagement, and research↔work handoff.
- Upstream now also ships `workbench` 0.5.0, a consolidated and mutually
  exclusive alternative to agile-workflow with its own `.work/`, `.research/`,
  and `.knowledge/` schemas.
- Current repository guidance incorrectly says Codex plugin hooks are not
  available. Codex 0.146.0 has been integration-tested successfully with the
  research-pipeline SessionStart navigator.

## Directional decisions required

1. Retain agile-workflow as the base, or migrate the suite/process to Workbench.
2. Keep vendored ARD inside research-pipeline, or compose with upstream
   agentic-research and make research-pipeline a thinner planning/knowledge
   overlay.
3. Preserve the current three-layer knowledge index and interactive graph, adopt
   Workbench's smaller `.knowledge/index.json`, or deliberately support both by
   workflow family.
4. Preserve `gate-infra` as a fork extension, relocate it, or retire it in favor
   of upstream's newer audit/plugin boundaries.

## Recommended direction pending confirmation

Use current upstream as the new repository baseline; retain agile-workflow for
existing projects; add Workbench as an available but not automatically adopted
alternative; preserve research-pipeline's project-process and knowledge-layer
capabilities; replace its vendored ARD implementation with an explicit
composition over agentic-research; and keep migrations operator-confirmed.

## Design decisions

- Retain `agile-workflow + research-pipeline` as Andrew's primary process.
- Carry Workbench as an optional upstream plugin; do not adopt or convert
  existing projects automatically.
- Treat Workbench as prior art for selective evolution, not as a future
  migration target. Candidate ideas must be evaluated and adopted individually
  without importing its mutually exclusive substrate schemas.
- Treat current upstream files as authoritative for upstream-owned plugins.
  Do not resolve old snapshot conflicts line by line.
- Preserve fork-owned research-pipeline capabilities, but compose with current
  `agentic-research` rather than maintaining a stale vendored ARD kernel.
- Preserve the knowledge navigator and validate it in both Claude and Codex.
- Keep all project migrations explicit and operator-confirmed.

### Workbench ideas worth evaluating later

- Outcome-first natural-language requests that route into the existing staged
  process without requiring users to name every skill.
- Proportional ceremony: formal design and review depth should track decision
  consequence and risk, not merely item size.
- Semantic autonomy: human-owned product and irreversible choices remain
  explicit while routine reversible choices stay with the agent.
- A shared review-weight vocabulary, provided it composes with the existing
  quality gates rather than replacing them.

These are possible enhancements to the retained workflow. Workbench's `.work/`,
`.research/`, and `.knowledge/` schemas are not adoption targets.

## Decomposition

1. `feature-upstream-baseline-2026-08` — establish current upstream-owned plugin
   content while preserving fork marketplace identity and research-pipeline.
2. `feature-research-composition-2026-08` — replace vendored ARD coupling with
   an explicit agentic-research integration and settle research skill routing.
3. `feature-knowledge-hooks-2026-08` — preserve and modernize the knowledge
   index/graph and cross-host session hooks.
4. `feature-process-docs-2026-08` — update the combined build process,
   manifests, templates, and guidance for the new plugin map.
5. `feature-cross-host-validation-2026-08` — run structural, behavioral,
   Claude, and Codex validation before any version bump or publication.

## Non-goals

- No direct merge into `main` before the decisions above are settled.
- No automatic conversion of existing projects from agile-workflow to Workbench.
- No silent migration or deletion of existing `.research/` corpora.
- No version bumps or marketplace publication until cross-host validation passes.

## Completion

The fork now tracks Nathan's current upstream baseline while retaining Andrew's
Agile Workflow + Research Pipeline process. Research Pipeline composes with one
authoritative Agentic Research engine, current and legacy research layouts stay
discoverable, cross-host hooks are tested and installed, process guidance is
single-sourced, and Workbench remains optional prior art. Research Pipeline
0.2.0 and the complete reconciliation history are pushed on the tracked feature
branch.
