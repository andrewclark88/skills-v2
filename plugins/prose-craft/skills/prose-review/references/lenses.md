# Review Lenses

A lens is a reviewer persona holding one question and one checklist. Review
through one lens at a time. A reviewer holding several at once catches
fewer defects in each.

## Severities

- **material**: a reader would be misled, blocked, or lose trust. In
  `prose-refine`, material-class rewrites keep the loop going.
- **polish**: an improvement a reader wouldn't notice missing. Never blocks
  convergence.

Standard weight uses lenses 1–4 (audience, structure, clarity, accuracy).
Thorough weight uses all six.

## Contents

1. Audience: can the intended reader do the thing?
2. Structure: is this the right document, organized right?
3. Clarity: is every sentence doing its job?
4. Accuracy: is every claim true and current?
5. Voice: does it sound like the venue, and like a human?
6. Accessibility: could a tired non-native speaker follow it?

## 1. Audience

*Persona: the actual target reader, armed with only the knowledge the brief
grants them.*

- Does the draft assume knowledge the audience doesn't have (undisclosed
  prerequisites)?
- Is every piece of jargon defined on first use, or safe for this audience?
- Does each load-bearing data object, domain model, interface, or object group
  first say what it represents in the real world and why it matters?
- Where provider vocabulary appears, does the document map provider terms
  through project concepts to generic real-world terms before field details?
- When relationships remain abstract, does a short real-world scenario establish
  the mental model before diagrams or schemas?
- Can the reader find their next action within the first screen?
- Does the entry path work? Whatever leads a reader here, does the doc
  catch them?
- Are examples drawn from the reader's world, not the author's?

## 2. Structure

*Persona: a developmental editor.*

- Is the document one Diátaxis mode, or does it mix modes (a tutorial that
  drifts into reference)?
- Does the opening state purpose and reader payoff before details?
- Are sections ordered by reader need, not by the system's internals?
- Can readers follow the document collection in its intended order without
  waiting for a later page to define an earlier load-bearing concept?
- Do headings carry information (not "Overview", "Misc")?
- Is anything the brief promised missing? Anything present the brief
  excluded?
- Is it scannable? Lists where lists help, tables for parallel facts.

## 3. Clarity

*Persona: a line editor with the style contract in hand.*

- Active voice unless the actor is genuinely unknown or irrelevant.
- Sentences short on average; any sentence over ~30 words earns its length
  or splits.
- Concrete verbs over nominalizations ("decide", not "make a decision").
- One idea per paragraph; the paragraph's point is its first sentence.
- No hedging pile-ups, throat-clearing openings, or double negatives.
- Terms consistent. Same thing, same name, every time.

## 4. Accuracy

*Persona: a skeptic who checks. The only lens that may leave the document.*

- Verify commands, file paths, flags, and code samples against the actual
  project. Would they run as printed?
- Are version numbers, dates, and "currently" claims still true?
- Are capability claims checkable against the code, or aspirations stated as
  facts?
- Do links point where the text says they point?
- Are numbers (counts, limits, benchmarks) sourced or honestly hedged?

## 5. Voice

*Persona: a tone editor.*

- Register matches the venue. A README, a foundation doc, and a web article
  do not sound alike.
- No marketing-speak or hype adjectives: "seamless", "powerful", "blazing",
  "simply", "just".
- Confidence without arrogance; limitations stated plainly, not buried.
- Person and tense consistent (second person imperative for instructions).
- Humor, if any, never gates comprehension.

## 6. Accessibility

*Persona: a plain-language and inclusion reviewer.*

- Reading level appropriate; long words only where precision requires them.
- Idioms, culture-bound references, and wordplay don't carry load-bearing
  meaning. The text survives translation.
- Inclusive language: avoid ableist terms and gendered defaults.
- Formatting aids meaning but never substitutes for it (nothing conveyed by
  color or emphasis alone).

Related: `prose-refine`'s `references/llm-tells.md` catalogs machine-prose
patterns for the rewrite rounds. Tell-hunting complements the voice lens
but is not a lens itself.

## Findings format

One finding per line:

```
[material|polish] lens-name — §section or "quoted anchor": issue → suggested fix
```
