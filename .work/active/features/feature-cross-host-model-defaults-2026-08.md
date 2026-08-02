---
id: feature-cross-host-model-defaults-2026-08
kind: feature
stage: drafting
tags: [claude, codex, workflow, prompt-ware]
parent: null
depends_on: []
release_binding: null
gate_origin: null
created: 2026-08-02
updated: 2026-08-02
---

# Make workflow model defaults host-aware

Preserve the existing role-based model and effort guidance while making every
cross-model workflow work symmetrically when either Claude Code or Codex is the
driver. Remove stale Claude-only skill metadata from portable Research Pipeline
skills, route concrete model choices through Agile Workflow's shared model
matrix, and make peer-readiness diagnostics validate the opposite host rather
than assuming Codex is always the peer.

This is related to, but does not absorb,
`cross-model-review-prompt-ware`: that backlog item decides when foundational
prompt-ware should trigger review; this feature decides how an already-required
peer is selected.

## Acceptance

- Claude-driven workflows select an explicit Codex model and effort appropriate
  to the role; Codex-driven workflows select an explicit Claude model and effort.
- Shared skill prose does not describe Claude as the assumed driver.
- Research Pipeline portable skill frontmatter contains only `name` and
  `description`; Codex invocation policy remains in `agents/openai.yaml`.
- The SessionStart peer preflight detects the active host and checks the
  opposite subscription-backed CLI without producing noise when peer review is
  unavailable by design.
- Tests cover both Claude-to-Codex and Codex-to-Claude readiness paths, including
  missing CLI and unauthenticated CLI behavior.
- The older Claude-only model-selection guidance is replaced by or redirected
  to the shared cross-host decision matrix.

## Simplification opportunities

- Consolidate concrete model mappings in one shared reference instead of
  maintaining a second Claude-only role table in Research Pipeline.
- Replace repeated host-specific advisory wording with one shared policy link.
- Remove portable frontmatter keys that only one harness understands.
