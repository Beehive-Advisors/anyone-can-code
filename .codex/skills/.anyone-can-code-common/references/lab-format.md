# Lab Format

Use this structure for every student lab file. Every lab ships with **two cross-platform tracks** (🍎 macOS and 🐧 Linux / WSL) that coexist in one markdown file — see `standards.md` Cross-platform Tracks section for the toggle and dual-block rules.

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

## Before you begin — pick your track

This is the **first section after the file header**, before What You'll Build. It is the student-facing toggle.

```md
## Before you begin — pick your track

This lab has two tracks in one file. Pick the one matching your operating system and follow the command blocks labeled for it throughout the lab.

<details>
<summary><b>🍎 I'm on macOS</b> — tap to see what this lab looks like for you</summary>

You'll use: `<tool 1>`, `<tool 2>`, `<tool 3>` — all installed by default on macOS (or via `brew install ...` if not).

Throughout the lab, every command block labeled **🍎 macOS** is yours. The **🐧 Linux / WSL** blocks do the same thing with different commands — skip them.

</details>

<details>
<summary><b>🐧 I'm on Linux or Windows/WSL</b> — tap to see what this lab looks like for you</summary>

You'll use: `<tool 1>`, `<tool 2>`, `<tool 3>` — installed by default on most distributions (or via `sudo apt install ...` if not). WSL students: always use WSL2, not WSL1.

Throughout the lab, every command block labeled **🐧 Linux / WSL** is yours. The **🍎 macOS** blocks do the same thing with different commands — skip them.

</details>
```

Keep each summary block tight — 2 to 4 lines. Name the specific tools the student will encounter in their track.

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

Every command is **dual-labeled by platform** — every step appears once for macOS and once for Linux / WSL.

If the lab is direct-typing:
- include 2 to 4 separate command blocks
- each command block has:
  - one framing sentence (shared — not per platform)
  - a `**🍎 macOS**` heading followed by the exact macOS command, then `**Output:**` with verbatim output from a macOS run
  - a `**🐧 Linux / WSL**` heading followed by the exact Linux command, then `**Output:**` with verbatim output from a tested Linux run (kubectl pod or Docker Ubuntu)
  - 1 to 2 sentences (shared) connecting the result back to the concept

If the lab is scaffolded:
- show the run command once per platform (🍎 macOS and 🐧 Linux / WSL) with their respective `**Output (Section X):**` blocks
- explain the labeled output (shared — the concept is platform-neutral)
- tell students to watch the walkthrough before continuing

### Conceptual question
- ask a why question
- shared across platforms (concepts are platform-neutral)
- use `<details><summary>Answer</summary>...</details>`

### Exercise
- one concrete task
- 5 to 15 minutes
- requires the learner to type code or commands
- if the exercise involves platform-specific commands: provide both 🍎 macOS and 🐧 Linux / WSL solution blocks inside the `<details><summary>Solution</summary>...</details>`
- if the exercise is platform-neutral: a single solution block, no platform split

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
