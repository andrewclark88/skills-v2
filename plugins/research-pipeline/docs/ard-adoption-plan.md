---
description: "Plan for adopting ARD (Agentic Research Discipline) verification into research-pipeline — Option A: vendor ARD's liftable kernel (anti-fabrication floor + attestation/[handle]{N} citation chain + citation lint) as a verification adapter, keeping our orchestration/tiers/knowledge layer. Phase 0 decisions locked; Phases 1-2 shipped (chain across all producers + vendored research-discipline); Phase 3 in progress (gate-citations + re-sync procedure). Peer-reviewed (Codex)."
type: architecture
updated: 2026-06-09
---

# ARD Adoption Plan (Option A)

*Last updated: 2026-06-08*

> How research-pipeline gains machine-checkable anti-fabrication by vendoring the
> liftable kernel of **ARD** (Agentic Research Discipline, upstream's
> `agentic-research` plugin), **without** installing that plugin, adopting its Rust
> `research-view` binary, or replacing our orchestrators. This doc records the
> decision rationale, the locked Phase 0 design, and the downstream phases.

## Why (the gap this closes)

research-pipeline is strong at research *production* (the `/research` →
`/deep-research` → `/research-program` scale tiers, `/scout`, `/brief`, the
knowledge-index/graph reuse loop) and at pipeline integration (ideate → … →
release). Its weakness is **grounding rigor**: sourcing is a `## Sources` section
by convention, with isolated LLM-judge evaluators only at the deeper tiers. There
is no machine-checkable binding from a claim to the source that supports it.

ARD's core strength is exactly that: a non-erodable anti-fabrication floor plus a
**citation chain** `claim → [handle]{N} → attestation file → actually-fetched
source`, mechanically checked by a zero-dependency Python lint. ARD's published
adoption model is "pin, don't fork — vendor the liftable kernel verbatim, cite the
spec by section." Lifting that kernel into research-pipeline closes our gap with
no `.research/` layout collision, no orchestrator redundancy, and no Rust binary.

Options B (install agentic-research alongside and reconcile two `.research/`
layouts + two orchestrators) and C (replace our research skills with ARD's, losing
our scale tiers / chain mode / knowledge-index reuse loop) were rejected. See the
session memory `agentic-research-vs-research-pipeline` for the full comparison.

## Reframe (from the cross-model review)

A Codex peer-review of the first draft produced one load-bearing correction:
**the lint/gate is the part with teeth; the prose floor is dispatch content that
supports the gate, not the gate itself.** The lint is also **syntactic, not
semantic** — it proves a `[handle]{N}` resolves to an attestation with provenance
(plus thin-attestation and surface-pattern flags), but it does **not** verify that
claim *N* is actually supported by the cited passage. That support check is the
**adversarial-reader** pass (`skills/adversarial-reader/`, which reads the attestation
passages), with the isolated evaluators catching fabrication-smell/coverage. The three
are complementary: **lint = chain resolves; adversarial-reader = passage supports the
claim; isolated evaluator = fabrication-smell, blind to sources.** See build-process.md
§ Quality Checkpoint for the full three-check model.

## Scope vendored from ARD (pinned to ARD v0.4.1)

| Piece | From ARD | Lands as |
|---|---|---|
| Anti-fabrication floor (6 discipline sections) | `skills/research-discipline/SKILL.md` | dispatch content inlined into authoring prompts (see propagation note) + an auto-loading reference skill |
| Attestation + INDEX templates, `[handle]{N}` wire-form | `templates/{attestation,INDEX}.md` | research-pipeline templates referenced by the research skills |
| Citation-chain lint + schema + pattern data | `scripts/lint-citations.py`, `scripts/schema/`, `catalogs.json` | `plugins/research-pipeline/scripts/` (+ a Bash-capable `citation-lint` skill) |
| `ard.json` pin + (optional) conformance fixtures | `ard.json`, `scripts/conformance/` | pin record + a guard that the vendored lint still matches ARD on re-sync |

**Explicitly out of scope:** the agentic-research plugin install, the `research-view`
Rust binary (we keep knowledge-index/graph as the query layer), and ARD's
`research-orchestrator` (we keep our scale tiers).

## Locked decisions (Phase 0)

These three were decided deliberately to keep long-term options open at minimal
present cost.

### D1 — `.research/` layout: compose beneath, with a configurable analysis dir

Keep our synthesis-centric tree as the **analysis tier**; add ARD's source tiers
beneath it:

```
.research/
  reference/<corpus>/INDEX.md      # NEW — numbered, append-only bibliography
  attestation/<handle>.md          # NEW — per-source attestation (provenance + quotes)
  briefs/<topic>/parent.md         # OURS — analysis tier (now cites [handle]{N})
  programs/<slug>/...              # OURS — analysis tier, unchanged structure
```

