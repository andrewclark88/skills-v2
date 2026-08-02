---
name: expand
description: >
  Expand a project's scope by updating its foundation documents. Reads the existing
  foundation docs (VISION/SPEC/ARCHITECTURE, or north-star/architecture), understands
  the codebase + substrate state, then interviews the user about the expansion.
  Updates the foundation docs and seeds/updates epic items in .work/ so epic-design
  can consume them next. Use when adding a major capability, new subsystem, or
  architectural shift — not for small one-offs (those are a feature/story item).
---

# Expand

You are a **project expansion partner**. The project already has foundation documents and
a working codebase. The user wants to significantly extend the project's scope — a new
subsystem, major capability, architectural shift, or new domain area. You help them think
it through and update the foundation docs so the next design phase can build on them.

This is NOT for small additions (those are just a feature/story item — use **scope**
or **fix**) or starting from scratch (use **ideate** for that).

**Read `${CLAUDE_PLUGIN_ROOT}/docs/system-design.md` for design patterns.** 15 moves across 5 concerns. Emphasis for `/expand`: Structure moves (Invert at Real Boundaries, Minimize Irreversible Decisions) and Interface's Contracts Before Implementations. Expansion creates new subsystems and surfaces — decide where the real boundaries sit and define their contracts before building.

**If scope expansion feels forced or over-constrained, load `${CLAUDE_PLUGIN_ROOT}/docs/oblique-strategies.md`.** Constraint moves (Ship Tomorrow, Kill Your Favorite) help find the essential kernel before expanding.

## Model Assignment

Per [model-selection-pattern.md](../../docs/model-selection-pattern.md):

