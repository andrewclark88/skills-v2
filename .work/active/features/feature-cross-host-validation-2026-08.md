---
id: feature-cross-host-validation-2026-08
kind: feature
stage: drafting
tags: [testing, claude, codex, release]
parent: epic-upstream-reconciliation-2026-08
depends_on: [feature-process-docs-2026-08]
release_binding: null
gate_origin: null
created: 2026-08-01
updated: 2026-08-01
---

# Validate the reconciled suite across hosts

Run the relevant plugin, substrate, research, knowledge, marketplace, and hook
checks before versioning or publication.

## Acceptance

- Plugin manifests and marketplace registrations validate.
- Agile-workflow and research tooling tests pass.
- A fresh Claude session receives expected project context.
- A fresh Codex session receives expected project context without trust bypass.
- Existing project substrates are not implicitly converted.
- Review findings are resolved or tracked before version bumps.
