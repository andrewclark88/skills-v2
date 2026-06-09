---
name: citation-lint
description: >
  Run the ARD citation-chain lint over research artifacts — the mechanical anti-fabrication
  floor for the .research/ tier. Verifies every [handle]{N} citation in a brief/campaign resolves
  to a real attestation under .research/attestation/ with valid provenance, flags thin attestations
  (no quoted passages), and flags surface patterns that usually mark unsourced claims (bare decimals,
  version numbers, comparative superlatives, composed effort estimates). Syntactic chain integrity
  only — it does NOT judge whether a claim is semantically supported (that is the research evaluator's
  job). Use when the user asks to "lint citations", "check the citation chain", "verify attestations",
  "is this brief grounded", or after a research skill writes attestations + [handle]{N} citations.
  Invoked by /research (and later /brief, /deep-research, the docs gate). Vendored verbatim from ARD
  v0.4.1 (pin, don't fork — see ard.json); run it via flags, never edit the script.
user-invocable: true
allowed-tools: Bash, Read, Glob
model: haiku
---

# Citation Lint

A thin wrapper over the vendored ARD citation lint
(`${CLAUDE_PLUGIN_ROOT}/scripts/lint-citations.py`, zero-dependency Python). It is the
**mechanical** half of research-pipeline's grounding model. The semantic question (is the
claim actually supported by the cited passage?) is only partly covered — the research
evaluators catch fabrication-smell and uncited claims, but passage-level support is a known
gap (see build-process.md § Quality Checkpoint). The two are
complementary — run both.

## What it checks (ARD CATALOGS §3 + GR.5)

For every `[handle]{N}` citation in the target:
- **Citation chain** — the handle resolves to `.research/attestation/<handle>.md`; the
  attestation's `source_handle` matches; the handle is declared by exactly one attestation
  (no collisions); `source_url`/`source_path` + `provenance` are present.
- **Thin attestation (GR.5)** — a resolved attestation with no `##` section anchors and no
  `>` quoted passages can't support a per-claim citation.
- **Surface patterns** — bare decimals-with-attribution, version numbers, counts-without-units,
  comparative superlatives, named-feature claims, composed effort estimates (data-sourced from
  `scripts/catalogs.json`).

Statuses: `resolved`, `intra-program-resolved`, `reduced-substrate-attestation` (non-broken);
`unresolved-handle`, `mismatched-source-handle`, `colliding-handle`, `unreachable-source`,
`missing-provenance` (broken).

## Invocation

Resolve the bundled script (never assume it's on PATH) and run it against the analysis-tier
target. Default invocation for this plugin's compose-beneath layout:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/lint-citations.py" <target> \
  --attestation-dir .research/attestation \
  --no-url-check \
  --exit-code-on high
```

- **`<target>`** — a single brief (e.g. `.research/briefs/<slug>/parent.md`) or a directory
  (`.research/briefs`, `.research/programs`) to scan for `[handle]{N}` citations.
- **`--attestation-dir .research/attestation`** — our canonical source tier (matches the lint's
  default, but pass it explicitly so the command is self-documenting).
- **`--no-url-check`** — default OFF for the network HEAD liveness probe: keep research runs
  deterministic and network-free. Drop this flag (let the probe run) only when the user explicitly
  asks to verify source liveness.
- **`--exit-code-on high`** — non-zero exit when any broken (high-severity) chain is found, so a
  caller (a producer skill or the docs gate) can fail on broken citations. **But `rp:gate-citations`
  is stricter — it stages *medium* findings (e.g. `unreachable-source`: a `source_path` that
  doesn't exist) into `drafting`, which blocks a release.** So a brief that passes its own
  high-only inline check can still block at the gate. Producers should resolve medium findings
  too before finalizing (re-run with `--exit-code-on medium` to see them), not just high.
- Add `--format json` when a caller needs to parse findings.

`--analysis-dir` defaults to `.research/analysis` (ARD's layout) and only affects
`intra-program-resolved` fallback; our compose-beneath layout doesn't use it. Pass
`--analysis-dir .research/programs` only if a brief cites a sibling program artifact by handle.

## Reporting

Summarize: counts by status, each broken citation with its file + handle + why, thin-attestation
flags, and pattern flags (pattern flags are advisory — verify before acting; they catch *likely*
unsourced claims, not certain ones). State plainly that this is a syntactic pass and recommend the
research evaluator for the plausibility/fabrication-smell pass (noting passage-level support is a known gap).

## Provenance & maintenance

Vendored **verbatim** from ARD v0.4.1 per `ard.json` (pin, don't fork). Never edit
`scripts/lint-citations.py`, `scripts/catalogs.json`, or `scripts/schema/` — re-sync by
re-copying from the pinned ARD release, then run conformance:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conformance/run.py"   # 16/16 checks must pass
```
