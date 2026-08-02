# Research intents

Research Pipeline exposes familiar project-facing intents while Agentic
Research supplies one dynamic grounded-research engine.

| Intent | Project purpose | Starting profile |
|---|---|---|
| `scout` | reveal prior art and research gaps | breadth survey |
| `research` | answer a bounded decision-relevant question | focused brief |
| `brief` | curate implementation-critical knowledge for a work item | commissioned brief |
| `deep-research` | investigate a consequential multi-facet domain | campaign |
| `research-program` | coordinate several decision-linked arcs | research epic |

These names are not fixed cost tiers and do not implement separate agent trees.
Each supplies project context, a decision-relevance hypothesis, and a proposed
output kind to `agentic-research:research-orchestrator`. The orchestrator settles
verification rigor with the user and discovers fan-out from the seed.

## Escalation

Escalation is a topology or coordination change:

- a focused question may discover several facets and become a campaign;
- several independent decision arcs become `[research]` feature engagements
  coordinated by a research epic; and
- cross-arc synthesis is another registered engagement, not an untracked
  program-only mechanism.

## Grounding and verification

All authoring follows Agentic Research's current ARD discipline. The engine owns
source attestations, citation lint, adversarial review, isolated evaluation,
spot-checks, refresh, and acquisition offgas. Research Pipeline does not carry a
copy of these mechanisms.

## Outputs and discovery

New work uses `.research/analysis/`, `.research/attestation/`, and
`.research/reference/`. The knowledge layer also scans legacy
`.research/briefs/` and `.research/programs/` until an operator-confirmed
conversion is complete.

See [research composition](research-composition.md), [build process](build-process.md),
and Agentic Research's own `research-orchestrator` and `HANDOFF.md` contracts.
