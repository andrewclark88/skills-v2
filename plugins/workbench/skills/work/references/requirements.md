# Requirements

Establish enough shared understanding to execute safely without turning every
request into a formal specification.

Determine:

- intended outcome and audience;
- observable behavior and acceptance evidence;
- constraints and explicit exclusions;
- consequential failure behavior;
- product choices only the user can settle.

Inspect code, tests, documentation, and current external facts before asking the
user. Ask one focused question when an answer materially changes the result,
then pause for the answer. Include a recommendation and evidence when useful.
Never treat the absence of a structured question tool as consent to guess.

Invoke `ideate` when the intended outcome or scope cannot yet support a coherent
work item, or when an apparently clear request depends on several coupled
product, domain, or business decisions whose answers materially reshape one
another or the scope. Do not accumulate a long requirements interview inside
`work`. Preserve ideate's no-write boundary and return only through a
user-selected handoff. Do not route
away merely because a small number of mostly local consequential choices remain,
and do not route large but already coherent work through ideation solely because
of its size.

Record settled requirements and exclusions in the relevant work item. Replace
superseded decisions instead of appending a conversation transcript. Preserve
implementation discoveries only when they change requirements, design,
integration, or future handoff.
