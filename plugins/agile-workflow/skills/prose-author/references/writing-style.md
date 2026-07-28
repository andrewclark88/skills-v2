# Writing Style

Plain technical English for prose deliverables, adapted from ASD-STE100
Simplified Technical English. Applies to docs, READMEs, item bodies,
conventions, rules, changelogs, release summaries, error messages, and
comments. Does not apply to code, identifiers, command syntax, or quoted
output. Not for marketing copy or essays — the style strips voice on purpose.

## Modes

- **Flavored (default)** — general prose such as docs, READMEs, item bodies,
  and release notes. Apply the sentence, paragraph, and active-voice
  discipline. Relax the fixed dictionary so the text keeps enough range to
  read naturally.
- **Strict** — procedures, runbooks, safety text, and error messages. Apply
  every rule and both length caps.

## Rules

### Words

- Use one name for one thing. Do not call the same item by two names.
- Use the short common word: start (not begin, commence, or initiate), use
  (not utilize or leverage), help (not facilitate), make sure (not ensure),
  before (not prior to), after (not subsequent to), about (not regarding),
  get (not obtain or acquire), show (not demonstrate), also (not additionally,
  furthermore, or moreover).
- Give each word one meaning.
- No marketing adjectives: seamless, robust, powerful, cutting-edge,
  effortless, world-class, next-generation, revolutionary.
- American spelling.

### Verbs

- Active voice. Write "the parser reads the file", not "the file is read by
  the parser".
- Use a verb for an action. Write "analyze the log", not "perform an analysis
  of the log".
- No stacked auxiliaries. Not "it is important to note that this may help to
  improve". Write "this improves X".
- No "-ing" main verb where a simple tense works.

### Sentences

- One instruction per sentence. Max 20 words for an instruction, 25 for a
  descriptive sentence.
- No contractions. Use articles: a, an, the, this, these.

### Punctuation

- No semicolons. Write two sentences.

### Structure

- One topic per paragraph, max six sentences.
- For steps, use a numbered vertical list. One action per item, imperative
  form.
- Put a condition before its command.

## Self-lint

Run before finishing the text:

1. Any sentence over 20 words? Split it.
2. Any semicolon? Replace it with a period.
3. Any contraction? Expand it.
4. Any passive voice with a known actor? Make it active.
5. Any "-ing" main verb, nominalization ("perform an analysis"), or phrasal
   verb ("spin up")? Replace it with a plain verb.
6. Same thing named two ways? Pick one name.

## Limits

The mechanical rules fix the form of slop. They cannot make a hollow paragraph
true. Choosing the right technical noun, and judging whether a sentence makes
good sense, stays human work.
