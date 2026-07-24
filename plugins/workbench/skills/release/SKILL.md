---
name: release
description: Prepare a Workbench release summary from completed outcome stubs. Use when the user asks to summarize completed work, prepare release notes, or bind outcomes to a version. Verify eligible outcomes, write one versioned summary under .work/releases, remove the selected completion stubs, and run repository-defined checks. This skill does not tag, publish, or deploy.
---

# Release Workbench Outcomes

Confirm Workbench ownership and `completed_items: summarize`. Read the selected
completion stubs in `.work/completed/`, existing release history, and project
delivery conventions.

Resolve the requested version and eligible outcome set. Do not include active,
blocked, unverified, or unrelated work. Verify that every selected stub reflects
an actual delivered outcome.

Write `.work/releases/<version>.md` with the date, concise outcome summary,
selected item ids, meaningful compatibility or operational notes, and
repository-defined verification. Prefer user-visible behavior over commit
chronology.

Remove the selected individual completion stubs after the release summary is
validated. Run the Workbench validator and project-defined release checks, then
report the release path, included outcomes, verification, and any excluded
items. Do not create a Git tag, publish an artifact, or deploy unless the user
separately requests that action.