We do **not** migrate to ARD's `.research/analysis/{briefs,campaigns}` naming.
Rationale: the lint cares only about `attestation/` + `[handle]{N}`, **not**
analysis-tier directory names, so strict ARD parity is cosmetic for the
verification goal — and migrating would be a *data migration* of every existing
project's research corpus plus a wide silent-break surface (consumers read exact
paths: `epicize` / `epic-design` / `feature-design`, `render.py` prefix
special-casing, `gate-docs-extension`, `normalize_slug`). To keep migration a
cheap future option rather than foreclosing it, **the citation lint takes
`--analysis-dir`** so the analysis root is configurable; flipping to ARD's layout
later becomes a config change, not a rewrite.

### D2 — Source tiers are tracked by their own tooling, not the docs index

`reference/`, `attestation/`, and `precis/` are **excluded** from the
knowledge-index navigator, the knowledge-graph default scan, and the docs
`updated:`-bump hook. They are not navigable knowledge docs (you read the *brief*,
never the attestation), and they carry a different frontmatter schema
(`source_handle`/`fetched`/`source_url`/`provenance`, not
`description`/`type`/`updated`) that the docs lint would reject.

Excluding them is **not losing them**: the **`citation-lint` is their tracker** —
it inventories attestations and validates the claim→attestation→source chain
(orphan attestations = cited nowhere; briefs with no attestation = ungrounded).
This mirrors how `.work/` substrate items are already routed separately by schema
(`discover_substrate()`), rather than forced into the docs schema.

**Fast-follow (post-Phase-0):** add an attestation **evidence-node class** to the
knowledge-graph so the source layer is *visible* beneath briefs (brief→attestation
containment edges) without being schema-linted as docs. This honors the "see them,
don't lose them" intent once attestations actually exist to visualize.

### D3 — Explicit `slug:` frontmatter now, path-derivation as fallback

Research outputs gain an explicit `slug:` frontmatter field as their canonical id;
when absent, the id derives from the directory name (e.g.
`.research/briefs/auth-providers/` → `auth-providers`).

Rationale: an explicit slug is **the hedge that makes D1 safe** — paths can change
(if we ever take the `--analysis-dir` migration), but a stable slug means
`research_refs` / `research_origin` links survive. Derive-from-path would rewrite
every slug on any layout change and break every reference. The cost of getting
this "wrong" now is low (`research_refs`/`research_origin` are advisory today —
`work-view --research-refs` string queries, nothing hard-resolves them), but the
value compounds as that linkage becomes load-bearing.

## Phase 0 — prerequisite work (done)

Phase 0 makes the substrate *ready* for attestations without writing any yet.
Direct code reading shrank the scope from the draft's three code changes to **one**:

1. **`skills/knowledge-index/regen.py` — DONE.** `discover_docs()` rglobs
   `.research/**/*.md` and `lint_doc` requires `description`/`type`/`updated`, so an
   attestation (which lacks them) would raise lint errors. Added
   `.research/{reference,attestation,precis}/` to the discovery skip set (constant
   `ARD_SOURCE_TIERS`), alongside the existing `_archive` / `doc-review-report-` /
   `RESUME-STATE.md` skips — the **skip** route per D2 (citation-lint owns the source
   tiers). Covered by `tests/test_regen_exclusions.py`.
2. **`skills/knowledge-graph/render.py` — no change needed.** Verified: the graph is
   **index-driven** — `build_nodes` iterates `knowledge-index.yaml` (regen.py's
   output); it only touches `.research/` filesystem in `classify_target`, and only
   for `related[]` targets (which attestations never are). Excluding the tiers in
   `regen.py` keeps them out of the graph automatically. *(Draft over-scoped this.)*
3. **`hooks/scripts/post-tool-use-docs-bump.sh` — no change needed.** Verified: the
   hook already guards with `grep -q '^updated:' || return 0`, so it no-ops on
   attestations (which use `fetched`, not `updated:`). The existing guard is
   self-documenting; no source-tier carve-out required. *(Draft over-scoped this.)*
4. **Path map + slug docs — DONE.** The canonical two-tier `.research/` layout (D1),
   the source-tier exclusion (D2), and the `slug` convention (D3) are recorded in
   `research-skills-overview.md` § Output Structure so producers and consumers share
   one source of truth.

## Phases 1–3 (status)

