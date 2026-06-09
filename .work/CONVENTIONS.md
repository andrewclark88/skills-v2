# skills-v2 .work/ conventions

skills-v2 is the plugins monorepo (it *develops* agile-workflow + research-pipeline
+ the others). It now **dogfoods its own substrate**: skills-repo work — new skills,
plugin features, doc/prompt-ware changes, follow-ups — is tracked as items in `.work/`,
not in docs (build-process rule #6: items track work, the roadmap-as-document pattern
is retired).

## Foundation docs (gate-docs checks these for rolling-foundation discipline)

foundation_docs:
  - README.md
  - .claude/CLAUDE.md
  - plugins/research-pipeline/docs/build-process.md

## Release mapping

release_mapping: none

skills-v2 has **no repo-level release**. Each plugin is versioned independently by its
own semver in `plugins/<name>/.claude-plugin/plugin.json` (+ the matching
`.codex-plugin/plugin.json`), bumped via `./scripts/bump-version.sh <plugin> <major|minor|patch>`,
which commits and pushes the bump on its own. The marketplace is a local directory
(`andrewclark88-skills-v2` → this working tree), so consumers pull a plugin's new
version with `claude plugin update <plugin>@andrewclark88-skills-v2 --scope project`.
There is **no CI** — PRs merge manually after review (cross-model `/peer-review` for
high-blast-radius prompt/skill changes; see backlog `cross-model-review-prompt-ware`).

## Gates for release-deploy

gates_for_release:
  - tests
  - cruft
  - docs
  - patterns

skills-v2 work is skill/prompt + Python-tooling authoring; the relevant gates are
tests (e.g. `plugins/research-pipeline/scripts/tests/`, conformance, knowledge-graph
render tests), cruft, docs (rolling-foundation across plugin docs), and patterns.
`security`/`infra` are omitted — skills-v2 ships no deployed infra or secrets surface.
skills-v2 rarely cuts a formal `release-deploy`; per-plugin `bump-version.sh` is the
normal ship path.

## Tag conventions

- `[refactor]` routes feature items to `/agile-workflow:refactor-design`
- `[perf]` routes feature items to `/agile-workflow:perf-design`
- `[needs-brief]` routes epic/feature items through `/research-pipeline:brief` before design
- `[needs-research]` routes through one of `/research`, `/deep-research`, or `/research-program` before brief

## Design-skill routing

design_skill_routing:
  epic_design: research-pipeline:epic-design
  feature_design: research-pipeline:feature-design

skills-v2 develops the research-pipeline plugin and uses its research-grounded,
`[needs-brief]`/`[needs-research]`-gated design skills for its own non-trivial work.
