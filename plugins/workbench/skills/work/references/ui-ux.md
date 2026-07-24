# UI and Journey Requirements

Use interactive mockups when a nontrivial interface or user journey contains
product, state, sequencing, accessibility, or interaction uncertainty that
would be expensive to discover in production code.

Store the smallest useful walkthrough under `.mockups/<item-id>/index.html`
with local shared assets. Reference it from the work item through `mock_refs`.
Mockups are requirements evidence, not production components.

Cover the meaningful journey rather than one ideal screenshot: entry, primary
path, loading, empty, error, recovery, permission, and responsive behavior when
relevant. Use representative synthetic data only; never place PII or PHI in a
mockup.

Inspect the walkthrough in a browser, check keyboard and accessibility basics,
and refine it with the user before implementation. Do not require mockups for
small, already-settled UI changes.