- **Phase 1 — verification adapter, one vertical slice with teeth (DONE).** The
  vendored kernel (`scripts/lint-citations.py`, `catalogs.json`, `schema/`,
  `conformance/`, `templates/{attestation,INDEX,precis}.md`, `ard.json`) plus a
  Bash-capable `citation-lint` skill (the research skills' `allowed-tools` omit
  `Bash`, so they delegate to it). `/research` is wired end-to-end: attest →
  `[handle]{N}` → lint. The conformance suite (16/16) proves the vendored lint
  reproduces ARD's verdicts. Pre-existing briefs are `verification_status:
  legacy-unattested` (the lint checks zero citations on them, so they need the
  explicit marker).
- **Phase 2 — roll out with propagation (DONE).** The attestation + `[handle]{N}`
  chain runs across all producers: `/research`, `/brief`, `/scout` (single-agent;
  the parent authors, thin-attestation for scout's breadth-first nature), and
  `/deep-research` + `/research-program` (parallel specialists / single-agent
  campaign Leads). The `research-discipline` bundle is vendored as a skill (six
  sections byte-identical to ARD) and **inlined verbatim into every specialist /
  campaign-Lead / synthesis dispatch prompt** — an auto-loading skill does not
  propagate into spawned sub-agents. Handle-namespacing is ARD's: a flat shared
  `.research/attestation/` dir with source-named handles, and the lint's
  `colliding-handle` check as the post-merge backstop (the orchestrators run a
  campaign/program-wide lint in Phase 9). provenance convention: attestation files
  = `source-direct`; all synthesis briefs = `agent-synthesis`.
- **Phase 3 — gate + honesty + sync (in progress).** `rp:gate-citations` surfaces the
  lint as the research gate in the 8-gate `quality-checkpoint`, emitting broken-chain
  findings as `gate_origin: citations` substrate items (severity-staged). The
  three-check grounding model — lint (syntactic) + `adversarial-reader` (passage-level
  support) + isolated evaluator (fabrication-smell) — is documented in build-process.md
  § Quality Checkpoint. The ARD v0.4.1 pin lives in `ard.json`; the re-sync procedure
  is below.
- **Hardening (post-arc review).** A cross-model (Codex) adversarial review + a verbatim
  guard for the discipline (`adopts.discipline_sha256` + `test_discipline_verbatim.py`)
  + an e2e behavioral run. The review's findings (over-claimed `N` enforcement, the
  isolated evaluator can't verify passage support, a parallel-INDEX race) were fixed;
  the passage-support gap it surfaced is now closed by `skills/adversarial-reader/`
  (adapted from ARD CATALOGS §4), wired into all five producers.

## Re-sync procedure (on an ARD version bump)

ARD is pinned in `ard.json` (`adopts.version` / `release_tag` / `commit_sha`). To adopt
a newer ARD release:

1. **Extract the new release.** `git archive upstream/main plugins/agentic-research | tar -x -C /tmp/ar` (or the pinned tag/sha of the new version). Confirm the `<!-- ARD-Version: X.Y.Z -->` markers match the target.
2. **Re-copy each `vendored_paths` entry verbatim** from the new release into this plugin — the kernel artifacts (`lint-citations.py`, `catalogs.json`, `schema/`, `conformance/`, `templates/*`) are byte-for-byte; the `research-discipline` SKILL's **six numbered sections** are byte-for-byte (leave the deployment wrapper above them — it names our orchestrators and paths). "Pin, don't fork — never patch": fix bugs upstream, then re-sync.
3. **Update `ard.json`** `adopts.{version,release_tag,commit_sha,catalog_baseline}` to the new release.
4. **Run conformance:** `python3 plugins/research-pipeline/scripts/conformance/run.py` — must stay green (it asserts the vendored lint still reproduces ARD's canonical verdicts; a drift here means the re-sync changed lint behavior). If `catalogs.json` added pattern categories or chain statuses, update `conformance/expected.json` to match the new canonical verdicts and re-run.
5. **Bump the plugin** (`./scripts/bump-version.sh research-pipeline patch`) — the plugin's own semver is decoupled from `adopts.version`; bump it because the plugin changed.

## Deferred follow-ups

Small debts surfaced during the post-arc review are tracked as **substrate items**, not
here (build-process rule #6 — items in `.work/` track work, docs don't). skills-v2 now
runs its own `.work/` substrate; query the follow-ups with:

```
.work/bin/work-view --paths | grep -E 'version-number-warn-noise|cross-model-review-prompt-ware'
```

- **`version-number-warn-noise`** (low) — the vendored lint flags `X.Y` strings (e.g. "OAuth 2.0") as advisory `version-number` `[warn]`s; harmless (gate ignores pattern flags), fix upstream on re-sync, don't patch the vendored catalog.
- **`cross-model-review-prompt-ware`** (medium) — extend the cross-model review (already wired for substrate review + design-time) to cover edits to the skills/docs themselves.

## Risks

- **Attestation overhead** on every source would slow research → require
  attestations only for *load-bearing* claims, per ARD's thin-attestation (GR.5)
  rule, not every fetch.
- **Legacy corpora** predating attestations → explicit
  `verification_status: legacy-unattested`; do not rely on the lint to handle them
  silently.
- **Vendoring drift** from ARD → the conformance suite (`scripts/conformance/`) is the
  guard; the re-sync procedure (above) re-runs it on every ARD bump.
- **`allowed-tools` / Bash** → addressed by a dedicated `citation-lint` skill rather
  than widening every research skill's tool surface.

## Provenance

Decision set confirmed with the user 2026-06-08; plan peer-reviewed cross-model
via `peeragent` (Codex, xhigh). Companion session memory:
`agentic-research-vs-research-pipeline`, `careful-on-ard-adoption-work`.
