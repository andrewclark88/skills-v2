---
id: semver-pre-1.0-stability
kind: research-brief
summary: Under SemVer 2.0.0 the major-version-zero (0.y.z) phase carries no stability promise; the public-API contract begins at 1.0.0.
updated: 2026-06-04
source_handles: [semver-spec]
---

# SemVer 2.0.0 — stability in the 0.y.z initial-development phase

*Seed question: Under SemVer 2.0.0, what stability is guaranteed during the pre-1.0
(`0.y.z`) phase? Single-source engagement at floor rigor (canonical spec text only).*

## Finding

The Semantic Versioning 2.0.0 specification makes **no stability promise** during the
major-version-zero phase: it designates `0.y.z` as "for initial development," states that
"Anything MAY change at any time," and that "The public API SHOULD NOT be considered
stable" [semver-spec]{1}. The stability commitment begins at the next milestone — the spec
defines `1.0.0` as the release that "defines the public API," after which increment rules
depend on how that public API changes [semver-spec]{2}.

Read together, the two clauses mark a boundary: before `1.0.0` the version carries no
backward-compatibility guarantee under the spec, and a consumer pinning a `0.y.z` release
takes on whatever change the next release brings; at `1.0.0` the public API becomes the
contract that governs subsequent increments [semver-spec]{1}.

## Disconfirming evidence

Searched the attested source for any carve-out that would grant stability *within* `0.y.z`
(e.g. a guarantee attached to MINOR or PATCH bumps before 1.0). The spec states the opposite
directly — "Anything MAY change at any time" [semver-spec]{1} — so no in-source
disconfirming evidence was found. Limitation: this is a single-source engagement at floor
rigor; the finding rests on the canonical specification text alone and was not
cross-checked against secondary interpretations.

## Revisit if

- A later SemVer revision changes the `0.y.z` language (this brief pins SemVer 2.0.0).
