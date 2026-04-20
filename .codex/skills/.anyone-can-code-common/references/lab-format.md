# Lab Format

Use this structure for every student lab file.

## File Header

```md
# Lab <id> - <title>

**Section:** <section name>
**Prerequisites:** <comma-separated list or None>
**Time:** ~<n> minutes
```

Add this line only when the lab is scaffolded:

```md
**Files:** `<lab-id>/`
```

## What You'll Build

Use 3 to 5 numbered outcomes.

Rules:
- each item is concrete and demonstrable
- prefer completed actions over vague learning claims

## Setup

Include:
- prerequisite checks
- install commands
- short plain-English package explanations
- platform split for CLI tools when install commands differ on macOS and Linux

Add terminal setup only when multiple terminals or processes are required.

## Part N - Concept Name

Each Part uses this order:

### What is <term>?
- 2 to 4 paragraphs
- explain the problem first
- define terms before using them casually

### Run the demo

If the lab is direct-typing:
- include 2 to 4 separate command blocks
- each command block has:
  - one framing sentence
  - the exact command
  - an `**Output:**` heading with verbatim output
  - 1 to 2 sentences connecting the result back to the concept

If the lab is scaffolded:
- include the exact command to run the demo file
- use `**Output (Section X):**` headings
- explain the labeled output
- tell students to watch the walkthrough before continuing

### Conceptual question
- ask a why question
- use `<details><summary>Answer</summary>...</details>`

### Exercise
- one concrete task
- 5 to 15 minutes
- requires the learner to type code or commands
- use `<details><summary>Solution</summary>...</details>`

## Putting It Together

Include:
- a comparison table with columns `Mechanism | What problem it solves | Key idea | Real systems`
- 1 to 3 sentences connecting the concepts

## Checklist

Use checkboxes for concrete skills.

## Further Reading

Use at least 3 real links from the research phase.

## Writing Rules

- one concept per paragraph
- no filler
- no repeated explanations across sections
- every paragraph must support a learning objective
