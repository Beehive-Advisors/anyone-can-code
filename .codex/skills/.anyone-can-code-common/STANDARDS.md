# Course Lab Standards

All three lab skills — `create-lab`, `research-lab`, and `review-lab` — read and apply these standards. They represent the pedagogical principles and quality criteria that every lab must meet.

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

- **No scaffolding** → no `.sh` / `.py` / `.ts` demo files; students type every command directly into the terminal; `[ID]-code-walkthrough.md` is NOT written (there is nothing to walk through); `[ID]-script.md` is the only instructor asset.
- **Scaffolding required** → write the demo files; `[ID]-code-walkthrough.md` IS written; students still type commands themselves when practical, and the scripts are a reference implementation.

Lab 1.5 ("Seeing the Machine") is the canonical example of *no scaffolding needed* — every demo is a single-line `sysctl` / `xxd` / `python3.12 -c "..."` command the student types live. A lab like "Build a TCP server in 30 lines of Python" is the canonical example of *scaffolding required* — the student cannot reasonably type 30 lines correctly on the first try.

The research phase of `/create-lab` is responsible for making this call explicitly and carrying it into the rest of the pipeline.

---

## Interactivity — First-Class Requirement

Interactivity is not optional. Every Part of a lab must include both:

**1. Student types commands directly into the terminal.**

Direct-terminal typing is the primary form of interactivity, not a fallback. In a no-scaffolding lab this means every Part has ≥2 discrete command blocks the student types themselves, each with its own labeled output. `bash demo.sh` abstraction is not acceptable as the student's primary action in this mode.

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

## Self-contained lab directory

**Preferable, not strictly required.** Student work should happen inside the lab's own folder (e.g., `1.5/`) rather than in `/tmp` or the user's home directory. Any files the student creates, any files they inspect, and any artifacts they'll throw away when the lab ends should live within that folder.

Why preferable:

- The lab folder becomes the single artifact an instructor can hand to a student — a USB, zip, Drive share, repo clone — and the student can work end-to-end without leaving it. Nothing gets scattered across the student's machine.
- No network dependency for reference files. Any PNG, compiled binary, or text file the lab analyzes is pre-committed to the folder; students don't need `curl` and don't break when upstream URLs change.
- Cleanup at the end of the lab stays simple. Remove the files the student created; leave the shipped reference files in place.
- Output blocks in the lab become deterministic. Every student running `xxd -l 16 sample.png` on a pre-shipped file sees identical bytes because the file is bit-for-bit the same everywhere.

When leaving the folder is fine:

- Reading system files by absolute path (e.g., `xxd -l 4 /bin/ls`, `cat /proc/cpuinfo`, `sysctl -n hw.memsize`). Those aren't "student artifacts" — they're points of interest elsewhere in the OS.
- Labs whose topic *is* the filesystem convention being taught (e.g., `/tmp`, `/var/log`).
- Demos that genuinely require a specific system location.

**For the lab author:**
- In Setup, tell the student to `cd` into the lab folder and state that they'll stay there for the rest of the lab.
- Ship any reference files the lab inspects (images, binaries, sample inputs) in the folder. Prefer programmatically-generated small files over downloaded ones.
- Keep a short `cd`-teaching-moment the first time the student's working directory matters (see Lab 1.5 Part 4): explain that `cd` is sticky, that `pwd` prints the current directory, and that `cd` with no argument returns home.
- Cleanup at the end of the lab removes student-created files only — the shipped references stay.

---

## Output Standards

**Never invent output.** Every OUTPUT block in a lab or script must be captured from an actual test run of the demo code. No approximations, no reconstructions from memory.

**Variable values:** Some output changes each run (hashes, tokens, timestamps). Paste the actual captured output and add: `*(Your [value] will look different — structure is the same.)*`

**Long output:** If output exceeds 25 lines, use the most instructive portion and add `(output continues...)`.

---

## Demo Code Standards

These rules apply **only to labs that require scaffolding** (see "The scaffolding test" above). Labs without demo files have nothing in this section to satisfy — the terminal commands and their captured outputs in the lab file take the place of demo files.

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
