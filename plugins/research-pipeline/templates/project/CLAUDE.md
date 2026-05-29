# {{PROJECT_NAME}}

<!-- One-line description — fill in after /ideate produces the north star. -->

## Start every session
The terse `docs/knowledge-index.yaml` auto-loads at session start (terse layer of the two-layer index — surfaces every doc's title, type, kind, and consumer_hint). For full per-doc detail (summary, decisions, key_findings), read `docs/knowledge-index-detail.yaml` on demand.

When you've added or modified docs, run `/knowledge-index` to regenerate both layers from frontmatter. **Do not hand-edit `knowledge-index.yaml` or `knowledge-index-detail.yaml`** — they're derived artifacts.

## Frontmatter convention
Every doc this project produces (VISION / north-star, architecture, brief, program synthesis, etc.) ships with structured frontmatter:

- `description:` — "when do I read this?" hook (becomes consumer_hint in the terse index)
- `type:` — north-star | architecture | brief | program-parent | program-report | features
- `summary:` — 1-2 sentences on what's in the doc
- `decisions:` — required for `kind: planning` (5-9 highest-leverage commitments)
- `key_findings:` — required for `kind: research`
- `kind:` — usually derived from `type:` + `status:`; set explicitly to override
- `updated:` — YYYY-MM-DD

See the `research-pipeline:knowledge-index` skill for the full schema and field semantics.

## Build process
Follow the global methodology in the `research-pipeline:build-process` skill. Work is tracked as items in `.work/` (created by `/agile-workflow:convert`), not as roadmap docs; per-feature designs live in the item body. Project knowledge lives under:

- `docs/architecture/` — foundation docs (VISION / SPEC / ARCHITECTURE), conventions; `history/` for frozen records
- `docs/briefs/` — curated domain briefs from `/brief`
- `.research/` — `/research` / `/deep-research` / `/research-program` outputs (created by those skills)

Parent `CLAUDE.md` files ship the pipeline and shared key rules — do not duplicate them here. This file is for project-specific context only.
