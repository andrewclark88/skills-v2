---
id: rust-binary-distribution-viable
kind: research-brief
summary: Rust prebuilt binaries are a viable distribution choice for a substrate query CLI, grounded in this repo's work-view precedent and Rust's documented size-tuning knobs.
updated: 2026-06-03
source_handles: [min-sized-rust, cargo-profiles]
---

# Rust prebuilt binaries are a viable distribution choice for research-view

*Settled stance (2026-06-03): if `research-view` ships as a prebuilt Rust binary committed to the
git tree (the `substrate-binary` pattern), binary size is repo size — and that remains viable.*

## What this brief is about

`research-view` will ship as a prebuilt Rust binary committed to the git tree (the
`substrate-binary` pattern), so binary size *is* repo size. This brief asks whether
that remains viable, grounded in the repo's existing precedent and Rust's documented
size behaviour — rather than recalling an estimate.

## The precedent already in this repo

`work-view` — a real substrate query binary of comparable scope — already ships four
cross-compiled targets, each well under 1 MB and all committed to git. Per direct repo
measurement (2026-06-03, branch `adopt-agentic-research`, `stat -c%s` on the committed
binaries under `plugins/agile-workflow/work-view/dist/`), the per-target sizes are:

- `aarch64-apple-darwin/work-view`: 636,880 bytes (~622 KiB)
- `x86_64-apple-darwin/work-view`: 664,144 bytes (~649 KiB)
- `aarch64-unknown-linux-musl/work-view`: 712,744 bytes (~696 KiB)
- `x86_64-unknown-linux-musl/work-view`: 760,656 bytes (~743 KiB)

All four combined total ~2.65 MiB, with musl static linking for the two Linux targets. A
single-purpose, read-only query CLI in Rust therefore lands in the low-MB range *in
practice* — at or below the ~2–5 MB-per-target figure the `substrate-binary` decision
assumed. (The original attestation that recorded these figures lived at
`.research/attestation/work-view-dist.md`; local-path attestations are not permitted in
the new layout, so the measurements are inlined here as direct repo observations.)

## Why the size stays small — and the headroom if needed

Rust's release profile is tunable for size without leaving the stable toolchain: the
`opt-level` `"z"` value means "optimize for binary size" [cargo-profiles]{2}, and
`strip` "direct[s] rustc to strip either symbols or debuginfo from a binary"
[cargo-profiles]{1} — symbol information that "is not needed to properly execute the
binary" [min-sized-rust]{2}. If a future tool ever pressed the per-plugin budget,
aggressive (nightly) techniques reach tens of KB — a stripped binary "reduced to 51KB"
with `build-std` [min-sized-rust]{3}, or "8KB" with careful `libstd` usage
[min-sized-rust]{4} — but work-view's ~700 KB shows the standard release + strip path is
already small enough that those extremes are unnecessary.

## Disconfirming evidence

The aggressive figures in [min-sized-rust]{3} are **not** a like-for-like comparison:
they require nightly `build-std` / `no_main` and measure a minimal program, not a full
CLI. The honest reference point for `research-view` is work-view's measured ~700 KB
(repo measurement, 2026-06-03, above), not 8 KB. This brief rests on the *work-view
precedent*, with the Rust-tunability sources as supporting mechanism only.

## Contradictions

None found among the three sources: the official `opt-level`/`strip` mechanics
[cargo-profiles]{1} are consistent with both the minimization catalogue
[min-sized-rust]{2} and the observed work-view sizes (repo measurement, 2026-06-03).

## Revisit if

`research-view` is actually built and its stripped per-target size measured — then
extend this brief with research-view's own numbers in place of the work-view analogue.
