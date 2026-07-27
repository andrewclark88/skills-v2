---
name: research
description: Conduct and maintain source-grounded research for unstable, unfamiliar, contested, or decision-relevant questions. Use for prior-art analysis, technology or policy investigation, Workbench research commissions, reusable briefs, initializing .research, or rebuilding the unified knowledge index. Adapt depth internally, attest fetched sources before synthesis, seek disconfirming evidence, preserve contradictions, lint citations, and never place PII or PHI in research artifacts.
---

# Research

Produce reusable research whose claims can be traced to sources fetched during
the engagement.

Read [references/discipline.md](references/discipline.md) completely before
engaging sources. Its grounding floor is mandatory at every depth.
Read [references/promotion.md](references/promotion.md) before offering to turn
research method or domain guidance into a reusable project skill.

If `.research/CONVENTIONS.md` is absent, initialize
`.research/attestations/.gitkeep` and `.research/briefs/.gitkeep`, then write
concise conventions covering the grounding floor, citation syntax, authority
boundary, and the repository's confirmed privacy requirements. Keep both
`.gitkeep` files so empty tiers survive a fresh clone. When a Workbench
substrate exists, align these conventions with `.work/CONVENTIONS.md` and
`AGENTS.md`. Do not overwrite an existing research substrate.

## Set the decision boundary

Clarify the question, what downstream decision the answer may change, current
knowledge, exclusions, and stopping condition. Inspect `.knowledge/index.json`
and existing `.research/` artifacts before acquiring duplicate evidence.

Adapt depth from decision relevance, uncertainty, consequence, source
disagreement, and corpus size. Use specialist fan-out, adversarial reading, or
fresh-model review only when it improves evidence or judgment. Do not expose
separate quick, deep, or program workflows to the user.

Prefer current primary sources for load-bearing claims. When consequences or
uncertainty are high, corroborate those claims with an independent source or
state why corroboration was unavailable in the research brief.

## Acquire and attest

Fetch each grounding source during this engagement. Do not use model memory as
a citation or bibliographic source.

Before citing a detail, write
`.research/attestations/<source-handle>.md` with required frontmatter, a
source-faithful summary, and numbered anchored details under
`## Attested details`. An attestation is a local record of what this engagement
actually fetched and verified; it is not an endorsement of the source. Keep
project decisions and recommendations out of attestations.

When delegating source work, give every specialist the complete discipline.
Each specialist owns its source attestations and scoped findings and must lint
them before handoff. The lead owns cross-source synthesis, contradiction
classification, and final lint; never synthesize unlinted specialist output.

Stop and ask for redaction or an approved non-LLM path if material may contain
PII, PHI, credentials, or other prohibited sensitive data.

## Synthesize

Write `.research/briefs/<id>.md`. Cite attested details as `[handle]{N}`.
Distinguish source claims from inference. Search for disconfirming evidence
before each load-bearing conclusion.

When sources diverge, place their positions side by side. Do not average away
contradictions. Every brief must contain `## Disconfirming evidence`, even when
the result is that no material counterevidence was found. Add explicit
contradiction analysis when relevant.

Use frontmatter `relationships` with `supports`, `contradicts`, `informs`, or
`supersedes` when the relationship improves later discovery.

## Validate

Run:

```bash
python3 <workbench-plugin-root>/scripts/lint-research.py <project-root>
python3 <workbench-plugin-root>/scripts/build-knowledge-index.py <project-root>
python3 <workbench-plugin-root>/scripts/build-knowledge-index.py <project-root> --check
```

Resolve the script root from the loaded plugin package using the same
identity-verification rule as Workbench setup; stop rather than guessing among
ambiguous installations.

Fix source-chain errors before calling the brief complete. Reply in the current
conversation with the decision boundary, findings, contradictions, confidence
limits, sources, and any research-handoff opportunity. This reply summarizes
the durable brief; it is not a second research artifact.

After an interactive research engagement, ask whether the user wants genuinely
reusable method or domain guidance promoted into a project skill. Never promote
a skill during an autonomous run, and never create or update one without the
user's explicit answer.

For an index-only maintenance request, inspect source frontmatter, run the same
lint first when `.research/` exists, rebuild the index, and mention unresolved
metadata or relationships in the current conversation without starting a new
investigation or creating a report file.
