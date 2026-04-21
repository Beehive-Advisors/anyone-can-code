# Course Lab Standards

These standards are the **canonical, agent-agnostic** course pedagogy. Both the Claude-native skills (under `.claude/skills/`) and the Codex-native skills (under `.codex/skills/`) apply the same semantic rules — audience, scaffolding test, dual-track layout, output discipline, interactivity. Agent-specific trees keep their own SKILL.md frontmatter and path conventions; the pedagogy does not diverge between them.

All three lab skills — `create-lab`, `research-lab`, and `review-lab` — read and apply these standards.

For language-specific rules (Python, shell, TypeScript, Docker), read the relevant file in `tech-standards/` based on the file extensions present in the lab.

See also:
- `lab-template.md` — exact formatting rules for student lab files
- `script-template.md` — exact formatting rules for instructor script files

---

## Audience

Students are beginner programmers — non-technical adults learning to code for the first time. They know basic programming syntax but nothing about the specific topic being taught. Every explanation must be accessible without being condescending.

---

## Pedagogical Principles

**First principles before jargon.**
Every technical term is explained from scratch the first time it appears. Start with the problem being solved, then the concept, then the name. Never use a term as if it's already understood.

**Ruthless simplicity.**
One thing per sentence. One concept per paragraph. If a sentence can be cut without losing meaning, cut it. Never repeat a concept already explained in a prior section. Minimum content for maximum clarity.

**Students build, not watch.**
Every lab produces something concrete. Outcomes are stated as actions: "I hashed a password with bcrypt", not "I learned about hashing."

---

## Cross-platform tracks — First-Class Requirement

Every lab has **two parallel tracks** that coexist in the same `[ID]-lab.md` file:

- 🍎 **macOS track** — the instructor's primary platform. Every command and captured output in this track comes from a tested macOS run.
- 🐧 **Linux / WSL track** — for students on Ubuntu / WSL2. Commands are parallel translations of the macOS track; outputs follow the same structure but line counts, labels, and specific values differ. Linux output is captured from a real Linux environment (kubectl pod on the bare-metal k0s cluster is preferred; Docker Ubuntu is fallback — see `create-lab/SKILL.md` Phase 3).

**How the two tracks lay out in the lab file:**

The lab's body is split into **two full-track collapsibles** at the top of the file. The student clicks one toggle and reads from there to the bottom of that track. Nothing but the file header sits outside the two collapsibles.

