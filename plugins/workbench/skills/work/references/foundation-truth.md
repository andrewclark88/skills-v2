# Foundation Truth

Foundation documents describe durable current behavior or an explicitly
intended project state. They are not progress logs, release notes, or a copy of
the work item.

## Find the affected foundations

Inspect the request, active item, design, final diff, and relevant entries in
`.knowledge/index.json`. Treat a foundation as affected when the work changes
or settles a durable:

- ownership boundary, architecture, contract, schema, protocol, or data flow;
- supported behavior, user journey, operating model, or compatibility promise;
- security, privacy, accessibility, reliability, or performance guarantee;
- repository-wide or sub-project principle.

Do not create or update foundations for local implementation details that do
not change durable project truth.

## Reconcile in place

For every affected assertion:

1. Compare the foundation, accepted requirements, design, and actual repository
   state.
2. Replace stale assertions, remove claims that are no longer true, and add only
   durable truth another contributor needs.
3. If implementation diverged from an intended design, update the intended
   assertion to the newly accepted state or leave the work open when the
   divergence is unresolved.
4. Keep repository-wide truth in root foundations and scope-owned truth in
   `<sub-project>/docs/` or `docs/<sub-project>/`, following repository
   convention. Link cross-scope contracts instead of duplicating assertions.
5. Preserve no historical narration merely to explain the change. Git carries
   history; release summaries carry delivered outcomes.

When no foundation changes are needed, state which durable surfaces were
considered and why existing assertions remain accurate. A silent no-op is not
reconciliation.

## Design, implementation, and review

During design, update foundations only after durable current or intended truth
is settled. A direct design request may roll intended truth forward before
implementation when the document clearly describes an intended state.

Before implementation closure, reconcile foundations against the integrated
result rather than the design alone. Do not close work while an affected
assertion is false, stale, contradictory, or ambiguously intended.

For independent design review, check that the proposed foundation changes match
requirements, ownership, boundaries, and meaningful alternatives. For
implementation review, check the final diff against affected foundations and
look for missing, stale, duplicated, or prematurely asserted truth.

## Keep discovery synchronized

If `.knowledge/index.json` exists and indexed documentation changes, rebuild it
with the Workbench `build-knowledge-index.py` script and run the same command
with `--check`. Resolve the script from the loaded plugin package using
Workbench's verified package-identity rule.

Report updated foundations and index validation with completion evidence.
Foundation reconciliation belongs inside design and delivery; do not invent a
separate documentation workflow, gate, or validation system unless the user
chooses one.
