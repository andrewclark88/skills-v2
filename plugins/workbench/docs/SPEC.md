# Specification: Workbench

## Authority boundaries

```text
.work/
├── CONVENTIONS.md
├── active/.gitkeep
├── active/<id>.md
├── backlog/.gitkeep
├── backlog/<id>.md
├── completed/.gitkeep
├── completed/<id>.md
├── releases/.gitkeep
└── releases/<version>.md

.research/
├── CONVENTIONS.md
├── attestations/.gitkeep
├── attestations/<handle>.md
├── briefs/.gitkeep
├── briefs/<id>.md
└── bibliography.yaml

.knowledge/index.json
.mockups/<item-id>/index.html
docs/<repository-wide foundations>
docs/<sub-project>/<scope-owned foundations>
<sub-project>/docs/<scope-owned foundations>
AGENTS.md
```

- `.work/` records outcomes the project may decide and deliver.
- `.research/` records externally fetched evidence and grounded synthesis.
- Foundation documents record current or explicitly intended project truth.
- `.knowledge/index.json` is committed discovery metadata with no independent
  authority.

Workbench and agile-workflow are mutually exclusive `.work/` owners.

## Work conventions

`.work/CONVENTIONS.md` begins with:

```yaml
---
owner: workbench
schema: 1
completed_items: summarize|discard
---
```

Setup always asks the user how completed items should be retained and aligns
repository-specific conventions. It may recommend conventions from repository
evidence, including parking useful out-of-scope findings and behavior-focused
testing, but writes no new convention without confirmation.

## Active items

```yaml
---
id: <stable-kebab-id>
kind: epic|feature|story
status: active|blocked
tags: []
parent: null
blocked_by: []
related_to: []
research_refs: []
mock_refs: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Hierarchy expresses durable outcome structure. `blocked_by` names active
prerequisites; `related_to` carries non-blocking context. An external blocker
uses an exact `## Blocker` section naming the condition and how it clears.
Focused audits, cleanup, and refactors use tags rather than new item kinds.

## Completion

Completed work never remains active.

- `completed_items: summarize` replaces an active item with a compact
  `.work/completed/<id>.md` outcome stub.
- `completed_items: discard` removes the active item after verification.

Before closure, remaining active relationships are reconciled and active
children are completed. `release` may collapse selected completion stubs into
one `.work/releases/<version>.md`; it does not tag, publish, or deploy.

## Work behavior

`work` keeps a clear request in one workflow even when it requires requirements,
design, implementation, review, integration, or several epics. It asks the
human at least one focused question about consequential choices, pauses for the
answer, and continues until the full named boundary is complete or externally
blocked.

If the outcome, ownership boundary, or success shape cannot yet form coherent
work, `work` routes through `ideate`. Ideate preserves a no-write boundary until
the user selects a Workbench, backlog, research, or foundation handoff.

Standalone cleanup, simplification, and refactoring are ordinary bounded work.
Behavior-preserving cleanup may travel with a delivery when cohesive; intended
behavior changes require explicit requirements.

Verification targets stable interfaces and meaningful user journeys. A test
must protect enough behavior, contract, boundary, risk, or regression to justify
its maintenance cost. Fresh-context or cross-model review is used when
independent judgment is materially valuable, and findings are verified before
acceptance.

## Research

An attestation uses:

```yaml
---
source_handle: <lowercase-kebab-handle>
fetched: YYYY-MM-DD
source_title: <title>
source_url: <absolute-http-or-https-url>
---
```

Attestations contain source-faithful summaries and numbered citable details
under `## Attested details`. They do not contain project recommendations.
Repository files are project context and are not represented as external
attestations.

Briefs cite details as `[handle]{N}`, distinguish source claims from inference,
preserve contradictions, and always include `## Disconfirming evidence`.
Research may use specialist fan-out only when every specialist receives the
full discipline, owns and lints its evidence, and the lead owns cross-source
synthesis.

After interactive research, the skill may ask whether genuinely reusable
guidance should become a project skill. It never promotes a skill autonomously
or without explicit approval.

## Knowledge index

`build-knowledge-index.py` indexes root and sub-project documentation,
`.research/**/*.md`, and `.work/**/*.md`. It emits byte-stable JSON, rejects
duplicate namespace/id pairs and unresolved relationships, generates the
bibliography, and checks committed freshness with `--check`.

Allowed knowledge relationships are `supports`, `contradicts`, `informs`, and
`supersedes`. Work hierarchy and scheduling continue to use `parent`,
`blocked_by`, and `related_to`.

## Setup conversion

Setup inventories any existing workflow semantically, aligns conventions with
the user, maps useful truth to the canonical destinations, validates retained
content block by block, rewrites inbound references, and only then removes
superseded artifacts.

Every removal target is classified as clean tracked, modified tracked,
untracked, ignored, or otherwise unrecoverable. Clean tracked content is
recoverable from Git. Removing other content requires a pre-state commit or the
user's exact-list confirmation.

Setup removes repository-scoped competing workflow plugins after conversion and
reports user- or machine-scoped competing installs for the user to uninstall.
It creates no migration archives, compatibility copies, `.bak` files, or legacy
folders. A second run produces no material change.

## Deterministic validation

`validate-workbench.py` checks ownership, canonical directories and clone-stable
markers, item schemas, globally unique ids, active relationships, blocker
evidence, research and mock references, and superseded substrate paths.

`lint-research.py` checks attestation metadata, external URL safety, sensitive
markers, mandatory attested-detail and disconfirming sections, and citation
resolution. `build-knowledge-index.py --check` rejects stale committed output.