1. **One single toggle at the top.** The first section after the file header is `## Pick your track`. It contains exactly two `<details>` blocks — one for macOS, one for Linux / WSL. Each block holds the complete standalone lab for that platform (What-you'll-build, Setup, all Parts, Putting-it-together, Checklist, Further Reading). See `lab-template.md` for the exact scaffolding.

2. **Each track is self-contained.** A student on macOS expands the macOS toggle and reads from top to bottom without ever seeing Linux content. The two tracks mirror each other beat-for-beat — same Part count, same exercise count, same conceptual intros, same WHY questions — but every command, every OUTPUT block, every tool reference is platform-native inside each track.

3. **Shared conceptual content is duplicated, not shared.** Because the entire lab body lives inside the two collapsibles, platform-neutral content like the `### What is X?` intros, WHY questions, Putting-it-together text, and Checklist items appear once in the macOS track and once in the Linux track. This duplication is intentional: the gain in reading flow (click once, never filter again) outweighs the cost of writing it twice.

4. **Never put dual 🍎 / 🐧 blocks inside a single track.** That was an earlier format. Inside the macOS `<details>`, every command is macOS-native without any 🍎 label. Inside the Linux `<details>`, every command is Linux-native without any 🐧 label. The 🍎 / 🐧 emojis appear only in the two `<summary>` labels at the very top.

**Never collapse the dual-track down to a single platform.** A lab that only works on macOS or only works on Linux is a FAIL.

**Instructor scripts follow the same dual-track rule.** Every lab produces TWO terminal screencast scripts:
- `[ID]-script-macos.md` — macOS shooting script (OUTPUT blocks from tested macOS run)
- `[ID]-script-linux.md` — Linux shooting script (OUTPUT blocks from tested Linux run; kubectl pod or Docker)

The optional `[ID]-code-walkthrough.md` (only when scaffolded) is **shared** — not duplicated per platform, because demo code is cross-platform.

---

## The scaffolding test

Default to direct-terminal typing. A lab should ship demo files (`.sh` / `.py` / `.ts` / `Dockerfile` / etc.) **only** when the demo cannot reasonably be typed command-by-command into the terminal.

A lab needs **scaffolding** when at least one of these is true:
- The demo is a multi-step program with loops, functions, or state
- The demo requires multi-file setup (Dockerfile, class hierarchy, config files, compose file)
- Any single logical unit exceeds ~5 lines of code and would be tedious or error-prone to type live

| Signal | No scaffolding needed | Scaffolding required |
|--------|-----------------------|----------------------|
| Commands per Part | 2–5 discrete one-liners | Single multi-line program |
| Lines of code | None, or brief `python3.12 -c "..."` expressions | 10+ lines with control flow |
| Files needed beyond lab markdown | None | One or more demo files |
| Can a student reproduce it by typing? | Yes, comfortably | Only with significant risk of typos |

**Consequences of the decision:**

- **No scaffolding** → no `.sh` / `.py` / `.ts` demo files; students type every command directly into the terminal; `[ID]-code-walkthrough.md` is NOT written (there is nothing to walk through); the two terminal scripts (`[ID]-script-macos.md` and `[ID]-script-linux.md`) are the only instructor assets.
- **Scaffolding required** → write the demo files; `[ID]-code-walkthrough.md` IS written (shared across both platforms); students still type commands themselves when practical, and the demo files are a reference implementation.

Lab 1.5 ("Seeing the Machine") is the canonical example of *no scaffolding needed* — every demo is a single-line `sysctl` / `xxd` / `python3.12 -c "..."` command the student types live. A lab like "Build a TCP server in 30 lines of Python" is the canonical example of *scaffolding required* — the student cannot reasonably type 30 lines correctly on the first try.

The research phase of `/create-lab` is responsible for making this call explicitly and carrying it into the rest of the pipeline.

---

## Interactivity — First-Class Requirement

Interactivity is not optional. Every Part of a lab must include both:

**1. Student types commands directly into the terminal.**

Direct-terminal typing is the primary form of interactivity, not a fallback. In a no-scaffolding lab this means every Part has ≥2 discrete command blocks **per platform** the student types themselves, each with its own labeled output. `bash demo.sh` abstraction is not acceptable as the student's primary action in this mode.

In a scaffolded lab, the student may run the demo file *after* typing at least one command themselves (a warm-up one-liner in the REPL, a `curl` probe, a `docker ps`, etc.). Running a pre-written script is never the only interactive moment in a Part.

**2. A conceptual question testing WHY.**

Not syntax recall or flag trivia. The question requires the student to reason through the concept.

Good: *"Why would the server wait forever if you don't send the blank line?"*
Bad: *"What flag suppresses the progress bar?"*

The test: can a student answer this by thinking through the concept, without memorizing syntax? If yes, it's good. If it's flag trivia, replace it.

Format questions with a collapsible answer:
```
> **Why does X work this way?**
> `<details><summary>Answer</summary>explanation from first principles</details>`
```

---

## Output Standards

**Never invent output.** Every OUTPUT block in a lab or script must be captured from an actual test run of the demo code. No approximations, no reconstructions from memory.

**Variable values:** Some output changes each run (hashes, tokens, timestamps). Paste the actual captured output and add: `*(Your [value] will look different — structure is the same.)*`

**Long output:** If output exceeds 25 lines, use the most instructive portion and add `(output continues...)`.

---

## Demo Code Standards

These rules apply **only to labs that require scaffolding** (see "The scaffolding test" above). Labs without demo files have nothing in this section to satisfy — the terminal commands and their captured outputs inside each track's `<details>` block take the place of demo files.

When a lab requires scaffolding, every demo file must:

- Have a header comment explaining what it is and how to run it
- Have 3–4 sections with clear section banners
- Label every output line so students know what each line means
- End the last section with a practical contrast or demonstration (with-vs-without, tamper detection, before-vs-after)
- Exit with code 0 — no unhandled errors or warnings. Fix the root cause; never suppress.

See `tech-standards/` for language-specific rules.

---

## Research Report Standards

Each report covers:
- **Overview:** 2–3 paragraphs on what the lab covers and why it matters. No jargon without definition.
- **One section per concept:** Background → How it works → Implementation → Sources (≥3 real URLs per concept)
- **Lab Design Decisions:** Key choices explained for a beginner audience (local vs. external API, which tool, why)

All source URLs must be real — taken from actual research, never invented.

---

## README Standards

Each completed lab directory gets a `README.md` that serves as an **instructor-only navigation aid**. It is not distributed to students — the student handout is `[ID]-lab.md`.

The README exists so an instructor opening the folder for the first time knows immediately which files to give to students and which to keep internal. It must NOT duplicate anything already in the lab file — no prerequisites, no setup commands, no time estimate, no "how to run" flags.

Content (exactly these two sections, nothing more):

1. **File-audience table.** One row per file in the lab folder. Columns:
   - `File` — the filename
   - `Audience` — one of `Student`, `Instructor`, `Both`
   - `Purpose` — one concise sentence (e.g., "Lab handout distributed to learners", "Terminal screencast shooting script", "Reference scaffolding code")
2. **Recording order.** One bullet: record the walkthrough first (if present), then the terminal screencast.

Always add a one-line note at the top marking the file as instructor-only (not distributed to students). Omit rows for files that don't exist — for example, a no-scaffolding lab has no demo files and no `[ID]-code-walkthrough.md`, so those rows are absent.
