---
name: research-handoff
description: Turn actionable findings from completed .research briefs into user-confirmed Workbench items. Use when research suggests implementation, remediation, follow-up investigation, or a project decision worth tracking. Preserve the research record, explain each proposed item's grounding, and create only the items the user confirms.
---

# Hand Research to Workbench

Read the relevant brief, cited attestations, `.work/CONVENTIONS.md`, and existing
active and backlog items. Require `owner: workbench` before emitting work.

Identify findings with concrete operational consequences. Do not rewrite
research to match project preferences, and do not treat every observation as
work.

For each proposed item, present in the current conversation:

- outcome and why it matters;
- supporting brief and source handles;
- whether it belongs in active work or backlog;
- relationships to existing items;
- unresolved decision or evidence risk.

Ask the user which proposals to emit. Create only confirmed items and include
the brief path in `research_refs`. Merge with equivalent existing work rather
than duplicating it.

Run `validate-workbench.py` from the installed Workbench plugin after emission,
resolving its package root by verified plugin identity. If Workbench is
unavailable, report that validation could not run rather than silently skipping
it. Identify created or updated items in the current conversation and leave the
research artifacts unchanged. Do not create a separate handoff report.
