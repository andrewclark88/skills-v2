# Build Process

Standard methodology for building projects on the agile-workflow substrate, grounded by the research-pipeline plugin. Follow this process for all new projects and modules. Skills automate each step — see the Pipeline section for the full flow.

Skills are namespaced: `research-pipeline:` (rp — research, planning, design grounding) and `agile-workflow:` (aw — substrate, implementation, gates, releases). Throughout this doc, bare `code-formatted` names refer to the skill in its owning plugin; the namespace is given where ambiguity matters.

## Where This Lives

This document is the source of truth for the methodology. It lives inside the research-pipeline plugin and is referenced, not copied, by every consuming surface.

| File | Scope | Purpose |
|------|-------|---------|
| `~/.claude/CLAUDE.md` | Global — always loaded in every conversation | Hard guardrails. Cannot be dropped even in long sessions. Points here. |
| Project-level `AGENTS.md` (and `CLAUDE.md` symlink) | Loaded when working in a project | The project's substrate overlay. Points here. |
| `${CLAUDE_PLUGIN_ROOT}/docs/build-process.md` | This file | Full methodology, reference, and checklists. Read by every research-pipeline skill at start (`You follow the build process at ${CLAUDE_PLUGIN_ROOT}/docs/build-process.md`). |

If the rules here conflict with a project-level doc, this document wins.

---

## The Pipeline

Every project follows this pipeline. **Work is tracked as markdown items in `.work/`, not as planning documents.** Each item is a file with YAML frontmatter (`id`, `kind`, `stage`, `tags`, `parent`, `depends_on`, `release_binding`, `gate_origin`). Stages advance `drafting → implementing → review → done`, and **every stage transition is a git commit** — git is the audit trail. Releases **bind late**: an item gets a `release_binding` only when `aw:release-deploy` runs.

The item hierarchy replaces the old roadmap-as-document model:
- **Epic** — a multi-feature architectural arc (`rp:epicize` emits these)
- **Feature** — one design + implement cycle, 5-15 units (`rp:epic-design` spawns these)
- **Story** — an independent implementation stride under a feature (`rp:feature-design` may spawn these)
- **Task** — a checklist line in a parent's body (no file)

```
SESSION START (every session on a project with a substrate)
│
├─ knowledge-index nav auto-loads  (docs/knowledge-index-nav.yaml — corpus situational awareness)
├─ substrate snapshot auto-loads   (aw SessionStart hook — items at review, the ready queue, top backlog)
│     └─ run rp:knowledge-index if the nav file is missing or stale
│     └─ query the queue with .work/bin/work-view --ready / --blocked / --kind
│
PROJECT START (truly new project — no foundation docs yet)
│
├─ 1. Define the Project       rp:ideate
│     └─ produces foundation docs: VISION.md, SPEC.md, ARCHITECTURE.md (high-level),
│        PRINCIPLES.md (optional), research-plan.md
│     └─ auto-calls rp:scout (prior art) during ideation
│     └─ for established projects, declare existing docs in .work/CONVENTIONS.md instead
│
├─ 2. Research the Domain      rp:research          (focused topic, one domain)
│                              rp:deep-research     (5+ orthogonal facets)
│                              rp:research-program  (megatopic spanning 3+ domains)
│     └─ produces briefs under .research/ (+ reference skill for rp:research)
│     └─ repeat until all critical domains are understood — assumptions cause rewrites
│     └─ escalation is user-gated: research → deep-research → research-program
│
├─ 3. Design the Architecture  rp:architecture
│     └─ produces docs/architecture.md (modules, data flow, conventions, dependencies)
│     └─ grounded in foundation docs + briefs — no unresearched assumptions
│     └─ run rp:doc-review to verify it matches VISION/SPEC + briefs
│
├─ bootstrap the substrate     aw:convert    (creates .work/, CONVENTIONS.md, AGENTS.md section, work-view)
│
├─ 4. Decompose into Epics     rp:epicize
│     └─ emits EPIC items to .work/active/epics/ at stage:drafting, with depends_on chains
│     └─ tags research-thin epics [needs-research] (campaign needed) / [needs-brief] (curation needed)
│     └─ NOT a roadmap.md — epics are containment shapes, not temporal slots
│
│  ┌── PER EPIC ───────────────────────────────────────────────┐
│  │                                                            │
│  ├─ 5. Brief (if [needs-brief])   rp:brief                    │
│  │     └─ produces a curated domain brief under .research/    │
│  │        / docs/briefs/; gates epic-design                   │
│  │                                                            │
│  ├─ 6. Decompose the Epic         rp:epic-design              │
│  │     └─ spawns FEATURE items to .work/active/features/      │
│  │     └─ writes the realized decomposition INTO the epic body│
│  │     └─ advances the epic drafting → implementing           │
│  │                                                            │
│  │  ┌── PER FEATURE ───────────────────────────────────────┐ │
│  │  │                                                       │ │
│  │  ├─ 7. Design the Feature   rp:feature-design            │ │
│  │  │     └─ writes the design INTO the feature item body   │ │
│  │  │        (interfaces, units, order, tests, risks)       │ │
│  │  │     └─ may spawn STORY items; advances → implementing │ │
│  │  │     └─ [refactor] → aw:refactor-design                │ │
│  │  │        [perf] → aw:perf-design                        │ │
│  │  │        [e2e-test]/[testing] → aw:e2e-test-design      │ │
│  │  │                                                       │ │
│  │  ├─ 8. Build              aw:implement (tiny, ≤~50 LoC)  │ │
│  │  │                        aw:implement-orchestrator (default)
│  │  │     └─ code + tests; advances implementing → review   │ │
│  │  │                                                       │ │
│  │  ├─ 9. Review             aw:review                      │ │
│  │  │     └─ verdict; files findings as items; advances     │ │
│  │  │        review → done (or back to implementing)        │ │
│  │  │                                                       │ │
│  │  └──────────────────────────────────────────────────────┘ │
│  └────────────────────────────────────────────────────────────┘
│
├─ AUTOPILOT (the queue driver — aw:autopilot)
│     └─ picks ready items by depends_on + stage, routes drafting items to the
│        right design skill (epic_design / feature_design via CONVENTIONS.md
│        design_skill_routing, or tag-routed refactor/perf/e2e), delegates
│        implementing → implement-orchestrator and review → review, commits each
│        transition, repeats until the scope is done or blocked
│
├─ QUALITY CHECKPOINT          rp:quality-checkpoint
│     └─ orchestrates the release gate sweep on a bound (or --pending) bundle;
│        each gate emits findings as substrate items, not a pass/fail report
│
├─ RELEASE                     aw:release-deploy <version>
│     └─ binds items to the version, advances release planned → quality-gate,
│        runs the configured gates in CONVENTIONS.md order, waits for all bound
│        + gate-produced items to reach done, ships per release mapping, archives
│        bound items via git mv to .work/releases/<version>/, advances → released
│
│  ┌── ONGOING / AS-NEEDED ───────────────────────────────────┐
│  │                                                          │
│  ├─ aw:scope           → promote backlog ideas into items   │
│  ├─ aw:park            → capture an idea to .work/backlog/   │
│  ├─ aw:fix             → repair a verified bug as a story    │
│  ├─ rp:expand          → scope/foundation change             │
│  ├─ rp:update-epicize  → rescope the epic graph after work   │
│  ├─ rp:update-documentation → align docs to code             │
│  ├─ aw:bold-refactor   → architectural reconception → epic   │
│  ├─ aw:bug-scan        → deep correctness bug hunt           │
│  ├─ aw:repo-eval       → multi-dimensional codebase scoring  │
│  └─ rp:knowledge-graph → corpus graph + index-integrity lint │
│  └───────────────────────────────────────────────────────────┘

KNOWLEDGE INDEX (essential infrastructure, maintained automatically):
  The navigator layer (docs/knowledge-index-nav.yaml) auto-loads at session start.
  Doc-producing skills (rp:ideate, rp:scout, rp:research, rp:deep-research,
  rp:research-program, rp:architecture, rp:brief, rp:expand) emit conformant
  frontmatter and call rp:knowledge-index to regenerate the index.
  Doc-maintaining skills (rp:update-documentation, rp:doc-review) call
  rp:knowledge-index after creating, modifying, or fixing docs.
  rp:knowledge-index also indexes substrate items in .work/ (linted separately
  from docs). The index is fully derived from frontmatter — never hand-edited.
```

