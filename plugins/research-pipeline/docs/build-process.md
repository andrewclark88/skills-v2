# Build process

This is the durable methodology for projects using Andrew's retained workflow.

## Composition

| Layer | Owns |
|---|---|
| `agile-workflow` | `.work/` items, dependencies, stages, implementation, review, gates, releases |
| `research-pipeline` | discovery, prior art, project intent, architecture, design overlays, knowledge, quality orchestration |
| `agentic-research` | ARD, `.research/`, source grounding, research topology, synthesis, verification, refresh and handoff |

Workbench is not part of this composition. It may inspire individual process
improvements, but its substrates are never mixed into an Agile Workflow project.

## Principles

- Durable files outrank chat history.
- Research depth is proportional to the decision it can change.
- Human authority is reserved for consequential requirements, irreversible
  choices, migrations, publication, and external side effects.
- Agents own routine, reversible implementation choices inside settled scope.
- Existing knowledge and code are read before new artifacts are commissioned.
- Research records inform work; operational state never rewrites research.
- Research-to-work emission and corpus migration are operator-confirmed.
- Review and ceremony follow consequence and risk, not a fixed document quota.

These last three interaction policies borrow useful ideas from Workbench while
remaining expressed through the retained substrate.

## Session start

1. Read `docs/knowledge-index-nav.yaml` when present. The hook normally injects it.
2. Query `.work/bin/work-view --ready`, `--blocked`, and `--stage review` as needed.
3. Read the active item and its cited `research_refs:` before acting.
4. Use the full and detail knowledge indexes only when a topic match warrants it.

SessionStart and host-supported PostCompact reorient from the navigator and a
compact substrate snapshot. Missing indexes and substrates are silent. Codex
PostCompact cannot inject output, so its compact/resume SessionStart path is the
reinjection point.

## Project discovery

For a new project:

1. `research-pipeline:init-project` scaffolds the project surfaces.
2. `research-pipeline:ideate` establishes vision, specification, architecture
   direction, principles, and the initial research plan.
3. `research-pipeline:scout` maps prior art without selecting a winner.
4. Consequential unknowns become separately commissioned research engagements.

Do not manufacture research because a template expects it. State the downstream
decision first; if no plausible finding changes it, keep the engagement light or
skip it.

## Research intents

The familiar pipeline names are process profiles over one engine:

| Intent | Use when | Expected shape |
|---|---|---|
| `scout` | the project needs a prior-art landscape | breadth survey |
| `research` | a bounded question affects a decision | focused brief or discovered campaign |
| `brief` | a work item lacks implementation-critical domain knowledge | commissioning-linked brief |
| `deep-research` | a consequential domain has several facets | campaign |
| `research-program` | several research arcs affect different decisions | `[research]` epic with feature engagements |

Each wrapper supplies context and a decision-relevance hypothesis to
`agentic-research:research-orchestrator`. The orchestrator owns kickoff, dials,
decomposition, attestations, synthesis, current output paths, and verification.

Use `[research]` work items with `research_dials:` when durable commissioning is
useful. Cite completed results through `research_refs:`. Emit actionable work
only through `agentic-research:research-handoff` after operator confirmation.

## Architecture and decomposition

Architecture settles the smallest set of consequential system decisions needed
to decompose work safely. It reads vision, code, constraints, and relevant
research. It does not repeat domain facts already owned by research artifacts.

`epicize` creates dependency-aware epics. `epic-design` decomposes an epic into
features. `feature-design` records implementation-relevant contracts and
acceptance criteria in the feature body. Use formal design in proportion to:

- blast radius and irreversibility;
- interface, data, security, or migration risk;
- uncertainty that would cause expensive rework; and
- coordination across independently executing agents.

Small reversible changes may proceed with a concise feature body. Consequential
requirements remain explicit human decisions.

## Delivery

Agile Workflow owns the delivery state machine:

```text
drafting → implementing → review → done → release binding → released/archive
```

Respect `depends_on`. Keep implementation discoveries, decisions, tests, and
review findings in the item body. Commit coherent increments and stage
transitions. Do not treat conversation summaries as project state.

Review depth is proportional:

- light: local, reversible, well-tested change;
- standard: ordinary feature with meaningful interfaces;
- deep: security, data integrity, concurrency, migration, or broad architectural impact.

This review-weight vocabulary guides which existing review lenses and gates to
activate; it does not replace them.

## Knowledge layer

`research-pipeline:knowledge-index` regenerates:

- `knowledge-index-nav.yaml` for compact session orientation;
- `knowledge-index.yaml` for the complete catalog; and
- `knowledge-index-detail.yaml` for rich metadata and relationships.

Frontmatter is authoritative for project docs. Agentic Research analytical
artifacts retain their own schema and are indexed by path, provenance, heading,
and available metadata. Source records (`reference`, `attestation`, `precis`),
scaffold files, and `.import-holding` are excluded.

Both current `.research/analysis/` and legacy `.research/briefs/` /
`.research/programs/` layouts remain discoverable during migration. Never
rewrite or delete a legacy corpus implicitly.

## Quality checkpoint

Before a release, `research-pipeline:quality-checkpoint` sequences the configured
Agile Workflow gates, the fork's infrastructure gate, document review, and the
research citation gate. Findings become `.work/` items.

The citation gate is a thin release adapter over Agentic Research's canonical
lint. Semantic source support and isolated evaluation run inside research
engagements; the release gate does not duplicate them.

Gate errors are blockers. Drain blocking findings through normal Agile Workflow
implementation and review, then rerun the checkpoint.

## Migration and compatibility

- Existing `.work/` projects remain Agile Workflow projects.
- Existing research corpora remain readable and indexed.
- `agentic-research:convert` proposes research migration; the operator confirms
  classification and per-artifact uplift.
- Workbench installation never converts a project.
- Cross-plugin calls use public skill namespaces. CLI adapters resolve the
  companion plugin explicitly and fail clearly when it is missing.

## Completion

An arc is complete when:

1. its acceptance boundary is implemented;
2. relevant tests and gates pass;
3. durable docs and knowledge artifacts reflect the current system;
4. tracked items carry implementation and review evidence;
5. changes are committed and the intended remote branch is current; and
6. any release or publication action has explicit authority.
