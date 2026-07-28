# Style Contract

Rules for drafting human-facing documentation. This contract draws on
plain-language guidance and the Google and Microsoft developer documentation
style guides. It is a working contract rather than an exhaustive style manual.

## Purpose first

- Start with the reader's outcome. The first paragraph states what the doc does
  for them.
- Organize around the reader's task, not the system's internal structure.
- Explain within the first screen why the reader should continue.

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
