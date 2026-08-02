---
name: gate-citations
description: >
  Run agentic-research's authoritative citation lint over a project's .research corpus and convert
  broken-chain findings into agile-workflow items. Use as the research integrity gate during a
  quality checkpoint or release; semantic support remains owned by the research engagement.
---

# Gate-Citations

You run a **citation-integrity gate** over the project's `.research/` corpus. Unlike the
other gates, the analysis is **not** a deep sub-agent — it is Agentic Research's authoritative
ARD citation lint, which mechanically resolves every
`[handle]{N}` citation against the attestation tier. Your job is to **run the lint, parse its
JSON, and convert broken-chain findings into items** that the release flow drains before
shipping.

**This gate is syntactic.** It proves the citation chain is intact — every `[handle]{N}`
resolves to a real attestation under `.research/attestation/` with valid provenance, no handle
collides, no source is unreachable. It does **not** judge whether a claim is actually supported
by its source. Agentic Research performs passage-level adversarial review and isolated evaluation
during the engagement. The checks compose; this gate is the release-time mechanical adapter.

## Trigger

- `/research-pipeline:quality-checkpoint` invokes this as the research gate (after the
  code/doc gates, before the consolidated summary).
- `/agile-workflow:release-deploy` may invoke during the `quality-gate` stage where a project
  configures it.
- User can invoke manually: `/research-pipeline:gate-citations <release-version>`.

## Model Assignment

- **Orchestrator (this skill's main loop)** — Opus, light. There is no analysis sub-agent;
  the lint script is the analytical authority. The orchestrator runs it, parses findings, and
  writes items. Keep it lightweight.

## Workflow

### Phase 1: Identify scope

The research corpus is **not** code bound to a release the way feature changes are — a broken
citation chain anywhere is a defect regardless of which release touched it. So this gate lints
the **whole research corpus**, then binds the resulting items to `<version>` so they drain with
the release.

```bash
# The brief-bearing + synthesis tiers carry [handle]{N} citations. The attestation/reference/
# precis tiers do not (attestations are source-direct descriptive files), so linting all of
# .research/ is safe — only [handle]{N} that fail to resolve produce broken-chain findings.
ls -d .research 2>/dev/null || { echo "No .research/ corpus — gate-citations is a no-op."; exit 0; }
```

If the project has no `.research/` directory, the gate is a clean no-op (report it and stop).

### Phase 2: Read existing gate items (idempotency prep)

```bash
.work/bin/work-view --release <version> --gate citations --paths 2>/dev/null
.work/bin/work-view --tag citations --paths 2>/dev/null   # includes any low/backlog items
```

Capture the set of already-tracked findings as `(file, handle, status)` tuples — you will skip
re-emitting these.

### Phase 3: Run the lint

Resolve the companion plugin, then run its citation lint over the corpus in JSON mode (no network
probe; surface everything, let severity drive staging):

```bash
AGENTIC_RESEARCH_ROOT="$(${CLAUDE_PLUGIN_ROOT}/scripts/resolve-agentic-research.sh)"
python3 "$AGENTIC_RESEARCH_ROOT/ard-core/kernel/lint-citations.py" .research/ \
  --no-url-check --format json > /tmp/citation-lint-<version>.json
```

The JSON shape is:

```json
{
  "results": [
    { "file": ".research/briefs/<slug>/parent.md",
      "citations": [ {"status": "unresolved-handle", "severity": "high",
                      "handle": "rfc6749", "n": 3, "line": 42}, ... ],
      "patterns": [...], "thin": [...] }
  ],
  "broken_chains": [...],
  "thin_attestations": [ [".research/briefs/<slug>/parent.md", {"handle": "...", "line": 9}] ]
}
```

A citation is **broken** when its `status` is not one of the non-broken statuses
(`resolved`, `reduced-substrate-attestation`, `intra-program-resolved`). Iterate
`results[]` (the `file` lives on the result, not on the citation) and collect, per file, every
citation whose `severity` is `high`/`medium`/`low`. Also collect `thin_attestations` (GR.5
thin-attestation flags) as low-severity findings.

**Note on advisory pattern flags.** The lint's `patterns[]` (e.g. the `version-number` flag a
numbered `## Sources` list trips) are `[warn]` advisories, **not** broken chains — do **not**
emit items for them. Only `citations[]` with a broken status and `thin_attestations[]` become
items.

