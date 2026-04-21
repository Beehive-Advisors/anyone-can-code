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

## Pick your track

This is the **first section after the file header, and it contains the entire body of the lab**. The lab's content lives inside two `<details>` collapsibles; nothing but the header and this intro sits outside them.

```md
## Pick your track

This lab has two versions in one file. **Click the one matching your operating system** and follow it top to bottom. You never need to open the other.

<details>
<summary><b>🍎 Click here if you're on macOS</b></summary>

[FULL macOS lab — What You'll Build, Setup, Parts 1..N, Putting It Together, Checklist, Further Reading — macOS-native commands and outputs only]

</details>

<details>
<summary><b>🐧 Click here if you're on Linux or Windows/WSL</b></summary>

[FULL Linux/WSL lab — same sections as macOS, mirrored beat-for-beat, using Linux-native commands and outputs only]

</details>
```

**Key rules:**
- The student clicks one summary, then reads top to bottom inside that collapsible. No per-Part toggling.
- Shared conceptual content (What-you'll-build, WHY questions, Putting-it-together, Checklist) is duplicated inside each track — written twice. That's intentional: clicking once beats filtering throughout.
- Inside a single track, commands are platform-native — no `**🍎 macOS**` or `**🐧 Linux / WSL**` dual-labeled blocks. Those emojis appear only in the two `<summary>` lines.
- Keep the two tracks in lockstep: same Part count, same exercise count, same conceptual `### What is X?` intros and WHY questions, same number of Checklist items.

## What You'll Build

All sections below appear **inside each platform's `<details>` block**, once per track. The formatting rules apply identically to both copies.

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

Inside a track, commands are platform-native. Do NOT put dual 🍎 / 🐧 blocks inside a single track — the student already chose their platform via the top-level toggle.

If the lab is direct-typing:
- include 2 to 4 separate command blocks
- each command block has:
  - one framing sentence
  - a fenced code block with the exact command for this track's platform
  - an `**Output:**` heading with verbatim output from a tested run on that platform
  - 1 to 2 sentences connecting the result back to the concept

If the lab is scaffolded:
- show the run command for this track's platform with its `**Output (Section X):**` block
- explain the labeled output
- tell students to watch the walkthrough before continuing

### Conceptual question
- ask a why question
- the text can be identical across tracks (concepts are platform-neutral), but write it once into each track — no shared blocks
- use `<details><summary>Answer</summary>...</details>`

### Exercise
- one concrete task
- 5 to 15 minutes
- requires the learner to type code or commands
- commands use this track's platform-native syntax; no dual blocks
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
