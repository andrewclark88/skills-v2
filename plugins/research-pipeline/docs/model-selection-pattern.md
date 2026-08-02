---
description: "Research Pipeline role vocabulary for host-aware model and effort selection."
type: pattern
updated: 2026-08-02
---

# Host-aware model selection

Research Pipeline declares the capability a workflow role needs. Agile
Workflow owns the mapping from those durable roles to concrete Claude, Codex,
Gemini, Z.AI, and Kimi models and effort flags:

- [Model Selection & Decision Matrix](../../agile-workflow/skills/principles/references/models.md)
- [Sub-agent dispatch contract](../../agile-workflow/skills/principles/references/subagents.md)

Do not copy concrete model tables into Research Pipeline skills. Model names,
aliases, and effort support change faster than workflow roles do.

## Role vocabulary

| Role | Required capability | Default posture |
|---|---|---|
| Orchestrator | decomposition, consequential judgment, integration | inherit the driver's quality-first session tier |
| Parallel worker | bounded inspection or editing with clear acceptance | balanced native worker at medium reasoning |
| Synthesizer | reconcile several artifacts into one coherent output | quality-first native model at high reasoning |
| Volume extractor | mechanical scaffolding or structured extraction | fastest adequate native model at low reasoning |
| Cross-model peer | independent blind spots | explicit different-lineage target from the shared host-to-peer matrix |

The interactive driver is a user/session choice. A portable skill must not
force a provider as its driver. Internal same-host sub-agents resolve from the
role table above. Cross-model work resolves an explicit opposite-lineage model
and effort from the shared matrix rather than inheriting the peer CLI's global
default.

## Effort guidance

- Use low reasoning for deterministic scaffolding and extraction.
- Use medium reasoning for bounded exploration and mechanical edits.
- Use high reasoning for orchestration, synthesis, design, and ordinary review.
- Use xhigh or the host's deepest stable tier for difficult cross-cutting work,
  adversarial review, or a task that already failed at high.

Effort names are provider-relative; equal labels do not imply equal compute or
capability. Preserve explicit caller and project overrides before applying these
defaults.

## Driver and peer separation

Claude Code, Codex, and Pi own their interactive driver defaults. Pi can drive
with GLM, Kimi, or another configured provider. Consuming these shared skills
additionally requires a working Pi plugin bridge; that bridge is currently
blocked on this project's macOS filesystem-lock capability probe, so Pi is not
yet a verified Research Pipeline workflow host here.

Cross-model review is lineage-relative, not harness-relative. Claude-driven
work normally chooses Codex; Codex-driven work normally chooses Claude. Once
the bridge path is operational, GLM- or Kimi-driven Pi work should normally
choose Claude or Codex. Gemini and Z.AI are valid fallback peer classes when
available. Kimi is a driver class in the current matrix but is not a peeragent
target until peeragent provides a Kimi adapter.

A same-lineage reviewer can still provide useful fresh context, but must not be
reported as cross-model evidence.
