---
id: feature-research-composition-2026-08
kind: feature
stage: implementing
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

## Design

### Authority boundary

`agentic-research` is the single authoritative ARD and grounded-engagement
engine. It owns:

- the ARD specification, catalogs, discipline bundle, and templates;
- substrate bootstrap/sync and legacy rigor-uplift;
- citation lint, conformance, refresh, adversarial review, and evaluation;
- the `.research/` tier contract and `research-view` query surface; and
- operator-confirmed research-to-work handoff.

`research-pipeline` remains the process overlay. It owns:

- prior-art discovery during ideation and scope changes;
- project intent, architecture, design, and work decomposition;
- knowledge-index and knowledge-graph discovery across project artifacts;
- quality-checkpoint orchestration; and
- familiar intent entrypoints that select an engagement shape.

The overlay may select, commission, and consume an agentic-research engagement.
It must not copy or restate the ARD kernel.

### Familiar entrypoints as intent profiles

Keep the existing user-facing names, but make their research mechanics thin
delegations to `agentic-research:research-orchestrator`:

| Entrypoint | Process intent | Orchestrator profile |
|---|---|---|
| `research` | answer a bounded implementation or domain question | focused or discovered multi-facet engagement; brief output |
| `scout` | map prior art before project definition | breadth-survey intent; landscape brief output; no technology choice |
| `brief` | resolve a blocking knowledge gap for a work item | commissioning-item dials; brief output; cite result from the item |
| `deep-research` | investigate a consequential multi-facet domain | multi-specialist campaign; standard/full rigor as warranted |
| `research-program` | coordinate several decision-linked research arcs | `[research]` epic decomposed into separately registered feature engagements |

The entrypoint supplies process context, a decision-relevance hypothesis, and
proposed dials. The orchestrator still performs its required kickoff and owns
research execution and verification. Escalation between shapes is therefore a
dial/topology change, not a handoff between duplicate engines.

### Paths and existing corpora

New authoritative outputs use agentic-research's current map under
`.research/analysis/`, `.research/attestation/`, and `.research/reference/`.
Existing research-pipeline corpora are preserved in place until the operator
runs `agentic-research:convert`, confirms classification, and accepts per-artifact
refresh. No bulk move, silent rewrite, or knowledge-index deletion is allowed.

During coexistence, knowledge discovery must index both legacy pipeline paths
and current agentic-research paths. A converted artifact remains discoverable
through the superseding artifact and its retained import lens. Once a project
has no remaining legacy artifacts, its generated index may stop scanning the
legacy layout.

### Quality seam

Research engagements run agentic-research's verification floor inline. The
release-time citation gate remains a thin process adapter that invokes the
authoritative agentic-research lint over research artifacts touched or consumed
by the release; it must not carry a forked validator. `quality-checkpoint`
continues to orchestrate that adapter alongside the delivery gates.

### Cross-plugin resolution

References must use the public skill namespace for agent actions and discover a
plugin root at runtime for CLI validators. They must not assume that
`research-pipeline` and `agentic-research` share a checkout path. Missing
`agentic-research` is a clear prerequisite error with an install instruction,
not a fallback to retired local ARD code.

## Migration sequence

1. Add an explicit agentic-research prerequisite and composition contract.
2. Convert familiar research skills into process/profile wrappers.
3. Point the citation gate at the authoritative validator and remove its copied
   kernel only after cross-host root discovery is proven.
4. Expand knowledge discovery to both layouts before retiring legacy scanning.
5. Remove vendored ARD skills, scripts, schemas, and templates only after no
   live wrapper references them and validation passes on Claude and Codex.

Each step is independently reversible. Existing project corpora are migrated
only through the operator-confirmed `convert` flow.
