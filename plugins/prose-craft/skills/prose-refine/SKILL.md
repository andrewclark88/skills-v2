---
name: prose-refine
description: >
  Drive a human-facing document such as a README, foundation doc, web article,
  or guide to publication quality through a multi-model rewrite-and-weave cycle.
  Use when a draft, or a topic that needs one, must be refined before publishing.
  In each round, fresh-context re-writer sub-agents from different model classes
  rewrite the draft in parallel. The orchestrator weaves the strongest sections
  into one voice. Scope narrows from a full rewrite to machine-prose tell hunting
  and then micro-edits, so the cycle converges within a 3-round cap.
---

# Prose Refine

Run the full cycle: establish the brief, draft, collect parallel rewrites from
different model classes, weave one voice, and repeat with narrower scope until
only micro-edits remain.

## Setup

1. If there is no draft, produce one with the `prose-draft` skill. Its brief is
   required for all later steps. If a draft exists, recover the brief from an
   HTML comment at the top or a companion note. If neither contains it, pin the
   brief with the user before refining.
2. Confirm the review weight. Use **standard** for 2 re-writers and the core
   lenses of audience, structure, clarity, and accuracy. Use **thorough** for 3
   re-writers and all six lenses. Default to standard when the user does not
   specify a weight.

## Re-writers, not just reviewers

Each round starts one fresh-context **re-writer** sub-agent per slot. Run them in
parallel where the harness supports it. Each re-writer returns a rewritten draft
and a per-section change log that states what changed and why. It does not
return a findings list. Use `prose-review` for review without rewriting.

**Diversify the model classes.** When the harness can access different model
classes, assign a different class to each re-writer. Different model families
expose different prose defaults and blind spots. When only one class is
available, assign distinct personas instead: a terse engineer, a longform
editor, and a domain skeptic. When the harness cannot spawn sub-agents, perform
sequential self-rewrites under those personas and report the fallback.

Every re-writer receives the current draft, the full brief, the style contract
(`prose-draft`'s `references/style-contract.md`), the venue obligations
(`prose-draft`'s `references/doc-types.md`), and the lens checklists for the
selected weight
(`prose-review`'s `references/lenses.md`).

## The round loop (cap: 3 rounds)

Scope narrows each round to ensure termination:

- **Round 1: full rewrite.** Re-writers may restructure and rewrite freely within
  the brief. Structural and sentence-level fixes are both in scope.
- **Round 2: targeted rewrite.** Do not restructure unless a material defect
  requires it. Focus on machine-prose tells and fit with the document's domain
  style. Give each re-writer `references/llm-tells.md`. Every change requires a
  justification in the change log.
- **Round 3: micro-pass.** Only tells, word choice, and surface errors are in scope.

Each round:

1. **Spawn.** Start the re-writers as described above.
2. **Weave.** Compare the rewrites section by section. Evaluate competing
   versions against the brief, the contract, and project facts. Merge the
   strongest versions. Must-keeps are invariant. Reject or repair in place any
   rewrite that changes one. Then normalize the voice of the woven draft so it
   reads as one author. Reject a rewrite that replaces the draft's tells with
   the re-writer's model-family tics.
3. **Measure the delta.** Classify the accepted changes. If all are micro-edits,
   consisting of tell fixes, word swaps, or punctuation changes, the document
   has converged. Exit the loop. Otherwise, continue to the next round at its
   tighter scope. At the cap, exit regardless and report what remains open.

## Final pass

After the loop, run one low-cost proofread for typos, punctuation, formatting,
and link targets. Use one agent without lenses or re-writers.

## Guardrails

- The brief's must-keeps are invariant. If a rewrite would change one, stop and
  surface the conflict to the user.
- The weave determines the final voice. Model diversity supplies alternative
  judgments, not multiple voices in the output. Reject changes that impose a
  re-writer's taste or model-family tics over the brief's intent. The result
  must sound like its author without retaining other authors' defaults.
- Do not force convergence by classifying a substantive rewrite as a micro-edit.
  If substantive changes continue to appear at the cap, report them accurately.
- The loop is bounded by design. Scope narrows each round so the loop
  terminates. Do not add rounds beyond the cap. Park remaining ideas as notes
  for the user.

## Report

Report the rounds run. For each round, identify the re-writers used by model
class or persona. List accepted and rejected changes with reasons, give the
delta classification, and state what the weave used from each re-writer. If the
process reached the cap, report all remaining known issues.