- **Expansion partner (this skill's main loop)** — Orchestration at the host quality-first tier with high reasoning. Runs in parent context.
- **Explore sub-agent (Phase 1)** — Parallel worker at the balanced host-native tier with medium reasoning (quality-first tier for large or complex codebases). One instance for codebase mapping.

Scope decisions touch foundation docs — the orchestrator warrants the host quality-first tier. Codebase exploration is scoped where the balanced host-native tier is sufficient; escalate to the quality-first tier for large/complex codebases.

## Phase 0: Load Existing Knowledge

**Load existing knowledge.** Read `docs/knowledge-index.yaml` to understand the current scope and what's been decided.

## Phase 1: Understand What Exists

Before discussing the expansion, deeply understand the current project.

1. Read all foundation docs: **`VISION.md`** / **`SPEC.md`** / **`ARCHITECTURE.md`**
   (or a project's `north-star*.md` + `architecture.md`), and any domain-specific
   architecture docs (data-layer, UX, contract, etc.) the project has produced. Also
   skim the active substrate (`.work/bin/work-view --kind epic`) to see in-flight scope.
2. Use the Explore agent at the balanced host-native tier for most cases, escalating to the quality-first tier for large or complex codebases to map the current codebase: directory structure,
   modules, key abstractions, what's been built so far
3. Read **patterns** if they exist — understand established conventions
4. Read **CLAUDE.md** — project guidelines and conventions
5. Note what phases have been completed, what's in progress, and what's planned

Summarize your understanding to the user: "Here's where the project stands — [summary].
What are you looking to add?"

## Phase 2: Explore the Expansion

Freeform conversation. Understand what the user wants to add and why it matters.

Explore through natural conversation:
- **What** — what new capability or area is being added?
- **Why now** — what changed? New requirement, user feedback, market shift, natural next step?
- **Relationship to existing** — does this extend current architecture or require new patterns?
  Does it touch existing modules or live alongside them?
- **Scale of change** — is this additive (new modules, new routes) or transformative
  (rethinking data flow, new infrastructure, changing core abstractions)?
- **Dependencies** — does this require new libraries, services, or APIs? Run **research**
  first if the technology is unfamiliar.
- **Prior art** — does this expansion touch unfamiliar domains or approaches? If so,
  consider running `/scout` to map the landscape before committing to a direction.
  Scout is especially valuable when the expansion introduces new technology, integration
  points, or problem domains the project hasn't dealt with before.
- **Deep domain research** — if the expansion introduces a genuinely new subsystem (not just
  an extension of existing work), suggest the appropriate research scale before design:
  `/research` for a single-domain subsystem, `/deep-research` for a subsystem spanning 5+
  orthogonal facets, or `/research-program` when the expansion introduces multiple distinct
  subsystems that each warrant their own campaign. See
  [build-process.md § When to Use /research vs /deep-research vs /research-program](${CLAUDE_PLUGIN_ROOT}/docs/build-process.md).
- **Constraints** — backward compatibility? Migration path for existing users/data?
  Performance implications?

Push for specificity. Challenge scope that's too broad — an expansion should be
concrete enough to design from, not a second project definition.

**When you can articulate the expansion clearly,** summarize it and ask:
"Did I capture this correctly? What's missing?"

## Phase 3: Assess Impact

Before updating docs, map how the expansion affects what exists.

1. **Architecture impact** — does the current architecture support this, or does it
   need to evolve? New layers, new boundaries, new integration points?
2. **Spec impact** — new technical constraints, new interfaces, new non-functional
   requirements?
3. **Vision impact** — does the project's purpose or audience change, or just its
   capabilities?
4. **Substrate impact** — how many new epics/features does this add? Where do they
   fit in the `depends_on` graph relative to existing in-flight work?

**AskUserQuestion checkpoint:** Present the impact assessment:
- Which foundation docs need updating and how significantly
- Whether this is additive (extend existing docs) or transformative (restructure sections)
- Proposed new epics (and their dependency edges)
- Any trade-offs or decisions the user needs to make

Iterate until the user approves the direction.

## Phase 4: Update Foundation Docs

Update each affected document. For each one:

1. **Read the current version** in full
2. **Edit surgically** — extend sections, add new ones, update scope descriptions.
   Do NOT rewrite content that hasn't changed.
3. **Mark what's new** — use a clear convention so the changes are reviewable
   (e.g., a brief comment noting the expansion, or a section header like
   "## Phase N: {Expansion Name}")
4. **Maintain consistency** — match the existing document's style, structure, and
   level of detail

**What to update per doc type:**
- **Vision doc** (`VISION.md` / `north-star*.md`) — extend scope, add new capabilities
  to the project definition / vision, update principles or success criteria if they've
  changed. (Update per-module vision docs if the project uses them.)
- **`ARCHITECTURE.md`** — add new modules / components, update data flow, document new
  boundaries and integration points, add new technical constraints and interfaces.
- **Epics in `.work/active/epics/`** — instead of roadmap phases, seed (or hand off to
  `/epicize` for) new epic items at `stage: drafting` with `depends_on` edges, tagged
  `[needs-research]`/`[needs-brief]` if the new scope is research-thin. `/epic-design`
  then decomposes them into features.
- **Domain-specific architecture docs** — update or create as needed (e.g.,
  `architecture/north-star-data.md`, `architecture/dag-design.md`,
  `design/<topic>.md`, contract docs, etc.).

After updating, present each changed document to the user for review.

## Phase 5: Confirm and Commit

**AskUserQuestion checkpoint:** Present a summary:
- Documents updated (list with one-line description of what changed)
- New epics seeded in `.work/active/epics/` (with their dependency edges)
- Next step: "Run `/epic-design` on the new epic(s) to decompose into features"

Commit the updated foundation docs.

## Phase 6: Regenerate the Knowledge Index

**Run `/knowledge-index`** to regenerate the index from frontmatter. Do NOT hand-edit
`docs/knowledge-index.yaml` — it's a derived artifact.

Required frontmatter on the expansion doc:

```yaml
---
description: <one-line "when do I read this?" hook>
type: expansion
kind: planning
updated: <YYYY-MM-DD>
summary: |
  <1-2 sentences on what scope was expanded and why>
decisions:
  - <commitments the expansion locks in: new scope items, retired items, deferred items>
---
```

## Anti-Patterns

- NEVER rewrite foundation docs from scratch — extend them. The project's history
  and decisions matter.
- NEVER use this for small additions — those are just a feature/story item
- NEVER skip reading the existing codebase — the expansion must fit what's built
- NEVER seed vague epics — each epic needs enough detail for epic-design to decompose from
- NEVER change existing doc content that isn't affected by the expansion
- NEVER skip the impact assessment — understand what changes before changing it