---

## Knowledge Index

Every project accumulates knowledge — briefs, architecture docs, research findings, and substrate items. The knowledge index tracks all of it so future sessions know what context is available.

**The knowledge index is essential infrastructure, not optional polish.** Skipping it leads to: duplicated research, contradicted prior decisions, agents flying blind on context that's already available, and architectural drift. Every project past day one should have one, and every session past day one should consult it.

**How it works** — `rp:knowledge-index` regenerates a three-layer model from frontmatter:
- **Layer 1 — `docs/knowledge-index-nav.yaml`** (~5-8KB): auto-loaded at session start within the harness's 10KB hook-output cap. Surfaces corpus counts by `kind`, the 15 most-recently-updated docs, and docs flagged `nav_priority: high`.
- **Layer 2 — `docs/knowledge-index.yaml`**: the terse full per-doc index, read on-demand.
- **Layer 3 — `docs/knowledge-index-detail.yaml`**: the rich layer (summaries / decisions / key_findings / related), read on-demand.

It also globs `.work/active/`, `.work/backlog/`, `.work/releases/`, and `.work/archive/` and indexes substrate items, which have a different frontmatter schema (`id`/`kind`/`stage`/`depends_on`) and are linted separately. An inline lint pass catches drift, broken supersession chains, and missing required fields; the navigator is warned at 8KB and errored at 10KB.

**The index is fully derived from frontmatter.** Sibling skills write conformant frontmatter on the docs they produce; `rp:knowledge-index` regenerates. Nothing else writes to the index files — never hand-edit `knowledge-index*.yaml`.

**Visualize + lint it with `rp:knowledge-graph`.** It renders the index as an interactive browser graph (nodes = docs colored by group; edges = typed `related[]` + directory-containment; supersession chains) and doubles as an integrity linter: it classifies unresolved `related[]` targets (`unindexed` on disk → fix the index / `broken` → fix the slug / `out-of-scope` → expected) and surfaces orphans (docs with no edges). Sibling to `agile-workflow:board` — board shows the work substrate, knowledge-graph shows the knowledge corpus.

**The rules:**
1. **Session start: load it.** The nav layer auto-loads. The agent's first action should be checking what's already known, not searching the codebase.
2. **Before researching: check it.** A `rp:research` invocation should not begin without confirming a relevant brief doesn't already exist.
3. **Before designing: check it.** `rp:epic-design` and `rp:feature-design` read the nav index for `blocks_phase`/`[needs-brief]` context before producing design content.
4. **After writing a doc: regenerate it.** Every doc-producing skill calls `rp:knowledge-index` after writing.

**Doc frontmatter convention:** every indexable doc declares `description`, `type`, `updated`, `summary`, `kind` (often derived from `type`), and either `decisions:` (`kind: planning`) or `key_findings:` (`kind: research`). See `knowledge-index/SKILL.md` for the full schema.

---

## When to Use `/brief` vs `/expand`

Both produce scoping context, but for different purposes:

| Situation | Skill | Why |
|-----------|-------|-----|
| An epic or feature is tagged `[needs-brief]` — domain knowledge is needed before design | `rp:brief` | Domain research for the knowledge layer. Produces a curated brief optimized for agent consumption. Updates the knowledge index. Gates the design pass. |
| You're adding a **new subsystem or capability** that changes the project's scope | `rp:expand` | Larger than a single feature. Updates foundation docs (VISION, ARCHITECTURE) so the next epicize/design pass can build on them. |

