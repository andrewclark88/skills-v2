---
id: feature-upstream-baseline-2026-08
kind: feature
stage: done
tags: [upstream-sync, agile-workflow]
parent: epic-upstream-reconciliation-2026-08
depends_on: []
release_binding: null
gate_origin: null
created: 2026-08-01
updated: 2026-08-01
---

# Establish the current upstream baseline

Adopt current upstream content for upstream-owned plugins and shared tooling,
without replaying obsolete fork snapshot commits or dropping fork-owned plugins,
marketplace identity, substrate history, or local process artifacts.

## Acceptance

- Upstream-owned plugin content matches the selected upstream commit except for
  explicitly documented extensions.
- `research-pipeline` and its history remain present.
- Root marketplace metadata exposes the intended combined plugin catalog.
- The worktree contains no unresolved merge artifacts.

## Design

### Baseline

Merge `upstream/main` to preserve ancestry, pinned at
`43f7f4bf9d5d00acaa5692c3dc321583baae76a2` for this feature.

### Ownership resolution

- Take upstream wholesale for upstream-owned plugins: `agile-workflow`,
  `nates-toolkit`, `ux-ui-design`, and `workflow`.
- Accept new upstream plugins unchanged: `agent-coordination`,
  `agentic-research`, `code-audit`, `prose-craft`, and `workbench`.
- Preserve fork-owned `research-pipeline` unchanged during this feature except
  for merge mechanics. Its modernization belongs to the dependent research and
  hook features.
- Preserve the fork's `.work/` substrate and reconciliation items.
- Start the root marketplace from upstream, then add the fork-owned
  `research-pipeline` entry and retain the intended fork marketplace identity.
- Defer root README and process prose reconciliation to
  `feature-process-docs-2026-08`; resolve merge conflicts by preserving the fork
  versions temporarily.

### Verification

- No unmerged paths or conflict markers.
- Upstream-owned plugin trees are byte-identical to the pinned upstream tree.
- Fork-owned research-pipeline remains present.
- Marketplace JSON parses and registers research-pipeline plus upstream plugins.

## Implementation notes

- Nathan's repository-level Workbench `.work/`, `.research/`, `.knowledge/`, and
  `.mockups/` state was intentionally excluded. It is upstream project state,
  not distributable plugin content, and its `.work/` schema conflicts with this
  fork's retained agile-workflow substrate.
- Upstream's `agent-metadata.test.sh` still read the removed Pi `package.json`.
  The stale assertion was updated to verify that the retired package metadata
  remains absent, matching the upstream changelog and current distribution
  design.
- Upstream's content-integrity test used Bash 4's `mapfile`, which fails under
  the supported macOS system Bash 3.2. Its line collection now uses an
  equivalent portable read loop without changing the assertions.
- Upstream's prompt-context timeout test compared unresolved macOS temporary
  paths against the hook's canonical path. Its expectation now resolves the
  fixture root, preserving the behavior assertion across `/var` → `/private/var`.
- The repository's dogfood `.work/bin/work-view` was refreshed from 0.11.3 to
  the adopted 0.16.14 prebuilt and passed version and board-capability checks.

## Verification

- All nine `plugins/agile-workflow/scripts/tests/*.test.sh` scripts pass on
  macOS after the two upstream test-harness corrections and dogfood binary
  refresh.
- Both marketplace catalogs parse and expose the same ordered plugin identities.
- Claude/Codex manifest versions match for every locally owned plugin pair.
- Upstream-owned plugin trees match the pinned upstream baseline except for the
  three documented test portability/correctness fixes.

## Review outcome

Repository-wide validation passed against upstream commit `43f7f4bf`. The fork
is 57 commits ahead of that baseline and zero behind. The three deviations are
test-only, documented above, and pass on macOS.
