---
name: release
description: >
  Prepare a Workbench release summary from completed outcome stubs. Use when the user asks to
  summarize completed work, prepare release notes, or bind outcomes to a version. Verifies eligible
  outcomes, writes one versioned summary under .work/releases, removes the selected completion
  stubs, and runs repository-defined checks. Does not tag, publish, or deploy.
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
reply in the current conversation with the release path, included outcomes,
verification, and any excluded items. This reply is separate from the durable
release summary and is not another repository artifact. Do not create a Git tag,
publish an artifact, or deploy unless the user separately requests that action.
