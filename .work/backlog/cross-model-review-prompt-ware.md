---
id: cross-model-review-prompt-ware
created: 2026-06-09
tags: [agile-workflow, research-pipeline, review, workflow, medium-priority]
---

The peeragent cross-model (Codex) review loop earned its keep during the ARD arc — it
caught real false-assurance bugs in single-author **prompt-ware** that the test suite
structurally cannot (over-claimed `N` enforcement, the isolated-evaluator passage-support
gap, a parallel-INDEX write race). Those bugs lived in SKILL.md / docs prose, not code.

**Already wired (verified 2026-06):**
- `agile-workflow:review` runs a cross-model peer pass on its standard/deep lanes.
- `research-pipeline:feature-design` / `epic-design` run a cross-model advisory pass
  under autopilot for risky decisions.

**The gap:** changes to the **skills/docs themselves** (the prompt-ware that defines the
pipeline) get no automatic cross-model pass. The ARD arc's review was a manual
`/peer-review` invocation that only happened because the user asked. A future
high-blast-radius prompt/skill edit could ship without it.

**Possible fixes (decide when next touching the review/checkpoint skills):**
- A documented convention: "run `/peer-review` before merging foundational prompt/skill
  changes" (cheapest; relies on discipline).
- A checkpoint/gate option in `quality-checkpoint` that triggers a cross-model pass when
  the bundle touches `*/skills/*/SKILL.md` or plugin `docs/`.
- A PreToolUse/Stop hook nudge when SKILL.md edits are detected on a branch.

Tracks the `multi-model-review-setup` memory's deferred-wiring note. Medium priority.
