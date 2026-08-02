# Research composition

`research-pipeline` is the project-process overlay. `agentic-research` is the
grounded research engine and the single authoritative deployment of ARD.

## Responsibilities

The pipeline owns the reason research occurs and how its result enters project
work: prior-art scouting, ideation, blocking briefs, architecture, design,
knowledge discovery, and quality-checkpoint orchestration.

Agentic Research owns how grounded research is executed: engagement dials,
decomposition, source attestations, citation chains, synthesis, verification,
refresh, substrate conventions, and operator-confirmed research-to-work handoff.

Pipeline skills must not duplicate or paraphrase the ARD discipline. They invoke
`agentic-research:research-orchestrator` with process context, a decision-relevance
hypothesis, and a proposed output shape. The orchestrator performs its normal
kickoff and remains authoritative for the engagement.

## Intent profiles

| Pipeline entrypoint | Intent | Proposed output shape |
|---|---|---|
| `scout` | map prior art without choosing a solution | breadth-survey landscape brief |
| `research` | answer a bounded implementation or domain question | focused synthesis brief |
| `brief` | resolve a work-item-blocking knowledge gap | commissioning-linked brief |
| `deep-research` | investigate a consequential multi-facet domain | campaign |
| `research-program` | coordinate multiple decision-linked research arcs | research epic with registered feature engagements |

These are starting profiles, not separate engines or fixed cost tiers. The
orchestrator discovers fan-out and confirms rigor according to the downstream
decision.

## Corpora and migration

New outputs follow Agentic Research's `.research/analysis/`,
`.research/attestation/`, and `.research/reference/` map. Knowledge tools scan
both that map and the legacy pipeline paths (`.research/briefs/` and
`.research/programs/`) during the transition.

Never migrate a corpus implicitly. Run `agentic-research:convert`; let it propose
and classify candidates; require operator confirmation; retain imported lenses;
and refresh claim-bearing artifacts individually. Existing paths remain valid
until that process completes.

## Work handoff

Research commissioned by a `.work/` item uses a `[research]` item carrying
`research_dials:` when durable coordination is useful. Results are cited through
`research_refs:`. Actionable findings become work only through the
operator-confirmed `agentic-research:research-handoff` flow.

## Prerequisite

The `agentic-research` plugin must be installed and enabled. A missing plugin is
a prerequisite error; do not fall back to the retired vendored ARD machinery.