**Decision tree:**
- Does this change the project's architecture or scope? → `rp:expand` (then re-`rp:epicize` or `rp:update-epicize`).
- Does designing/implementing an item need domain knowledge research (rules, APIs, protocols)? → `rp:brief`.

Small self-contained work is not a brief or an expansion — it's a feature or story item (create via `aw:scope`), or `aw:fix` for a verified bug.

---

## When to Use `/research` vs `/deep-research` vs `/research-program`

Three scales of the same fractal pattern (same four-role architecture: orchestrator + isolated parallel workers + synthesis + isolated evaluator). All three produce briefs the build process consumes; they differ in breadth, shape, and cost.

| Situation | Skill | Shape | Cost (calibrated) |
|-----------|-------|-------|-------------------|
| Focused topic, one domain, clear question | `rp:research` | Orchestrator + 3-5 Sonnet sub-agents, synthesis in parent | ~$3-5 |
| Topic spans 5+ orthogonal aspects, or decomposition is part of the work, or multi-angle synthesis matters | `rp:deep-research` | Lead + 3-7 Sonnet specialists (parallel, isolated) + spawned Opus Synthesis + spawned Opus Evaluator | ~$6 scoped, ~$12-15 default |
| Megatopic spans multiple distinct domains (3+), each big enough to be its own campaign | `rp:research-program` | Planner + 3-7 Campaigns (each a full `rp:deep-research` tree) + Cross-Campaign Synthesizer + Program Evaluator | ~$35-75 |

**Escalation ladder:** `rp:research` can escalate to `rp:deep-research` when it detects the topic is broad. `rp:deep-research` can escalate to `rp:research-program` when its Lead recognizes the seed is actually a megatopic. `rp:ideate`, `rp:brief`, and `rp:expand` can all call any of the three directly based on the shape of what they need. Escalation is always user-gated.

**Chain mode:** `rp:deep-research --continue-from <parent-campaign-dir>` extends a leaf of a prior campaign — loads parent context, scopes decomposition to the leaf, writes typed cross-references back, appends a child-pointer section to the parent's `parent.md`. Use when a finished campaign's output reveals one leaf turned out to be its own domain. Chains longer than 2-3 links typically mean the topic should have been `rp:research-program` from the start.

**Reuse check:** every scale's Phase 1 checks the knowledge index for existing work. Cite existing briefs and campaigns instead of re-running — saves $6-15 per cited campaign at program scale.

See [`research-skills-overview.md`](research-skills-overview.md) for the full family view (fractal pattern, composition points, isolation rules). Full architectures: [`deep-research-architecture.md`](deep-research-architecture.md), [`research-program-architecture.md`](research-program-architecture.md).

---

## Model Selection

Skills that spawn sub-agents follow the [Model Selection Pattern](model-selection-pattern.md) — four archetypes (orchestration, parallel-worker, synthesis, volume-extraction) with explicit model (Opus/Sonnet/Haiku) and effort recommendations. Each skill's SKILL.md declares its archetype mapping.

**The short version:**
- **Orchestration** (few calls, high stakes — e.g. `rp:architecture`, `rp:epic-design`, `rp:deep-research` Lead) → Opus high
- **Parallel workers** (many parallel, scoped — e.g. research sub-agents, deep-research specialists, design Explore agents) → Sonnet medium
- **Synthesis / judgment** (one call, integrates N inputs) → Opus high
- **Volume / structured extraction** (many calls, well-defined task — e.g. `rp:knowledge-index` regeneration) → Haiku/Sonnet low

Cost impact (calibrated from demos 2026-04-15): a scoped `rp:deep-research` campaign costs ~$6 using the mix, a default campaign ~$12-15, vs ~$50-75 if everything ran on Opus. A 4-campaign `rp:research-program` lands at ~$35-60.

---

## Step Details

### 1. Define the Project (`rp:ideate`)

Interactive workshop. Explore the idea, refine it, produce the **foundation docs** the substrate expects. Auto-calls `rp:scout` for breadth-first prior art discovery — adjacent projects, approaches, and lessons — before committing to a direction.

