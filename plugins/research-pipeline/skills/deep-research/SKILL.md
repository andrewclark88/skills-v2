---
name: deep-research
description: >
  Investigate a consequential multi-facet domain. Retains the familiar deep-research intent while
  delegating the campaign, ARD discipline, specialists, synthesis, and verification to
  agentic-research:research-orchestrator.
user-invocable: true
allowed-tools: Read, Glob, Grep, Skill, AskUserQuestion
model: opus
---

# Deep Research

Use this when a consequential decision needs multi-facet investigation. Read
`${CLAUDE_PLUGIN_ROOT}/docs/research-composition.md`, the project context, and
the knowledge index. Identify the decision the engagement can change and the
known constraints, but do not design a specialist tree yourself.

Invoke `agentic-research:research-orchestrator` with a proposed campaign output,
the decision-relevance hypothesis, relevant priors, and the requested scope.
Propose `standard` or `full` verification only when consequence warrants it;
the orchestrator confirms the dial and discovers fan-out during decomposition.

The orchestrator exclusively owns discipline propagation, specialist dispatch,
attestations, campaign paths, cross-synthesis, citation lint, adversarial read,
evaluation, acquisition offgas, and refresh semantics. Do not call the retired
pipeline validators or write legacy `.research/briefs/` campaign layouts.

On completion, update knowledge discovery and cite the resulting slug from the
commissioning work item when present. Actionable output crosses into `.work/`
only through the operator-confirmed research handoff.
