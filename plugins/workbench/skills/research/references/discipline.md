# Research Discipline

This grounding floor applies to every committed research brief. Keep
`.research/attestations/.gitkeep` and `.research/briefs/.gitkeep` so canonical
empty tiers survive a fresh clone.

## Source-bound claims

Fetch every grounding source during the current engagement. Model memory may
guide a search but may not become a citation, source URL, date, DOI, venue, or
other bibliographic fact.

If a fetched source attributes a claim to an unfetched source, state that
relationship explicitly and cite the fetched source. Do not present the
unfetched source as independently verified.

## Attest before synthesis

Before citing any detail, create
`.research/attestations/<source-handle>.md`:

```yaml
---
source_handle: <handle>
fetched: YYYY-MM-DD
source_title: <title>
source_url: <fetched-http-or-https-url>
---
```

Use a lowercase kebab-case handle matching the filename. Write a source-faithful
summary, then put all numbered, citable details under `## Attested details` with
source-internal anchors. Put the cited detail in the attestation before writing
`[handle]{N}` in a brief. Keep project framing, recommendations, and
cross-source synthesis out of attestations.

## Separate source and composition

An unmarked cited statement should be directly supported by its attestation.
Label cross-source or beyond-source composition as inference. Do not write
precise effort estimates, comparative superlatives, or named-feature claims
without fetched support.

## Seek disconfirming evidence

Before each load-bearing conclusion, search the attested corpus and available
sources for evidence that would weaken or reverse it. Every brief contains
`## Disconfirming evidence`; record meaningful results, or state the bounded
search that found none.

When sources differ, state their positions side by side and classify the
relationship as contradiction, tension, qualification, or incommensurability.
Do not smooth disagreement into a blended conclusion.

## Preserve authority boundaries

Research informs work. Work items, project plans, prior syntheses, and framework
rules are analytical lenses, not source attestations. Never rewrite an
attestation to support a downstream project decision.

## Protect sensitive data

Do not fetch, attest, synthesize, or index PII, PHI, credentials, session
material, or private patient/member data through an LLM-connected surface.
Request redaction, narrowing, or an approved non-LLM workflow.
