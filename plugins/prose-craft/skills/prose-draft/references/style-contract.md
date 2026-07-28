# Style Contract

Rules for drafting human-facing documentation. This contract draws on
plain-language guidance and the Google and Microsoft developer documentation
style guides. It is a working contract rather than an exhaustive style manual.

## Purpose first

- Start with the reader's outcome. The first paragraph states what the doc does
  for them.
- Organize around the reader's task, not the system's internal structure.
- Explain within the first screen why the reader should continue.

## Ground concepts before details

- Treat the document, and any ordered collection it belongs to, as the reader
  will encounter it. Do not rely on hidden project context or a later page to
  define a load-bearing term.
- Before technical detail, explain what each important data object, domain
  model, interface, or object group represents in the real world and why it
  matters to a user or the business. Work definitions into the prose when a
  glossary would feel forced.
- When a provider uses its own vocabulary, map the provider term to the
  project's concept and a generic real-world term. Explain major objects and
  systems before mapping individual fields.
- When provider models shape the document's concepts, compare representative
  providers or standards through current-source research. Do not let one
  provider's model silently become the project's model.
- When relationships remain abstract, use a short real-world scenario before
  diagrams, schemas, or field detail. Add only enough example to establish the
  mental model.
- Define terms that carry meaning or may be unfamiliar to the audience. Assume
  ordinary knowledge and do not explain every common term.

## Sentences

- Use active voice. Use second person ("you") for instructions.
- Keep sentences short by default. Aim for an average under 20 words. A sentence
  over ~30 words must justify its length or be split.
- Limit each sentence to one idea and each paragraph to one topic.
- Prefer concrete verbs to nominalizations. Write "configure" instead of
  "perform the configuration of".
- Put the main point first. Place conditions and caveats after the main clause
  when possible.

## Words

- Define jargon and abbreviations on first use, or link to a definition.
- Use one term for each concept and use it consistently.
- Prefer common words. Write "use" instead of "utilize" and "start" instead of
  "commence".
- Use contrastive correction only when the distinction prevents a real
  misunderstanding. If “X, not Y” or “X does A, not B” merely adds emphasis,
  state the positive claim and stop.
- Prefer literal domain language to stock metaphors such as “seam,” “spine,”
  “load-bearing,” “bridge,” or “north star.” Keep a metaphor when the user
  requests it, the domain already uses it, or it makes the concept clearer.
- Do not use hype or minimizers such as "simply", "just", "easy", "seamless",
  or "powerful". Delete them or replace them with the fact they obscure.
- Omit "please" from instructions and be direct.

## Structure

- Use informative headings. Write "Install on macOS" instead of "Installation".
- Use lists for enumerations, tables for parallel facts, and prose for argument.
- Commands and code blocks must be complete and work when copied as printed.
- Include only sections required by the doc brief.

## Honesty

- State limitations and gotchas where the reader encounters them, not in a
  footnote.
- Verify behavioral claims against the subject being documented.
- Give time-sensitive claims a specific basis. Write "as of v2.3" instead of
  "currently".
