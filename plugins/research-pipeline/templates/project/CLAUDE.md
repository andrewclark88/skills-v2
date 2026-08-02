# {{PROJECT_NAME}}

<!-- Add project-specific purpose, constraints, and commands here. -->

## Process

Use `agile-workflow` for durable delivery state in `.work/`,
`research-pipeline` for discovery/planning/architecture/knowledge, and
`agentic-research` for grounded research execution.

Workbench is not active in this project unless the project was explicitly
created with Workbench. Never mix its substrate schemas into this process.

## Session orientation

The compact `docs/knowledge-index-nav.yaml` and `.work/` snapshot load at
session start. Read `docs/knowledge-index.yaml` for the full catalog and
`docs/knowledge-index-detail.yaml` for summaries and relationships.

Run `research-pipeline:knowledge-index` after changing planning or research
artifacts. These index files are generated; do not edit them by hand.

## Research

Use the familiar pipeline intents (`scout`, `research`, `brief`,
`deep-research`, `research-program`). They commission
`agentic-research:research-orchestrator`, which owns source attestations,
synthesis, current `.research/` paths, and verification.

Existing legacy research paths remain readable. Migrate them only through the
operator-confirmed `agentic-research:convert` flow.
