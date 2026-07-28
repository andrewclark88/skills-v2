---
name: prose-draft
description: >
  Draft or rewrite human-facing documentation (READMEs, foundation docs, web
  articles, guides, reference pages) to a plain-language style contract. Use
  when starting a new doc from a topic or rewriting an existing draft for
  publication. Pins a five-field doc brief (audience, venue, purpose,
  must-keeps, scope) before writing, drafts to the contract, and hands off a
  brief that travels
  with the draft so later review can judge against intent.
---

# Prose Draft

Write documents for humans who chose to read. This skill is for published
artifacts: READMEs, `docs/` pages, web articles, and guides. It does not
cover code comments or commit messages.

## 1. Pin the brief

Before writing anything, pin and write down:

- **Audience**: who reads this, and what they already know.
- **Venue**: README, foundation doc, web article, guide, or reference page
  (see `references/doc-types.md`).
- **Purpose**: one sentence. After reading, the reader can ___.
- **Must-keeps**: facts, claims, commands, or phrasings that must survive
  every later edit. These are the source of truth against review drift.
- **Out of scope**: what this doc deliberately does not cover.

Gather the brief from the user's request and the repository. Ask at most one
round of questions, and only for load-bearing unknowns (usually audience
and venue). Use the harness's structured question tool when available.

For a rewrite, extract the brief from the existing document first; confirm
with the user only when the apparent audience or venue seems wrong.

## 2. Choose the type's obligations

Read `references/doc-types.md`. Name the single Diátaxis mode the draft is
in, then note the venue archetype's obligations. If the requested document
mixes modes, either split it or pick the dominant mode and cut the rest.
Say which you did. (README is the one sanctioned hybrid; see the reference.)

## 3. Draft to the contract

Read `references/style-contract.md` and write to it. The contract is the
default; a documented project style guide overrides it where the two
conflict.

## 4. Self-check, then hand off

Re-read the draft once as the audience would. Fix what fails the contract.
Then report: the file written, the brief in full, the chosen mode, and any
place you knowingly bent a contract rule and why.

Keep the brief with the draft so `prose-review` and `prose-refine` can
review against intent instead of guessing it. Carry it as an HTML comment
at the top of a markdown file (invisible when rendered), or inline in your
report when the venue cannot carry comments. Four fields are non-optional
in the carried brief: audience, venue, purpose, and must-keeps. Out-of-scope
travels whenever it was stated. That is the fifth field: required at pinning
time, optional only in transport when never stated. A reviewer receiving a
brief without these
fields should treat the brief as incomplete and pin them before judging.