**Produces** (only docs that don't already exist; never overwrites):
- `docs/VISION.md` — vision, problem, who it's for, non-goals
- `docs/SPEC.md` — capabilities, domain model, constraints, non-functional requirements
- `docs/ARCHITECTURE.md` — **high-level only**: 3-7 module names, data flow sketch, key dependencies, biggest risk
- `docs/PRINCIPLES.md` — decision heuristics (optional; skipped if the user has none to surface)
- `docs/research-plan.md` — domains needing `rp:research` / `rp:deep-research` / `rp:research-program` before architecture firms up
- `scout-landscape.md` — prior art (from the auto-called scout)

**Does NOT produce detailed architecture, epics, or substrate items.** Detailed architecture is `rp:architecture` after research lands; epics are `rp:epicize` after the substrate is bootstrapped.

For established projects with existing nested docs (e.g. `docs/architecture/north-star-*.md`), don't run ideate — declare those as `foundation_docs:` in `.work/CONVENTIONS.md` instead.

### 2. Research the Domain (`rp:research`)

Deep investigation of each domain in the research plan. Use for external systems, protocols, APIs, analytical methods, hardware, regulations — anything the project builds on.

**Produces:** domain briefs under `.research/` + an auto-loading reference skill (for `rp:research`).

**Be aggressive about research.** It's far cheaper to spend a session researching than to discover mid-build that the domain works differently than assumed. If you're not sure whether something needs research, it does. Run it once per domain — don't research everything in one pass. Escalate to `rp:deep-research` / `rp:research-program` per the scale table above.

### 3. Design the Architecture (`rp:architecture`)

Technical design, informed by the foundation docs AND domain briefs. Now you know enough to make real decisions.

**Produces:** `docs/architecture.md` (modules, data flow, conventions, dependencies).

**Prerequisites:** foundation docs and relevant domain briefs MUST exist. If you discover during architecture that a domain isn't understood, stop and run `rp:research` first. Ground every decision in research — not "we'll use X" but "we'll use X because the brief confirmed it fits our constraints."

**After writing architecture.md, run `rp:doc-review`.** Catch contradictions between architecture and the foundation docs / briefs before any epics are built on top of them.

### Foundation Docs & The Item Hierarchy

There are no separate "design docs." Planning lives in two places: **foundation docs** (the durable description of present intent) and **substrate items** (the work). Each has one job; no duplication.

**Foundation docs** (in `docs/`, declared in `.work/CONVENTIONS.md` `foundation_docs:`):
- **VISION** — vision, principles, problem, who it's for, non-goals. Owns the "what and why."
- **SPEC** — capabilities, domain model, constraints, non-functional requirements. Owns the contract surface.
- **ARCHITECTURE** — modules, data flow, conventions, dependencies, cross-cutting design decisions. Owns "how the system is built." Maintained by `rp:update-documentation` as the project evolves. May be a single `architecture.md` or a nested set (e.g. `docs/architecture/north-star-*.md` + `architecture.md` + supplementary cross-cutting docs).
- **PRINCIPLES** — optional decision heuristics.

Foundation docs follow the **rolling-foundation principle**: they describe present intent only. No "previously", "originally", or "in v1.x" prose — git is the audit trail. Historical decision records go to `docs/architecture/history/` with `kind: historical`.

**Substrate items** (in `.work/active/{epics,features,stories}/`) replace the roadmap-as-document model:
- **Epic** — a multi-feature architectural arc. Body is a brief + research references + the realized decomposition (written by `rp:epic-design`). Produced by `rp:epicize`.
- **Feature** — one design + implement cycle (5-15 units). Body accumulates the **design itself** (interfaces, units, order, tests, risks) when `rp:feature-design` runs. Spawned by `rp:epic-design`.
- **Story** — an independent implementation stride under a feature. Spawned by `rp:feature-design` when a feature is multi-stride or has internal parallelism.
- **Release** — orchestration state for a version (`aw:release-deploy`); stage `planned → quality-gate → released`.

Frontmatter (`id`, `kind`, `stage`, `tags`, `parent`, `depends_on`, `release_binding`, `gate_origin`, `created`, `updated`) is validated by every skill that reads or writes items. `depends_on` is sequencing (can't start until listed items are `done`); `parent` is hierarchy. `release_binding` stays `null` until late-binding at release time. Gate-produced items carry `gate_origin`.

**Briefs** (`type: brief`, `kind: research`, under `.research/` or `docs/briefs/`) own curated domain knowledge — facts, research findings, implementation context. Produced by `rp:research` (domain investigation) and `rp:brief` (item-specific context). Indexed by frontmatter, NOT reviewed by `rp:doc-review`.

### 4. Decompose into Epics (`rp:epicize`)

After foundation docs + research + `aw:convert` (substrate bootstrap), decompose the architecture into **epics**.

**Produces:** EPIC items in `.work/active/epics/`, each at `stage: drafting`, with declared `depends_on` chains. Aim for 3-8 epics. Epics are containment shapes (split by capability), not temporal phases — no "Phase 1 / Phase 2." Research-thin epics get a `[needs-brief]` tag so the design pass knows a brief is required first. Epic bodies are briefs + research references, NOT designs.

`rp:epicize` does adaptive grounding: heavy when a `.research/` corpus + knowledge index exist; foundation-doc-only otherwise. After epicizing, the epics are ready for `rp:epic-design` (or an `aw:autopilot` goal).

### 5. Brief (`rp:brief`) — when `[needs-brief]`

If an epic or feature carries the `[needs-brief]` tag, write the brief before designing it. Briefs are curated domain knowledge optimized for agent consumption — not raw research, not architecture, not a tutorial. They answer: "what does the builder need to know to implement this correctly?"

`rp:epic-design` and `rp:feature-design` halt at their Phase 0 knowledge-index check when they see a `[needs-brief]` tag and direct the user to run `rp:brief <topic>` first. This is the gate that enforces "if an item lists a blocking brief, write it before building." For broad topics, `rp:brief` escalates to `rp:deep-research`; for multi-domain programs, to `rp:research-program`.

### 6. Decompose the Epic (`rp:epic-design`)

Designs an epic at `stage: drafting`. Grounds itself in the knowledge index + research corpus + patterns + system-design moves, maps the codebase with parallel Explore sub-agents, surfaces high-level design ambiguities (resolved with the user, or with judgment under autopilot), and runs a pre-mortem.

**Produces:** child FEATURE items in `.work/active/features/` with `parent` + `depends_on` metadata, and a `## Decomposition` section written **into the epic body** (replacing the provisional sketch). Aim for 2-6 child features per epic. Advances the epic `drafting → implementing`. NEVER writes a `docs/designs/epic-*.md` file — the decomposition lives in the item body.

### 7. Design the Feature (`rp:feature-design`)

The feature-level entry point in the design family. Routes by tag: greenfield → this skill; `[refactor]` → `aw:refactor-design`; `[perf]` → `aw:perf-design`; `[e2e-test]`/`[testing]` → `aw:e2e-test-design`.

Grounds itself (knowledge index, parent epic body, foundation docs, research corpus, patterns), maps the codebase, surfaces feature-specific ambiguities, enumerates 2-3 architectural options, designs the trickiest unit first, runs a pre-mortem, and designs the test approach per unit.

**Produces:** the design written **into the feature item body** — `## Architectural choice`, `## Implementation Units` (exact file paths + language-specific signatures + testable acceptance criteria), `## Implementation Order`, `## Testing`, `## Risks`. Spawns child STORY items when the feature is multi-stride or has internal parallelism. Advances the feature `drafting → implementing`. NEVER writes a `docs/designs/<feature>.md` file.

### 8. Build (`aw:implement` or `aw:implement-orchestrator`)

Implement the design embedded in the item body. Output is code AND tests — tests are the contract.

- **`aw:implement`** — inline single-stride implementation for tiny deliveries (≤ ~50 LoC, ≤ 2 files, no coordination). Reads the design from the item body, writes code, runs build + tests, advances `implementing → review`, and records implementation notes in the item body.
- **`aw:implement-orchestrator`** — the **default** path. Builds a `depends_on` graph, bundles related work, chooses wave width and worktree isolation, and dispatches implementation sub-agents (including large non-overlapping write paths when ownership and verification make that safe). Advances parents whose children all reach `stage: review`.

A feature is done when its work passes review and reaches `stage: done` — and ultimately when its PR merges with CI green (see PR & CI Checkpoints).

### 9. Review (`aw:review`)

Reviews an item at `stage: review`. Reads the item's design + implementation notes, runs a code review of the changes, classifies findings (blockers / important / nits), and **files findings as substrate items** with appropriate tags rather than gating on human acknowledgment. Advances the item `review → done` if approved, or back to `implementing` if changes are needed. Autonomous-safe — `aw:autopilot` calls it directly to drain `stage: review` items.

### Autopilot (`aw:autopilot`)

The queue driver. Reads `.work/active/`, picks ready items (every `depends_on` terminal) by `depends_on` count then `created`, and delegates:
- `drafting` epic → `epic_design` (resolved via `.work/CONVENTIONS.md` `design_skill_routing`, default `epic-design`)
- `drafting` feature → tag-routed (`refactor-design` / `perf-design` / `e2e-test-design`) else `feature_design` (default `feature-design`)
- `implementing` non-epic → `implement-orchestrator`
- `review` → `review`

It commits each transition, rebuilds the queue from disk, and repeats until the scope is **complete**, **blocked**, or **interrupted**. A review circuit-breaker escalates items that bounce twice. In `--all` mode it runs a conservative `refactor-design` discovery pass every 5 items advanced to `done`. It never invokes `bold-refactor` (too aggressive for autonomous driving). Projects layered with research-pipeline set `design_skill_routing` to the `research-pipeline:` design skills so the research-grounded, `[needs-brief]`-gated versions win on the autopilot path.

### Quality Checkpoint (`rp:quality-checkpoint`)

Run before binding a release. Orchestrates a sequential gate sweep on one shared bundle (a bound version, or `--pending` for all unbound `stage: done` items), then surfaces a consolidated blocking set. It invokes, **in order**:

1. `aw:gate-security`
2. `aw:gate-tests` (with the spec-driven coverage extension policy from `gate-tests-extension.md` appended)
3. `aw:gate-cruft`
4. `aw:gate-docs` (with the cascading-consistency extension policy from `gate-docs-extension.md` appended)
5. `rp:doc-review` (the narrative cascading pass, running alongside gate-docs)
6. `aw:gate-patterns`
7. `aw:gate-infra`

Each gate **emits findings as substrate items**, not a pass/fail report — Critical/High land at `stage: implementing` (release blockers), Mediums at `drafting`, Lows at backlog. The orchestrator never acts on findings or substitutes its own judgment; it sequences, injects the extension policies, and reports. Gates are idempotent (skip already-tracked findings), so re-running after an `aw:autopilot` drain only emits net-new items. A clean bundle (zero `implementing`/`drafting` gate items) is ready for `aw:release-deploy`.

### Release (`aw:release-deploy <version>`)

Cuts a release in three movements: **bind** items to the version, **gate** the bundle, **ship** when readiness criteria are met.

Reads `.work/CONVENTIONS.md` for the release mapping (`branch-held` / `tag-based` / `release-branch` / `none`) and `gates_for_release` (default order: **security → tests → cruft → docs → patterns → infra**). Interactively binds items, advances the release `planned → quality-gate`, runs the configured gates in CONVENTIONS order, waits until all bound + gate-produced items reach `stage: done`, ships per the mapping, archives bound items via `git mv` to `.work/releases/<version>/`, and advances the release to `released`. Idempotent — safe to re-run after fixing gate findings.

### Ongoing / As-Needed

- **`aw:scope`** — promote a backlog idea or fresh request into the active tier as an epic/feature/story with declared dependencies.
- **`aw:park`** — capture an idea to `.work/backlog/` without derailing current work.
- **`aw:fix`** — diagnose and repair a verified bug as a single-stride story (reproduce → failing test → minimal fix → confirm), landed at `stage: review`. Not for unverified hunches, refactors, or features.
- **`rp:expand`** — extend project scope by updating foundation docs for a new subsystem or capability.
- **`rp:update-epicize`** — rescope the epic graph (splits / merges / archive moves) after a batch of work lands and reality diverges from the plan.
- **`rp:update-documentation`** — align all docs to code after a change. If it touches foundation docs, it triggers `rp:doc-review` for cross-doc consistency. At release time, `aw:gate-docs` enforces the same rolling-foundation principle.
- **`aw:bold-refactor`** — find beautiful cross-cutting simplifications; produces a refactor EPIC with `[refactor]`-tagged child features. User-invocable only.
- **`aw:bug-scan`** — deep multi-angle correctness bug hunt; standalone scored report, or gate mode emitting `gate_origin: bugs` items.
- **`aw:repo-eval`** — multi-dimensional codebase scoring (architecture, code quality, testing, docs, CI/CD, error handling, security, DX, maintainability).

### Doc Review: Cascading Passes (`rp:doc-review`)

`rp:doc-review` uses cascading passes to check consistency at multiple levels — important for multi-module projects where module docs drift from system-level docs.

```
Pass 1: System-Level
  VISION ↔ SPEC ↔ ARCHITECTURE ↔ cross-cutting designs
  → Are these internally consistent? Do they match the code?

Pass 2+: System + Module (one pass per module, discovered dynamically)
  All of Pass 1 + the module's docs
  → Does the module's scope match its epics/features?
  → Does the module's architecture match the system architecture?
  → Are cross-cutting systems referenced correctly?
```

Module discovery is dynamic (scans the knowledge index + `docs/*/architecture/`). It also verifies `[needs-brief]` briefs exist on disk and infrastructure references are accurate. Arguments: no args = full cascade; a module name = system + that module; `--system-only` = system-level only. Runs after `rp:architecture`, after `rp:epicize`, during the quality checkpoint, and when triggered by `rp:update-documentation`.

### Pre-Deploy Security Review (`rp:security-review`)

Standalone comprehensive audit (distinct from the release-time `aw:gate-security`). Discovers the stack, lets you choose focus domains (auth, injection, secrets, dependencies, API, infra, crypto, data protection, error handling), researches current best practices, and produces a scored markdown report with severity-classified findings. Address all Critical and High findings before deploying; track Mediums.

---

## Working Principles

- **Items, not docs, track work.** Substrate items in `.work/` are the source of truth for work decomposition. The roadmap-as-document pattern is retired.
- **Rolling-foundation: docs describe present intent.** No "previously", no "originally", no "in v1.x" prose. Git is the audit trail. Historical decision records go to `docs/architecture/history/`.
- **Each planning doc has one job.** VISION owns the why, SPEC owns the contract, ARCHITECTURE owns the how, epics own work decomposition, the feature body owns its design. Don't duplicate.
- **Late-binding releases.** Bind items to a version only when running `aw:release-deploy`. Don't pre-bind.
- **Data-driven over hand-curated.** When there's a data source, build a pipeline. Don't manually curate what can be automated.
- **Repeatable processes.** Pipelines should re-run (new data, new releases, meta shifts). One-off scripts become recurring commands.
- **Auto-generate, then enrich.** Generate what you can from existing data, layer in external sources, leave TODOs only for things requiring human judgment.
- **Don't hand-write what can be researched.** Use `rp:research`, web search, API exploration, and data analysis before asking for manual input.

---

## Loop Exit Gates: External Verifier Required

**Any loop that converges on a quality criterion — auto-fix loops, evaluator passes, gate verifications — MUST delegate the exit decision to a separately-dispatched verifier in a fresh context. The orchestrator's self-confidence is not an exit gate. This is non-negotiable across all skills.**

This rule applies to (non-exhaustive list):

- `rp:doc-review`'s auto-fix loop (re-audit dispatched as Sonnet Agent every iteration)
- `rp:deep-research`'s evaluator pass (Opus Agent, isolated context)
- `rp:research-program`'s program-level evaluator
- `rp:security-review`'s severity verification
- Any future loop skill that converges on quality criteria

### Why this is structural, not stylistic

The orchestrator (the skill's main loop) is the same context that just produced the fixes / findings. It has motivated reasoning to declare the work done — token economy, fatigue, completion bias. **The orchestrator cannot verify itself.**

A separately-dispatched verifier in a fresh context has none of those biases. It reads only the inputs (briefs / docs / fixes) and produces a structured verdict. The exit decision is then mechanical: read the verdict's severity counts, exit if 0/0, otherwise iterate.

### Concrete pattern (applies to all loop skills)

For every iteration of a quality-convergence loop:

1. Apply fixes (orchestrator may do this directly or via dispatched fix agent).
2. **Dispatch a fresh verifier Agent.** New context, given only the inputs needed to verify. Required — this step is non-negotiable.
3. Verifier produces a structured report with severity counts (or equivalent quality signal).
4. **Read the verdict from the report.** Exit decision is mechanical: if severity counts indicate convergence (0 Critical, 0 High; or score ≥ threshold), exit. Otherwise iterate.
5. The orchestrator does NOT make the exit call from its own assessment, grep, spot-check, or "it looks fine."

### Anti-patterns explicitly forbidden

- Orchestrator manually grepping for the patterns the previous verifier flagged and declaring success
- Orchestrator spot-checking edited files and declaring "they look right"
- Orchestrator exiting the loop on its own confidence ("I'm sure that fixed it")
- Orchestrator skipping the verifier dispatch for token-economy reasons
- Orchestrator re-using a stale verifier output from a previous iteration

### Why this matters

Skill rules that say "re-run the audit" without enforcing structural separation can be violated by an orchestrator interpreting the rule loosely. Making the verifier-dispatch a required Agent call (visible in the tool-call trace) makes shortcut exits structurally observable. The cost of one extra dispatched audit is far less than the cost of an undetected regression.

---

## Thinking Layer

The pipeline's thinking-heavy skills (`rp:research`, `rp:deep-research`, `rp:research-program`, `rp:ideate`, `rp:architecture`, `rp:brief`, `rp:epicize`) load a first-principles thinking primer before starting work. The primer provides 10 concrete thinking moves organized in four phases:

1. **Open** — decompose the problem, question deeply, doubt what you know
2. **Challenge** — invert the problem, seek falsification, trace consequences
3. **Synthesize** — find leverage points, apply multiple lenses
4. **Verify** — test your understanding, check your thinking mode

**The Asymmetry Principle:** The cost of not going deep enough is much higher than the cost of going too deep. When in doubt, go deeper.

**For `rp:deep-research` specifically**, the thinking layer is load-bearing across three phases:
- **Decomposition** (Open + Synthesize) — faceted decomposition is the highest-leverage decision in a campaign; a bad tree wastes specialists × token budget on wrong questions
- **Stopping decisions** (Challenge + Verify) — falsify your confidence that each leaf is truly a leaf; test the decomposition by trying to find what's missing
- **Synthesis** (Challenge + Synthesize) — invert the campaign ("what would make these briefs useless?"), find leverage in cross-references, check for contradictions rather than smoothing them over

See [`first-principles.md`](first-principles.md) for the full primer and per-skill emphasis table.

## System Design Layer

The pipeline's design-heavy skills (`rp:architecture`, `rp:epic-design`, `rp:feature-design`, `rp:brief`, `rp:expand`) load a system design primer before starting work. The primer provides 15 concrete design moves organized across five concerns:

1. **Structure** — start monolith, invert at real boundaries, minimize irreversible decisions
2. **Interfaces** — contracts before implementations, match API to consumer, evolve additively
3. **Data** — normalize first, per-feature consistency, cache deliberately
4. **Scale** — idempotent operations, stateless services, scale vertically first
5. **Reliability** — instrument from day one, design for failure, validate at boundaries

**The Earn-Your-Complexity Principle:** 12 of the 15 moves are design-in (cheap to include from the start, expensive to retrofit). 3 are earn-in (add only with measured evidence). When in doubt, keep it simple.

The system design primer complements the first-principles thinking primer: first-principles teaches *how to think*; system-design teaches *how to design*. Skills that do both (like `rp:architecture`) load both. Epic-design emphasizes Structure moves (epic boundaries are the highest-leverage decision); feature-design emphasizes Interface and Data moves.

See [`system-design.md`](system-design.md) for the full primer and per-skill emphasis table.

---

## Infrastructure Safety Practices

These apply whenever a project deploys to shared cloud infrastructure (GCP, AWS, etc.). The goal: **never destroy or interfere with resources you don't own.** At release time, `aw:gate-infra` audits the bundle for violations of these rules and emits findings as items.

### Terraform Rules

**Never apply locally.** Local `terraform apply` has no review, no audit trail, and no guardrails against destroying someone else's resources.

| Action | Where it runs | When |
|--------|--------------|------|
| `terraform init` | Local or CI | Anytime (safe, idempotent) |
| `terraform plan` | Local or CI | Anytime — review the plan carefully |
| `terraform apply` | **CI only, on merge to main** | After plan is reviewed and approved in PR |
| `terraform destroy` | **Never without explicit approval** | Requires manual confirmation + team review |

**Remote state is mandatory.** Terraform state must be stored in a remote backend (GCS bucket, S3, Terraform Cloud) with state locking enabled. Never commit `.tfstate` files to git.

```hcl
terraform {
  backend "gcs" {
    bucket = "<project>-terraform-state"
    prefix = "<service-name>"
  }
}
```

**State lock prevents concurrent applies.** If two CI jobs try to apply at the same time, the lock prevents conflicts. Never use `-lock=false`.

### Shared Project Safety

When deploying into a GCP project (or AWS account) that other teams use:

**Prefix all resources.** Every resource your project creates should be namespaced:
- GCS buckets: `<project-name>-<purpose>` (e.g., `myproject-briefs`)
- Service accounts: `<project-name>-<role>` (e.g., `myproject-server`)
- Secrets: `<project-name>-<secret>` (e.g., `myproject-bearer-token`)
- Cloud Run services: `<project-name>` (e.g., `myproject`)

**Never use wildcard IAM.** Don't grant project-level `roles/owner` or `roles/editor` to service accounts. Use the narrowest role on the specific resource.

**Import before managing.** If a resource already exists (someone created it manually), `terraform import` it into your state before writing the `.tf` file.

**Use `prevent_destroy` on critical resources:**

```hcl
resource "google_storage_bucket" "data" {
  lifecycle {
    prevent_destroy = true
  }
}
```

**Tag everything.** Add labels to all resources so ownership is clear:

```hcl
labels = {
  managed_by = "terraform"
  project    = "<project-name>"
  team       = "data"
}
```

### Secrets

**Never in code.** Secrets (API keys, tokens, passwords) never appear in:
- Source code (`.ts`, `.py`, `.tf` files)
- Terraform state committed to git
- Environment variable files committed to git (`.env`)
- CI/CD logs

**Where secrets live:**
- GCP Secret Manager (for deployed services)
- Local environment variables (for development)
- CI/CD secret store (GitHub Actions secrets, etc.)

### Pre-Flight Checklist (Before First `terraform apply`)

- [ ] Remote state backend exists (GCS bucket for state)
- [ ] State bucket has versioning enabled
- [ ] CI/CD pipeline is configured for plan-on-PR, apply-on-merge
- [ ] All resources are prefixed with project name
- [ ] IAM bindings are scoped to specific resources (not project-wide)
- [ ] Secrets are in Secret Manager (not in code or `.tfvars` committed to git)
- [ ] `prevent_destroy` is set on any resource that would be catastrophic to lose
- [ ] All resources have ownership labels
- [ ] Team has reviewed the initial `terraform plan` output

---

## PR & CI Checkpoints

**All code goes through PRs.** No direct pushes to main for application code or infrastructure.

### Application Code PR Pipeline

```
PR opened/updated:
  → Build (compile, lint)
  → Run full test suite
  → Docker build (verify the deployable image still builds)
  → All checks must pass before merge is allowed

Merge to main:
  → Same checks run again
  → (After deploy phase) Deploy
```

### Infrastructure PR Pipeline

```
PR opened/updated:
  → terraform init
  → terraform plan
  → Post plan output as PR comment
  → Require approval before merge

Merge to main:
  → terraform init
  → terraform plan (again, to catch drift)
  → terraform apply -auto-approve
```

### Branch Protection Rules

| Rule | Required |
|------|----------|
| PRs required before merge to main | Yes |
| At least 1 approval (or self-review for solo projects) | Yes |
| CI checks must pass | Yes |
| No direct pushes to main | Yes |
| No force pushes to main | Yes |

### What CI Checks Per Item

Each feature/story ships tests. CI runs them all, not just the new item's tests — the full suite is the regression gate. An item isn't truly done until its PR merges with CI green; reaching `stage: done` locally is not enough.

| Check | When | Why |
|-------|------|-----|
| Build/compile | Every PR | Catch type errors, syntax issues |
| Unit tests | Every PR | Item acceptance + regression |
| Docker build | Every PR | Verify the deployable image works |
| Terraform plan | Infra PRs only | Review before apply |
| Lint (if configured) | Every PR | Code quality |

---

## Git Practices

- **Stage transitions are commits.** Every `drafting → implementing → review → done` advance commits the item file (and any code) — git is the substrate's audit trail.
- **Commits are small and focused.** One logical change per commit.
- **PRs before merge.** No direct pushes to main. Code review required.
- **Don't commit generated files.** Data caches, build outputs, `.env` files, `.tfstate` — all gitignored.
- **Don't commit secrets.** Ever. Use pre-commit hooks or CI checks to catch accidental secret commits.

---

## Skill Reference

Namespace: `rp` = `research-pipeline:`, `aw` = `agile-workflow:`.

| Skill | When | What it produces |
|-------|------|-----------------|
| `rp:knowledge-index` | Start of every session; after any doc/item change | Three-layer index (nav + terse + detail) derived from frontmatter; lint pass |
| `rp:init-project` | Brand-new project lacking docs/ scaffolding | Copies the canonical docs/ + rules template; points at `aw:convert` then `rp:ideate` |
| `rp:ideate` | Project start | Foundation docs (VISION, SPEC, ARCHITECTURE high-level, optional PRINCIPLES, research-plan) + scout auto-call |
| `rp:scout` | Auto-called during ideate + standalone + from expand | Landscape brief (prior art) + research recommendations |
| `rp:research` | Domain research; before any work using unfamiliar tech | Domain brief + auto-loading reference skill |
| `rp:deep-research` | Topic spans 5+ orthogonal facets; `--continue-from` for chain mode | N cross-referenced briefs + parent synthesis + quality report |
| `rp:research-program` | Megatopic spanning 3+ distinct domains | Program directory (plan + super-parent + N campaigns + program evaluation) |
| `rp:architecture` | After foundation docs + domain briefs | `architecture.md` — modules, data flow, conventions, dependencies |
| `aw:convert` | After architecture, before epicize | Bootstraps `.work/`, CONVENTIONS.md, AGENTS.md section, work-view; or syncs an existing substrate |
| `rp:epicize` | After architecture + substrate bootstrap | EPIC items in `.work/active/epics/` with `depends_on` + `[needs-brief]` tags |
| `rp:brief` | An epic/feature is tagged `[needs-brief]` | Curated domain brief; gates the design pass |
| `rp:update-epicize` | After a batch of work, when scope shifted | Rescoped epic graph (splits/merges/archive moves) |
| `rp:epic-design` | An epic at `stage: drafting` | Child FEATURE items + `## Decomposition` in the epic body; advances epic → implementing |
| `rp:feature-design` | A greenfield feature at `stage: drafting` | Design written into the feature body (units/order/tests/risks) + child STORY items; advances → implementing |
| `aw:refactor-design` | A `[refactor]` feature at `stage: drafting`; or discovery scan | Refactor plan in the feature body + child stories; or emitted items |
| `aw:perf-design` | A `[perf]` feature at `stage: drafting`; or discovery profiling | Perf plan + benchmark scaffolds in the feature body; or emitted items |
| `aw:e2e-test-design` | A `[e2e-test]`/`[testing]` feature; `--bootstrap`/`--audit` | Service-mocked e2e design in the feature body + child stories |
| `aw:implement` | Tiny inline delivery (≤~50 LoC, ≤2 files) | Code + tests; advances item implementing → review |
| `aw:implement-orchestrator` | Default implementation path; any non-tiny work | Code + tests via bundled/parallel sub-agents; advances parents when children reach review |
| `aw:review` | An item at `stage: review` | Verdict + findings filed as items; advances review → done or back to implementing |
| `rp:update-documentation` | After a non-trivial code change | Docs synced to code; triggers `rp:doc-review` if foundation docs changed |
| `rp:doc-review` | After architecture/epicize; quality checkpoint; major design changes | Cascading consistency report; verifies docs match code + briefs exist |
| `rp:quality-checkpoint` | Before binding a release | Orchestrates the gate sweep (security → tests → cruft → docs + doc-review → patterns → infra); consolidated blocking set; findings emit as items |
| `aw:gate-security` | Release-deploy / quality-checkpoint | Security findings as `gate_origin: security` items |
| `aw:gate-tests` | Release-deploy / quality-checkpoint | Spec-derived coverage-gap findings as `gate_origin: tests` items |
| `aw:gate-cruft` | Release-deploy / quality-checkpoint | Dead-code / bloat findings as `gate_origin: cruft` items |
| `aw:gate-docs` | Release-deploy / quality-checkpoint | Rolling-foundation drift findings as `gate_origin: docs` items |
| `aw:gate-patterns` | Release-deploy / quality-checkpoint (last) | Reusable patterns extracted to `.agents/skills/patterns/`; `gate_origin: patterns` tracking item |
| `aw:gate-infra` | Release-deploy / quality-checkpoint | Infra-safety findings (Terraform drift, secrets, missing CI gates) as `gate_origin: infra` items |
| `aw:release-deploy` | Cut a release | Binds items, runs gates in CONVENTIONS order, ships, archives bound items to `.work/releases/<version>/` |
| `aw:autopilot` | Drain the ready queue autonomously | Routes drafting → design, implementing → orchestrator, review → review; commits transitions until done/blocked |
| `aw:scope` | Promote backlog/fresh ideas into tracking | Epic/feature/story items with declared dependencies |
| `aw:park` | Capture an idea without derailing | Backlog item at `.work/backlog/<id>.md` |
| `aw:fix` | A verified bug | Single-stride story (failing test → minimal fix) at `stage: review` |
| `rp:expand` | Scope/foundation change for a new subsystem | Updated foundation docs |
| `aw:bold-refactor` | Suspect a fundamental simplification (user-invocable only) | Refactor EPIC with `[refactor]` child features |
| `aw:bug-scan` | Deep correctness bug hunt | Scored report (standalone) or `gate_origin: bugs` items (gate mode) |
| `aw:repo-eval` | Holistic codebase evaluation | Verified 1-10 scorecard across 9 dimensions + prioritized recommendations |
| `rp:test-quality` | Spec-driven coverage analysis (standalone) | Tests derived from contracts/specs, not from existing code |
| `rp:security-review` | Pre-deploy standalone audit | Scored security report with severity-classified findings |
| `rp:knowledge-graph` | Visualize / audit the knowledge corpus | Interactive browser graph (typed + containment edges) + index-integrity QA (unindexed / broken / orphan / superseded) |
