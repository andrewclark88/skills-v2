---
id: feature-process-docs-2026-08
kind: feature
stage: review
tags: [documentation, process, plugins]
parent: epic-upstream-reconciliation-2026-08
depends_on: [feature-research-composition-2026-08, feature-knowledge-hooks-2026-08]
release_binding: null
gate_origin: null
created: 2026-08-01
updated: 2026-08-01
---

# Update the combined process and plugin guidance

Make the supported primary process, optional Workbench path, plugin ownership,
skill routing, project templates, and Codex/Claude behavior accurate and
single-sourced.

## Acceptance

- Agile-workflow is clearly the primary substrate for Andrew's process.
- Research-pipeline is described as an overlay, not the entire methodology.
- Workbench is documented as optional and mutually exclusive per project.
- Workbench is treated as prior art; any borrowed ideas are named individually
  and expressed through the retained agile-workflow + research-pipeline model.
- Codex hook support is described accurately.
- No documentation points at retired or duplicated ARD machinery.

## Implementation record

### 2026-08-01

- Replaced the imported Workbench-centered repository instructions with a
  canonical retained-process contract in `AGENTS.md`, mirrored for Claude.
- Rewrote the root README around the three-layer composition:
  Agile Workflow delivery, Research Pipeline project process, and Agentic
  Research grounding.
- Rewrote the build-process reference and auto-loaded skill to make ownership,
  research routing, semantic autonomy, proportional ceremony, review weight,
  migration, hooks, and completion explicit.
- Documented Workbench as optional prior art and prohibited mixed substrate
  schemas or automatic conversion.
- Updated the project `CLAUDE.md` template, plugin manifests, marketplace
  descriptions, research overview, and affected design consumers.
- Modernized the touched skill frontmatter to the portable `name` /
  `description` contract.
- Removed links to retired duplicate-engine architecture documents and copied
  ARD skills.

The feature is ready for repository-wide and cross-host validation.
