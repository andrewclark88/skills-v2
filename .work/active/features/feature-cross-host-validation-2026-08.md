---
id: feature-cross-host-validation-2026-08
kind: feature
stage: done
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

## Validation record

### Repository and upstream

- Upstream refreshed at `43f7f4bf9d5d00acaa5692c3dc321583baae76a2`;
  reconciliation branch is 57 commits ahead and zero behind.
- Both marketplace catalogs expose the same 12 ordered plugin identities.
- Every local plugin's Claude and Codex manifests match by name and version.

### Automated checks

- All Agile Workflow shell suites pass, including 66 versioning assertions,
  47 installer assertions, conversion integrity/routing/review-weight checks,
  board shim checks, distribution-version checks, and fallback readiness.
- Python suite: 97 passed across Agile Workflow hooks, Agentic Research refresh,
  Research Pipeline knowledge generation/graph, and Workbench validation.
- Agentic Research conformance: 57/57.
- Research Pipeline knowledge/graph suites: 19/19.
- Resolver, SessionStart/PostCompact, shell syntax, canonical links, portable
  frontmatter, stale-reference scans, and diff whitespace checks pass.
- Agentic Research's binary parity test skipped as designed because neither a
  local prebuilt target binary nor Cargo was available; installer coverage
  passed on the supported platform matrix stubs.

### Installed hosts

- Claude: Agile Workflow 0.16.14, Research Pipeline 0.2.0, and Agentic Research
  0.6.5 are installed at user scope. The installed Research Pipeline hook
  emitted the ds-engine navigator with `total_docs: 488`; its companion resolver
  found the installed Agentic Research cache.
- Codex: the same three versions are installed and enabled. A fresh normal
  `codex exec` session emitted `NAV_TOTAL=488` without reading project files or
  using a trust bypass.
- A live Claude model turn could not be run because the local Claude OAuth token
  is revoked (`401`). This does not affect plugin installation or hook execution;
  reauthentication is an environment follow-up, not a repository defect.

### Version and remote

- Research Pipeline bumped from 0.1.26 to 0.2.0 after validation.
- The reconciliation branch is pushed to `origin` and tracks its remote branch.
