---
name: park
description: Capture useful context for later in a Workbench-owned project without expanding current scope. Use when the user says to park, defer, remember, backlog, or save an idea, bug, risk, or follow-up. Create the smallest useful .work/backlog item, preserving supplied context and evidence pointers without inventing requirements, priority, ownership, or design.
---

# Park Work

Confirm that `.work/CONVENTIONS.md` is owned by Workbench. If it is absent or
another system owns it, stop and offer `setup`; do not invoke destructive
conversion without the user's explicit choice.

Create `.work/backlog/<id>.md` with:

```yaml
---
id: <stable-kebab-id>
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Preserve the user's useful context, why it may matter, known evidence, and any
relationship to current work. Do not invent priority, acceptance criteria,
design, estimates, or assignment.

If equivalent backlog context already exists, update it instead of creating a
duplicate. Run the Workbench validator after writing the item. Report the
captured item and return to the prior scope.
