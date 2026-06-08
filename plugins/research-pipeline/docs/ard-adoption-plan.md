---
description: "Plan for adopting ARD (Agentic Research Discipline) verification into research-pipeline — Option A: vendor ARD's liftable kernel (anti-fabrication floor + attestation/[handle]{N} citation chain + citation lint) as a verification adapter, keeping our orchestration/tiers/knowledge layer. Phase 0 decisions locked + code touchpoints; Phases 1-3 outlined. Peer-reviewed (Codex)."
type: architecture
updated: 2026-06-08
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
claim *N* is actually supported by the cited passage. Semantic support stays the
job of the LLM evaluator (the Phase 5 groundedness check added to `/research`, and
the isolated evaluators in the deeper tiers). The two are complementary:
**lint = mechanical chain integrity; evaluator = semantic support.**

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

## Phase 0 — verified code touchpoints (the prerequisite work)

All confirmed against the current code on `main`. None of this writes attestations
yet; it makes the substrate *ready* for them.

1. **`skills/knowledge-index/regen.py`** — `discover_docs()` (≈line 69) rglobs
   `.research/**/*.md`; `lint_doc` requires `description`/`type`/`updated`
   (≈line 144). Add `.research/{reference,attestation,precis}/` to the skip set
   (alongside the existing `_archive` / `doc-review-report-` / `RESUME-STATE.md`
   skips), **or** route them through a separate discovery like
   `discover_substrate()`. Decision per D2: **skip** (citation-lint owns them).
2. **`skills/knowledge-graph/render.py`** — `SCOPE = ("docs/", ".research/")`
   (line 32) with a generic `.research/` node fallback (≈line 62). Exclude the
   three source tiers from the scan so attestations don't appear as orphan nodes.
   (The evidence-node class is the separate fast-follow.)
3. **`hooks/scripts/post-tool-use-docs-bump.sh`** — activation gate matches
   `.research/**.md` (≈line 59) and bumps `updated:`. Attestations have no
   `updated:` field (they use `fetched`) and are immutable source records —
   exclude `.research/{reference,attestation,precis}/` from the bump.
   *(This touchpoint was found by direct code reading; it was not in the original
   plan.)*
4. **Path map + slug doc** — record the canonical `.research/` layout (D1) and the
   `slug:` convention (D3) in `research-skills-overview.md` so producers and
   consumers share one source of truth.

## Phases 1–3 (outline; designed after Phase 0 lands)

- **Phase 1 — verification adapter, one vertical slice with teeth.** Vendor
  `lint-citations.py` + schema + `catalogs.json` + `ard.json` + the templates; add
  a **Bash-capable `citation-lint` skill** (the five research skills' `allowed-tools`
  omit `Bash`, so they cannot run the lint directly — confirmed). Wire **one**
  `/research` slice end-to-end: write one attestation, cite `[handle]{1}`, run the
  lint, fail on broken chains. Add a conformance/fixture test proving the vendored
  lint reproduces ARD's verdicts. Mark pre-existing briefs
  `verification_status: legacy-unattested` (the lint's `reduced-substrate` status
  only applies when an attestation already exists, so legacy briefs need an
  explicit marker — they otherwise pass with zero citations checked).
- **Phase 2 — roll out with propagation.** Extend attestation-writing + `[handle]{N}`
  across `/research` → **`/brief` → `/scout`** (both emit sourced research that feeds
  design — omitting them leaves bypasses) → `/deep-research` → `/research-program`.
  **Inline the discipline body into dispatch prompts** (an auto-loading skill does
  not propagate into spawned specialists — ARD prepends the discipline into every
  authoring dispatch). Single-agent paths first; parallel specialists last, where
  shared-handle collisions/races appear.
- **Phase 3 — gate + honesty + sync.** Surface the lint as a release/quality gate;
  document plainly that lint = syntactic chain integrity and the LLM evaluator =
  semantic support; record the ARD v0.4.1 pin and the re-sync procedure (run
  conformance after any ARD bump).

## Risks

- **Attestation overhead** on every source would slow research → require
  attestations only for *load-bearing* claims, per ARD's thin-attestation (GR.5)
  rule, not every fetch.
- **Legacy corpora** predating attestations → explicit
  `verification_status: legacy-unattested`; do not rely on the lint to handle them
  silently.
- **Vendoring drift** from ARD → the conformance fixtures (Phase 3) are the guard;
  re-run on every ARD re-sync.
- **`allowed-tools` / Bash** → addressed by a dedicated `citation-lint` skill rather
  than widening every research skill's tool surface.

## Provenance

Decision set confirmed with the user 2026-06-08; plan peer-reviewed cross-model
via `peeragent` (Codex, xhigh). Companion session memory:
`agentic-research-vs-research-pipeline`, `careful-on-ard-adoption-work`.
