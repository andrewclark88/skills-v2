# research-pipeline

Research-grounded process overlay for projects using the `agile-workflow`
substrate and the `agentic-research` engine. Adds research-first planning,
architecture rigor, knowledge-index integration, and cascading doc review.

This plugin is **additive**: it does not replace the delivery substrate or the
research engine. It layers project-process skills over both so work reaches the
`.work/` queue with grounded decisions.

`agentic-research` is a required companion and the single authoritative ARD
implementation. The familiar `/scout`, `/research`, `/brief`,
`/deep-research`, and `/research-program` entrypoints are intent profiles that
commission its orchestrator. See [research composition](docs/research-composition.md).

## What's in here

| Layer | Skills |
|---|---|
| **Research intents** | `/research` (bounded question), `/deep-research` (multi-facet decision), `/research-program` (coordinated research arcs) |
| **Prior art** | `/scout` |
| **Foundation docs** | `/ideate` (super-layer: produces VISION/SPEC/ARCHITECTURE + research-plan + PRINCIPLES), `/architecture` |
| **Substrate planning** | `/epicize`, `/epic-design`, `/feature-design`, `/update-epicize`, `/brief` |
| **Quality** | `/doc-review` (cascading), `/quality-checkpoint` (orchestrates 8 gates), `/gate-citations` (research-corpus citation integrity), `/test-quality`, `/security-review` |
| **Lifecycle** | `/init-project`, `/expand`, `/update-documentation`, `/knowledge-index` |
| **Knowledge viz** | `/knowledge-graph` (interactive corpus graph + index-integrity linter; sibling to `agile-workflow:board`) |
| **Auto-loaded** | `/engineering-principles` (code-design), `/build-process` (methodology) |

## Skill catalog

See the [top-level README](../../README.md) for the full catalog.

## Compatibility with agile-workflow

This plugin operates on Nathan Klisch's `agile-workflow` substrate. Same `.work/` format, same frontmatter schema, same `work-view` query tool. On shared projects, our skills check tags (`[needs-brief]`, `[needs-research]`) to decide when to run; his skills ignore them.

**Where we extend his skills**: `gate-infra` is added in
`plugins/agile-workflow/` (his namespace), and our `quality-checkpoint`
orchestrator invokes his gates with optional extension policies. The pipeline's
release-time citation gate is a process adapter over Agentic Research's
authoritative validator; research engagements run the same engine's verification
stack inline.

**Where we don't duplicate**: `implement`, `implement-orchestrator`, `cruft-cleaner`, `bold-refactor`, `repo-eval`, `e2e-test-design`, `extract-patterns`, `refactor-design`, `feature`, `release` — defer to his.

## Naming collisions

Two skills exist in both plugins:
- `/ideate` — ours is the canonical entry for our workflow (produces all Nathan's foundation docs + research-plan + auto-`/scout`). His `/agile-workflow:ideate` remains available but is redundant for our users.
- `/research` — ours is the process-aware entrypoint into Agentic Research; his
  is a single-shot reference helper. Use ours for project-grounded investigation.

Disambiguate via namespace when needed: `/research-pipeline:ideate` vs `/agile-workflow:ideate`.
