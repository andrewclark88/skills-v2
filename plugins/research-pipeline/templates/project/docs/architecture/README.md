# Architecture

Repo-level planning docs live here.

- **`north-star-{{PROJECT_NAME}}.md`** (or `VISION.md`) — vision, principles, domain model (produced by `/ideate`)
- **`architecture.md`** — modules, data flow, conventions (produced by `/architecture`)
- **`conventions.md`** — directory layout, naming, cross-module rules (hand-written, updated as the project matures)
- **`history/`** — frozen records (superseded plans, decision logs) kept out of the rolling foundation

Work decomposition lives in the `.work/` substrate (epics → features → stories via `/epicize` → `/epic-design` → `/feature-design`), not a `roadmap.md`.

Every doc should carry the standard frontmatter (`description`, `type`, `updated`) so `/knowledge-index` can catalog it.