### Phase 4: Convert findings to items

Map the lint's severity to stage exactly as the other gates do:

| Lint status | Severity | Stage | Location |
|---|---|---|---|
| `unresolved-handle`, `colliding-handle`, `mismatched-source-handle` | high | `implementing` | `.work/active/stories/` (blocks) |
| `unreachable-source` (source_path missing) | medium | `drafting` | `.work/active/stories/` (blocks) |
| `unreachable-source` (URL), `missing-provenance` | low | backlog | `.work/backlog/` (no binding; non-blocking) |
| thin-attestation (GR.5) | low | backlog | `.work/backlog/` (non-blocking) |

For each finding not already tracked, write an item:

```yaml
---
id: gate-citations-<short-slug>
kind: story
stage: implementing        # high  → implementing
                           # medium → drafting
                           # low    → backlog file (omit release_binding)
tags: [research, citations]
parent: null
depends_on: []
release_binding: <version>   # omit for low/backlog items
gate_origin: citations
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <one-line: which brief, which handle, what's broken>

## Finding
- **Status**: <unresolved-handle | colliding-handle | mismatched-source-handle | unreachable-source | missing-provenance | thin-attestation>
- **Severity**: <high | medium | low>
- **Citation**: `[<handle>]{<N>}`
- **Location**: `<file>:<line>`

## What's broken
<plain-language explanation. Examples:
- unresolved-handle: the brief cites [<handle>]{N} but no attestation exists at
  .research/attestation/<handle>.md — write the attestation, fix the handle, or drop the claim.
- colliding-handle: two attestation files declare source_handle: <handle> for different
  sources — rename one source's handle (and its citations) so each handle names one source.
- mismatched-source-handle: the attestation's source_handle field ≠ its filename/cited handle.
- unreachable-source: the attestation's source_path doesn't exist on disk.
- missing-provenance: the attestation or the calling brief lacks a provenance field.
- thin-attestation: the attestation has no verbatim key-passage anchors (GR.5).>

## Required fix
<the specific repair. The finding must clear at its severity before this item moves to done —
for a high finding the chain must lint clean at `--exit-code-on high`; for a medium
(unreachable-source) it must clear at `--exit-code-on medium`. Re-run the lint to confirm.>
```

Use a short, stable slug derived from `(handle, status)` so re-runs match (`gate-citations-rfc6749-unresolved`).

### Phase 5: Commit

```bash
git add .work/active/stories/ .work/backlog/
git commit -m "gate-citations: <N> citation-chain findings for <version>"
```

## Output

In conversation:
- **Corpus**: lint ran over `.research/` — `<N>` files, `<M>` citations resolved
- **Broken chains**: count by status (unresolved / colliding / mismatched / unreachable / missing-provenance)
- **Thin attestations**: count
- **Items created**: count by severity, with new ids
- **Goal reminder**: every `[handle]{N}` must resolve to a real attestation. high/medium items
  block release until they reach `stage: done`; low items live in the backlog. This gate is
  syntactic — pair it with Agentic Research's inline adversarial and evaluation stages.

## Guardrails

- **The analysis is the lint script, not your judgment.** Run it, parse the JSON, convert
  findings. Don't hand-adjudicate whether a chain is "really" broken — the lint's status is the
  authority within this lane.
- **One ARD implementation.** Resolve the validator from `agentic-research`; never fall back to a
  copied pipeline kernel. If resolution fails, report the missing companion as a blocking gate error.
- **Syntactic only.** Never claim this gate verifies a claim is supported by its source. Say so
  in the output; the semantic checks run inside Agentic Research engagements.
- **Don't fix the chains here — produce items only.** Repairs (writing the missing attestation,
  reconciling a colliding handle) happen via `/agile-workflow:implement` on each item, or via
  re-running the producing research skill.
- **Don't emit items for advisory pattern `[warn]`s** (e.g. `version-number` on numbered
  source lists). Only broken-status citations and thin attestations become items.
- **Idempotent.** Skip already-tracked `(file, handle, status)` findings on re-run, so a second
  `/quality-checkpoint` pass after a partial drain only emits net-new items.
- **No `.research/` corpus ⇒ clean no-op.** Report and exit; do not fabricate findings.
