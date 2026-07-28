---
source_handle: actions-stale-github
fetched: 2026-06-15
source_title: The official GitHub Actions `stale` action automates the management of inactive issues and pull requ…
source_url: https://github.com/actions/stale
provenance: source-direct
---
# Attestation: GitHub Actions — actions/stale

## Summary

The official GitHub Actions `stale` action automates the management of inactive issues and pull requests through a two-phase lifecycle: marking items stale after inactivity, then closing them if stale state persists. The action embodies a "nudge before removal" philosophy with extensive human-override mechanisms. It supersedes the now-archived probot/stale.

## Key passages

**Core lifecycle**:
- Phase 1: After `days-before-stale` (default: 60 days) of inactivity, adds a "Stale" label and optional comment
- Phase 2: After `days-before-close` (default: 7 days) additional inactivity, automatically closes the item
- Reactivation: Any update or comment removes the stale label and resets the timer (`remove-stale-when-updated: true` by default)

**Key configuration parameters**:
- `days-before-stale`: default 60 days
- `days-before-close`: default 7 days
- `operations-per-run`: default 30 (API rate limit guard)
- `debug-only`: false (dry-run mode for safe testing)
- `delete-branch`: false (opt-in branch deletion for PRs)

**Exemption mechanisms** (human override patterns):
- Label-based: `exempt-issue-labels`, `exempt-pr-labels` (e.g., "never-stale" label)
- Milestone-based: `exempt-all-issue-milestones`, `exempt-all-pr-milestones`
- Assignee-based: `exempt-all-issue-assignees`
- Draft protection: `exempt-draft-pr`
- Selective scope: `only-labels`, `any-of-labels`
- Set `days-before-close: -1` to mark without closing (requires explicit human action)

**Philosophy**: The automation embodies a "nudge before removal" philosophy: stakeholders receive warnings (via labels and comments) before closure, enabling manual intervention. The system respects active discussion—any engagement resets the timer—prioritizing human judgment over purely time-based rules.

**When NOT to use**:
- Repositories with sporadic contributors who may need extended response times
- Issues requiring domain expertise where automated closure risks losing valid but neglected problems
- Communities that value archival over deletion
- High-stakes items (security, compliance) demanding human review before closure

**Historical note**: The predecessor `probot/stale` was archived on May 20, 2023; `actions/stale` is the current supported implementation.

## Structural metadata

- Author: GitHub (official maintainer)
- Publication: github.com/actions/stale (README)
- Type: tool documentation / reference
- Primary concept: Time-based automated staleness detection with two-phase mark-then-close lifecycle
- Key defaults: 60 days to stale, 7 days stale-to-close
- Key design: Human override preferred; "nudge before removal" pattern; `debug-only` mode for safe validation

## Attested details

1. The official GitHub Actions `stale` action automates the management of inactive issues and pull requests through a two-phase lifecycle: marking items stale after inactivity, then closing them if stale state persists; any update or comment removes the stale label and resets the timer (`remove-stale-when-updated: true` by default).
2. The action embodies a "nudge before removal" philosophy with extensive human-override mechanisms (label-, milestone-, assignee-, and draft-based exemptions; `debug-only` dry-run mode).
3. It supersedes the now-archived probot/stale.
4. Setting `days-before-close: -1` enables a mark-without-close mode where items are marked stale but never auto-closed, leaving disposition to explicit human action.
5. Two-phase lifecycle parameters: `days-before-stale` (default 60 days) of inactivity triggers the Stale label; `days-before-close` (default 7 days) of additional inactivity triggers automatic closure (a 67-day total default mark→close cycle).
6. Mechanizable staleness signals (no NLP required): time since last update (60-day default), absence of assigned owner, absence of milestone, and absence of exemption labels.
7. "When NOT to use": "Issues requiring domain expertise where automated closure risks losing valid but neglected problems" — age alone is a weak signal for semantic staleness.
