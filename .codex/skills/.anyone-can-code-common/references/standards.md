# Anyone Can Code Standards

These standards apply to the Codex-native lab skills in this repo. They intentionally preserve the course pedagogy while adapting the workflows to Codex.

## Audience

The audience is non-technical adults learning to code for the first time. Assume they know a small amount of programming syntax, but not the underlying systems ideas.

Write for clarity:
- first principles before jargon
- one concept per paragraph
- one claim per sentence when possible
- no repetition that does not advance a learning objective

## Codex Operating Rules

- Do not touch `.claude/`.
- Keep all Codex skill material under `.codex/skills/`.
- Use current browsing for research. Prefer primary sources.
- Do not use subagents unless the user explicitly asked for delegation.
- For `create-lab`, commit and push by default after review passes and registry files are updated.
- Validate the `origin` remote before pushing and never force-push.
- Never invent output. Run the commands and capture it.

## Scaffolding Test

Default to direct terminal typing.

A lab needs scaffolding only when at least one of these is true:
- the demo is a multi-step program with loops, functions, or state
- the demo needs multiple files
- a single logical unit is too long or error-prone to type live

Use this table:

| Signal | No scaffolding | Scaffolding |
| --- | --- | --- |
| Student interaction | 2 to 5 commands per Part | A program or file is the teaching unit |
| Files beyond markdown | None | One or more demo files |
| Complexity | Small commands or one-liners | Multi-line code with control flow or setup |
| Typing burden | Comfortable live typing | High typo risk or setup friction |

Consequences:
- No scaffolding: no demo files, no code walkthrough file, students type each command themselves.
- Scaffolding required: create only the necessary demo files, and add a code walkthrough file.

## Interactivity

Every Part of the lab must include:
- direct student action in the terminal or editor
- one conceptual question that tests why, not flag memorization

For direct-typing labs:
- each Part must have at least 2 distinct student-typed command blocks
- each command gets its own output block
- do not collapse a Part into one wrapper script

For scaffolded labs:
- each Part still needs at least 1 student-typed command in addition to running the demo

## Output Rules

- Every output block must come from a real run.
- If values vary per run, paste the actual output and add a short note that the learner's value will differ.
- If output is long, keep the most instructive portion and mark that it continues.

## Lab Deliverables

Always write:
- `<lab-id>-lab.md`
- `<lab-id>-script.md`
- `<lab-id>-report.md`

Write only when scaffolding is required:
- `<lab-id>-code-walkthrough.md`

After review passes, ensure `<lab-id>/README.md` exists as an instructor-only navigation file.

## Research Expectations

The research phase must:
- explain the problem before naming the concept
- cover internal mechanics, not just effects
- compare viable tooling options
- note macOS versus Linux differences when relevant
- provide at least 3 real sources per major concept

## Coverage Registry

Update `LAB_COVERAGE.md` for every new lab. Capture:
- concepts taught
- tools and commands demonstrated
- external services used, if any
- student exercises

If the matching row in `SYLLABUS.md` has no status, set it to `Draft`.

## README Rules

`README.md` is instructor-only and should not repeat student-facing setup content.

It contains exactly:
- a file-audience-purpose table
- a short recording order section
