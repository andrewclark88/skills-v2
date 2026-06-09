---
name: research
description: >
  Research external systems, libraries, APIs, protocols, domain knowledge, and patterns.
  Investigates deeply, evaluates options, and produces a domain brief + auto-loading reference skill.
  Use before designing features that depend on unfamiliar technology, when domain knowledge is
  needed for architecture decisions, or when assumptions need verification.
  Extended for domain research and knowledge indexing.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, Agent, AskUserQuestion
model: opus
---

# Research

You research external systems deeply and produce two outputs: a domain brief with your
findings and an auto-loading reference skill. You also update the project's knowledge index.

**You follow the build process at `${CLAUDE_PLUGIN_ROOT}/docs/build-process.md`.** Read it before starting.

**Read `${CLAUDE_PLUGIN_ROOT}/docs/first-principles.md` for consideration.** Apply its thinking moves — especially Open and Challenge — to decompose domains deeply and stress-test assumptions during research.

**Extended for domain research (protocols, game rules, analytical methods) and knowledge index integration.**

## Model Assignment

Per [model-selection-pattern.md](../docs/model-selection-pattern.md):

- **Researcher (this skill's main loop)** — Orchestration. Opus high effort. Runs in parent context.
- **Investigation sub-agents (Phase 2)** — Parallel worker. Sonnet medium. Typically 3-5 parallel across sub-questions.
- **Synthesis (Phase 3)** — Synthesis. Opus high. Runs in parent context after sub-agents complete.

Scoping, synthesis, and recommendation are high-leverage — the orchestrator warrants Opus. Parallel investigation is scoped work where Sonnet is sufficient. For broader topics, escalate to `/deep-research`; for genuine megatopics spanning multiple domains, escalate further to `/research-program`. See [research-skills-overview.md](${CLAUDE_PLUGIN_ROOT}/docs/research-skills-overview.md) for the three-scale family.

## What This Covers

This skill handles two types of research:

**Technology research** — libraries, APIs, SDKs, frameworks:
- Evaluate options against project needs
- Verify API shapes from current docs (don't trust training data)
- Check health: recent commits, releases, community, license
- Produce code examples and integration patterns

**Domain research** — protocols, game rules, hardware, analytical methods, regulations:
- Investigate how external systems work
- Document rules, specifications, edge cases with source citations
- Produce implementation-relevant guidance (not textbook summaries)
- Ground findings in real data when available

## Phase 0: Knowledge Index Check (HARD PRECONDITION)

**Do not start research without this step.** Duplicated research is the #1 way knowledge layers rot.

1. Read `docs/knowledge-index.yaml` (or run `/knowledge-index` if no file exists)
2. Search the index for entries whose `description` or `title` overlaps with the research target
3. **If a relevant brief exists:**
   - Read it in full
   - Decide one of: (a) the existing brief is sufficient — STOP, present the existing brief to the user and confirm, (b) the existing brief is incomplete — note specifically what's missing and proceed with research scoped to the gap, (c) the existing brief is stale (outdated facts, superseded by changes) — proceed with research and explicitly mark this as a refresh of the existing brief
4. **If no relevant brief exists:** proceed to Phase 1
5. Communicate the outcome to the user before starting Phase 1: "Index check complete. Found existing brief X / Found no existing brief / Found related brief Y, scoping research to gap."

## Phase 1: Scope the Research

1. Read **CLAUDE.md** and project docs — understand the stack, constraints, what's known
2. Map how the project currently handles the area being researched with a **read-first triage**: dependency manifests, imports, config files, existing wrappers, and representative call sites via Read/Glob/Grep. Spawn an Explore sub-agent only when the integration surface is still broad or unclear after that probe (Sonnet minimum, Opus for large/complex codebases).
3. **Assess breadth.** Is this a focused single-domain topic, or does it span 5+ orthogonal aspects? If the topic is genuinely broad (multiple perspectives, requires decomposition, multi-angle synthesis matters), suggest `/deep-research` instead. If the topic spans multiple distinct domains each big enough to be its own campaign (3+), suggest `/research-program`. Let the user decide. See [build-process.md § When to Use /research vs /deep-research vs /research-program](${CLAUDE_PLUGIN_ROOT}/docs/build-process.md).
4. Define research questions:
   - What specific problem does this knowledge solve for the project?
   - What assumptions are we making that need verification?
   - What could we get wrong that would force a redesign?

**AskUserQuestion checkpoint:** Present:
- The research questions you'll investigate
- Options you plan to evaluate (if technology research)
- Domains you plan to investigate (if domain research)
- Any existing knowledge that's relevant (from the index)

Ask: "Are these the right questions? Anything to add or exclude?"

## Phase 2: Investigate

### For Technology Research

**2a. Official Sources**
- Read official documentation — focus on getting-started guides and API reference
- Check current version and recent changelog
- Read migration guides if upgrading

**2b. Health Check**
- Repository: recent commits, open issues, PR response time
- Releases: frequency, latest date, semver discipline
- Community: download trends, Stack Overflow activity
- License: compatible with project?

**2c. API Verification**
- Find the actual API surface — do NOT trust training data
- Verify function signatures, config options, return types from docs
- Find real-world usage examples (blog posts, open source projects)
- Note breaking changes between major versions

**2d. Integration Fit**
- Works with project's runtime/framework/build system?
- What does integration look like? (imports, config, initialization)
- Known conflicts with other dependencies?

### For Domain Research

**2a. Authoritative Sources**
- Official specifications, rule books, RFCs, API documentation
- Use WebSearch and WebFetch to find current sources
- Cite rule numbers, section references, version numbers

**2b. Real Data Grounding**
- If the project has data (card pools, tournament results, technique inventories), use it
- "The top 100 meta cards" is better than "common cards"
- "CR 603.3b" is better than "triggers go on the stack"

**2c. Edge Cases and Interactions**
- What are the complex interactions the system must handle?
- What do practitioners get wrong?
- What would break a naive implementation?

**2d. Implementation Relevance**
- What does this mean for the system we're building?
- What data structures does this imply?
- What decisions does this inform?

**Use Agent subagents (`model: "sonnet"`)** for parallel investigation when multiple areas need research. These subagents **gather** — have them return raw fetched material (URLs + verbatim excerpts), not just conclusions. **You (the parent) write the attestations from the actual sources** in Phase 2e; never attest from a subagent's paraphrase (that would launder an unverified summary into a source-direct attestation — the fabrication the chain exists to catch).

### 2e. Attest load-bearing sources (ARD citation chain)

As you consult sources, attest the ones that back a **load-bearing** claim — a number, an API shape, a specification rule, a comparative or composed-effort claim. Not every page you skim; only sources a reader would need to verify. (This is ARD's thin-attestation discipline: attest what the synthesis leans on.)

For each such source, write an attestation from the template at `${CLAUDE_PLUGIN_ROOT}/templates/attestation.md` to:

```
.research/attestation/<handle>.md
```

- **`<handle>`** — a stable kebab id for the source (`rfc6749`, `hono-v4-docs`, `postgres-mvcc`). It MUST equal the `[handle]` you cite with in the brief.
- Frontmatter (normative minimum): `source_handle` (== the handle), `fetched: <YYYY-MM-DD>`, one of `source_url` / `source_path`, `provenance: source-direct`.
- Body: a **Summary** (paraphrase, ~100-300 words — your words, no project framing) and **Key passages** (verbatim quotes for the load-bearing claims only, each with a source-internal anchor: §/p./¶/timecode).

Maintain a numbered bibliography per corpus at `.research/reference/<corpus>/INDEX.md` (template: `${CLAUDE_PLUGIN_ROOT}/templates/INDEX.md`). Pick a `<corpus>` slug grouping related sources (e.g. `oauth-standards`). **Append entries; never renumber.** `N` is the human-readable bibliography index — `/citation-lint` resolves the chain by **handle** (it does not read `INDEX.md` or check `N`), so append-only keeps the bibliography honest for readers, not because the lint depends on it. A new source gets the next free `N`.

If a topic is small enough that nothing is genuinely load-bearing (no numbers, no API shapes, no rules to verify), it's fine to produce no attestations — the brief is then `verification_status: legacy-unattested` (see Phase 4).

## Phase 3: Evaluate and Synthesize

**For technology:** Score each option against project-specific criteria. Present recommendation.

**For domain:** Synthesize findings into a coherent reference. Flag gaps where authoritative
sources disagree or are incomplete.

**AskUserQuestion checkpoint:** Present:
- Summary of findings (technology: comparison table; domain: key discoveries)
- Your recommendation or synthesis
- Any surprises or things that contradict assumptions
- Gaps: what couldn't you find authoritative sources for?

## Phase 4: Write Outputs

### 4a. Primer Document

Write to the canonical research tier: `.research/briefs/<topic-slug>/parent.md` (the same tree `/deep-research` and the design skills read; consumers and `/knowledge-index` resolve briefs from there). **Required: emit standard frontmatter at the top** so `/knowledge-index` regeneration picks it up.

**Cite load-bearing claims** with the `[handle]{N}` wire-form inline in the body — `handle` is the attestation handle from Phase 2e, `N` is its entry number in the corpus `INDEX.md`. Example: "OAuth refresh tokens SHOULD rotate on use `[rfc6749]{3}`." The `## Sources` section stays as the human-readable list; the `[handle]{N}` citations are the machine-checkable chain `/citation-lint` verifies. Cite the same claims you attested — don't cite a handle you didn't write an attestation for.

**For technology research:**
```markdown
---
description: {one-line "when do I read this?" hook — frame as the question this doc answers}
type: brief
slug: {topic-slug}
research_method: /research
verification_status: attested   # attested = went through the Phase 2e attestation + Phase 4d citation-lint chain
provenance: agent-synthesis   # the brief is a synthesis artifact (only the attestation files are source-direct); provenance must be PRESENT for [handle]{N} citations to resolve (the lint checks the calling brief, not just the attestation)
updated: {today's date, YYYY-MM-DD}
summary: |
  {2-4 sentences — what was researched and the key recommendation}
key_findings:
  - {finding or recommendation}
  - {finding or recommendation}
---

# Research: {Topic}

## Context
{Why this research was needed}

## Options Evaluated
### {Name} (v{version})
- **Maturity**: {Active/Stable/Deprecated}
- **License**: {license}
- **Pros/Cons**: {list}
- **Fit**: {project-specific}

## Recommendation
{Clear choice with rationale}

## Implementation Notes
{Key API patterns, pitfalls, configuration}

## Code Examples
{Concrete usage patterns}

## Sources
{URLs, doc references}
```

**For domain research:**
```markdown
---
description: {one-line "when do I read this?" hook — frame as the question this doc answers}
type: brief
slug: {topic-slug}
research_method: /research
verification_status: attested   # attested = went through the Phase 2e attestation + Phase 4d citation-lint chain
provenance: agent-synthesis   # the brief is a synthesis artifact (only the attestation files are source-direct); provenance must be PRESENT for [handle]{N} citations to resolve (the lint checks the calling brief, not just the attestation)
updated: {today's date, YYYY-MM-DD}
blocks_phase: {phase number, if this brief gates a specific phase — optional}
summary: |
  {2-4 sentences — what this brief covers and why it matters}
key_findings:
  - {key finding}
  - {key finding}
---

# Brief: {Topic}

## Purpose
{What this covers and why it matters for the project}

## {Core Sections}
{Rules, specifications, interactions — with citations}

## Implementation Notes
{What this means for the system being built}

## Sources
{Every source consulted — URLs, rule numbers, doc names}
```

### 4b. Reference Skill (for technology research)

Write an auto-loading reference skill at `.claude/skills/{topic-slug}/SKILL.md`:
- Named after the technology (e.g., `hono-v4`, not `research-hono`)
- `user-invocable: false` — auto-loads by keyword match
- Key API patterns, code examples, pitfalls
- Under 200 lines

### 4c. Regenerate Knowledge Index

After writing the brief, **run `/knowledge-index`** to regenerate the index from frontmatter.

Do NOT hand-edit `docs/knowledge-index.yaml` — it's a derived artifact. Frontmatter is the
only source of truth. See `${CLAUDE_PLUGIN_ROOT}/skills/knowledge-index/SKILL.md` for the full schema and
field semantics.

Required frontmatter on the brief:

```yaml
---
description: <one-line "when do I read this?" hook — frame as the question this doc answers>
type: brief
kind: research
slug: <topic-slug>
research_method: /research
verification_status: attested   # attested | legacy-unattested (absent ⇒ legacy-unattested)
provenance: agent-synthesis   # the brief is a synthesis artifact (attestation files are source-direct); must be present for [handle]{N} citations to resolve (lint checks the calling brief too)
updated: <YYYY-MM-DD>
summary: |
  <1-2 sentences on what's in the brief>
key_findings:
  - <3-7 bullets on what the research showed>
status: draft
---
```

### 4d. Lint the citation chain

Before finalizing, run the **mechanical** citation check via the `citation-lint` skill on the brief you just wrote:

```
/citation-lint .research/briefs/<topic-slug>/parent.md
```

It verifies every `[handle]{N}` resolves to a real attestation under `.research/attestation/` with valid provenance, and flags thin attestations + suspicious unsourced-claim patterns. On a **broken chain** (high severity — e.g. a `[handle]` with no attestation), fix it before finalizing: write the missing attestation, correct the handle, or remove the claim. Re-run until clean.

Note: the lint checks that `provenance` is **present** on the **calling brief** too, not just the attestation — that's why the brief frontmatter carries `provenance: agent-synthesis` (the brief is a synthesis artifact; only the attestation files are `source-direct`). A brief that cites `[handle]{N}` without its own `provenance` field gets a (low-severity) `missing-provenance` finding. Numbered `## Sources` lists can trip the advisory `version-number` pattern flag — that's a `[warn]`, not a broken chain; ignore it or move the source list below the citations.

This is the syntactic half. It pairs with Phase 5 (the independent evaluation): **4d proves the citations resolve to real, attested sources; Phase 5 — isolated to the brief + questions — catches fabrication-smell, uncited or internally-unsupported claims, and gaps.** Note the boundary: Phase 5 does NOT see the attestation passages, so it does not verify a cited passage actually *supports* its claim (passage-level support is a known pipeline gap — see build-process.md § Quality Checkpoint). Run both; treat clean lint + clean Phase 5 as "the chain resolves and nothing looks fabricated," not "every claim is source-verified."

If the brief is genuinely `verification_status: legacy-unattested` (nothing load-bearing to attest), there are no `[handle]{N}` citations and the lint is a no-op — that's fine; record the status honestly rather than manufacturing citations.

## Phase 5: Independent groundedness check

Single-tier `/research` has no parallel specialists, so the brief carries more unverified author judgment than a `/deep-research` campaign — and unlike the deeper tiers, nothing has independently checked it. Before finalizing, run one **fresh-context evaluation** to catch fabrication and ungrounded claims — the same isolation principle `/deep-research`'s Evaluator uses, scaled to one brief.

Spawn an evaluator with **only the written brief + the Phase 1 research questions** — NOT your investigation notes, sources list reasoning, or orchestration context. The isolation is the point: it prevents the evaluator inheriting your framing and rubber-stamping it.

```
Agent({
  description: "Evaluate research brief: {topic}",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: <the brief's full text + the Phase 1 research questions; ask for the assessment below>
})
```

Ask the evaluator for:
- **Groundedness** — does every load-bearing claim trace to a source in `## Sources`? Flag anything that reads like training-recall (especially API shapes, version numbers, benchmark/figures) with no citation.
- **Coverage** — are the Phase 1 research questions actually answered, or are gaps papered over?
- **Contradictions** — internal inconsistencies, or sources that disagree without being flagged?
- **Verdict** — `APPROVED` or `NEEDS-REVISION` with specific, locatable findings.

On `NEEDS-REVISION`, fix the flagged claims (re-fetch sources, add citations, or mark gaps honestly as limitations) and re-run until `APPROVED` or the remaining items are acknowledged limitations recorded in the brief. Under an active autopilot run this check is advisory and non-blocking — record the verdict and proceed if the evaluator can't be spawned — but a fabrication-grounds `NEEDS-REVISION` should always be addressed.

## Anti-Patterns

- **NEVER skip the knowledge index check.** If a brief exists, read it first. Don't duplicate.
- **NEVER trust training data for API shapes.** Verify from current documentation.
- **NEVER recommend without evaluating alternatives** (technology research).
- **NEVER skip the health check** — a superior but abandoned library is a liability.
- **NEVER produce a brief without source citations.** Every claim must be verifiable.
- **NEVER cite a `[handle]{N}` you didn't attest.** The handle must resolve to a real attestation under `.research/attestation/` — a citation with no attestation is exactly the fabrication the chain exists to catch.
- **Keep the corpus `INDEX.md` append-only.** `N` is a human bibliography index; the lint resolves by handle, not `N`, so renumbering won't break the chain mechanically but will misnumber the reader-facing list.
- **NEVER mark a brief `verification_status: attested` if `/citation-lint` reports broken chains.** Fix them, or record `legacy-unattested` honestly.
- **NEVER produce generic findings.** Ground everything in this project's specific needs.
- **NEVER skip AskUserQuestion checkpoints.** Wrong research direction wastes effort.
- **NEVER forget to run `/knowledge-index`** after writing the brief. Future sessions depend on the regenerated index.
- **NEVER hand-edit `docs/knowledge-index.yaml`.** It's derived from frontmatter; edits will be overwritten on the next regenerate.

## Completion Criteria

- All research questions answered with evidence
- Domain brief written with source citations
- Load-bearing claims attested (Phase 2e) and cited `[handle]{N}`; corpus `INDEX.md` updated
- Reference skill written (technology research only)
- Citation chain clean — `/citation-lint` reports no broken chains (Phase 4d); `verification_status` set accordingly
- Knowledge index updated
- User confirmed findings at Phase 3 checkpoint
- Independent groundedness check passed (Phase 5) — or its findings acknowledged as recorded limitations
