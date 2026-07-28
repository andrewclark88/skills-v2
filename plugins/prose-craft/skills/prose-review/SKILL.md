---
name: prose-review
description: >
  Review a human-facing document (README, foundation doc, web article,
  guide, or reference page) through editorial lenses and report
  severity-tagged findings with concrete fixes. Lenses: audience, structure,
  clarity, accuracy, voice, accessibility. Use for a single-pass review of
  an existing draft. Findings are proposals for the author to adjudicate,
  not verdicts. For a full draft-review-revise cycle with sub-agent
  reviewers, use prose-refine.
---

# Prose Review

Conduct one pass with the selected lenses and return actionable findings. Do
not edit the document.

## Inputs

- **The draft** (a path). Read the whole thing once for context before
  judging any part.
- **The brief**: audience, venue, purpose, must-keeps. Look for a brief
  carried with the draft (an HTML comment at the top, or a companion note).
  Published documents normally carry no brief — `prose-draft` strips the
  working comment at publication — so a missing brief is expected, not a
  defect. If none exists, ask the user for audience and venue, or infer them
  and say you did. If a brief exists but lacks audience, venue, purpose, or
  must-keeps, treat it as incomplete: pin the missing fields (ask, or infer
  and say so) before judging.
- **Lens selection.** Default (standard): audience, structure, clarity,
  accuracy. The user may name lenses or ask for all six.

## Review

Read `references/lenses.md` for the checklists. Review one lens at a time,
in the order listed there. The accuracy lens may and should leave the
document to check commands, paths, and claims against the actual project.

Rules:

- Judge against the brief, not your taste. A deliberate, documented style
  choice by the author is not a finding.
- Every finding names a location (section heading or quoted anchor) and a
  concrete fix. "Consider improving the flow" is not a finding.
- Severity must be honest. **material** means a reader would be misled,
  blocked, or lose trust. Do not inflate polish into material to look thorough. Do
  not soften material into polish to be kind.

## Report

1. Findings grouped by lens, in the format from `references/lenses.md`.
2. A verdict line: N material, M polish.
3. One short paragraph on the draft as a whole: what already works, so the
   author protects it during revision.

Do not edit the draft. Findings are proposals; the author or the
`prose-refine` loop adjudicates and revises.
