---
id: feature-research-composition-2026-08
kind: feature
stage: drafting
tags: [research-pipeline, agentic-research, refactor]
parent: epic-upstream-reconciliation-2026-08
depends_on: [feature-upstream-baseline-2026-08]
release_binding: null
gate_origin: null
created: 2026-08-01
updated: 2026-08-01
---

# Compose research-pipeline with agentic-research

Preserve research-pipeline's project planning, prior-art, architecture, design,
and knowledge roles while delegating current ARD grounding and research
engagement mechanics to upstream agentic-research.

## Acceptance

- There is one authoritative ARD implementation.
- Research skill routing is explicit and has a migration story for existing
  `.research/` corpora.
- Research-to-work handoff remains operator-confirmed.
- Existing knowledge-index consumers do not silently lose discoverability.
