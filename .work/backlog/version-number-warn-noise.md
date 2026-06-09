---
id: version-number-warn-noise
created: 2026-06-09
tags: [research-pipeline, citation-lint, vendored, low-priority]
---

The vendored ARD citation lint's pattern catalog flags any `X.Y`-shaped string as a
`version-number` advisory `[warn]` — including innocuous prose and titles like
"OAuth 2.0" (confirmed in the ARD-arc e2e run), not just numbered `## Sources` lists.

**Impact:** cosmetic only. It's an advisory `[warn]`, never a broken chain, and
`research-pipeline:gate-citations` ignores pattern flags (never emits items for them).
But it's noisier than the producer docs imply ("numbered Sources lists trip it"), which
can erode trust in an otherwise-clean lint ("my clean brief has 3 warnings").

**Constraint:** the pattern lives in the **vendored** `plugins/research-pipeline/scripts/catalogs.json`.
Pin-don't-fork — do NOT patch it locally (the verbatim guard + conformance assume the
vendored kernel is byte-identical to the pinned ARD release).

**Fix options:** (a) tighten the `version-number` pattern upstream in ARD, then pull it
on the next ARD re-sync (see `docs/ard-adoption-plan.md` § Re-sync procedure); or
(b) raise it to ARD as a false-positive report. Low priority.

Surfaced by the post-arc review; see `plugins/research-pipeline/docs/ard-adoption-plan.md`
§ Deferred follow-ups.
