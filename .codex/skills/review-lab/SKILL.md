---
name: review-lab
description: |
  Review a completed "Anyone Can Code" lab against all quality standards. Checks demo
  code quality, script-lab alignment, course overlap, lab structure and necessity, and
  report quality. Creates README.md for the lab folder. Returns a structured PASS/FAIL
  report by component with specific fix instructions. Invoked by /create-lab or
  standalone. Use when user says "review lab", "check lab", "qa lab", or provides a
  section ID and asks for review.
metadata:
  short-description: Review a completed lab for quality and correctness
---

# /review-lab — Lab Quality Review

You are the quality review phase of the "Anyone Can Code" lab pipeline. Read all files fresh — no assumptions about what they contain.

**Before starting:** Read `.codex/skills/.anyone-can-code-common/references/standards.md`, `.codex/skills/.anyone-can-code-common/references/lab-format.md`, and `.codex/skills/.anyone-can-code-common/references/script-format.md`. Detect the file extensions present in `$0/` and read the relevant `.codex/skills/.anyone-can-code-common/references/tech-standards/<lang>.md` files. These are the complete criteria you will apply.

## Arguments

- `$0` — Lab section ID (e.g., "5.7"). Required.

## Setup

- `LAB_DIR` = `$0/`
- `LAB_PREFIX` = `$0`

Read all files in `LAB_DIR`. Required files:
- `{LAB_PREFIX}-lab.md` — student lab
- `{LAB_PREFIX}-script-macos.md` — macOS terminal script
- `{LAB_PREFIX}-script-linux.md` — Linux terminal script
- `{LAB_PREFIX}-report.md` — research report

If any of these don't exist, stop and report what's missing. (The code walkthrough file `{LAB_PREFIX}-code-walkthrough.md` is optional — only present for scaffolded labs.)

---

## Pass 1: Demo Code + Script-Lab Alignment

**First, determine the scaffolding mode for this lab.**

Use `Glob` to check for demo files in `LAB_DIR` matching `*.sh`, `*.py`, `*.ts`, `*.js`, `Dockerfile`, `*.yaml`, `*.yml`. Store the result as `SCAFFOLDED` (boolean):
- `SCAFFOLDED = true` if any such files exist
- `SCAFFOLDED = false` if only markdown files exist

The rest of Pass 1 branches on this.

### 1a. Demo Code Quality — scaffolded labs only

**If `SCAFFOLDED = false`:** skip this subsection — mark it `N/A (direct-typing lab — no demo files)` in the report and move to 1b.

**If `SCAFFOLDED = true`:** for each demo file, check language-specific rules from the relevant `.codex/skills/.anyone-can-code-common/references/tech-standards/*.md` file.

**Universal checks for all demo files:**
- Exits with code 0 — run it and capture stdout+stderr
- Zero warnings or errors on run
- Has a file header explaining what it is and how to run it
- Has 3–4 sections with clear section banners
- Every output line is labeled
- Last section is a practical contrast or demonstration
- Section structure is present

**Run each file:**
- `.sh`: `bash <filename> 2>&1; echo "Exit: $?"`
- `.py`: `cd $0 && source .venv/bin/activate && python3.12 <filename> 2>&1; echo "Exit: $?"`
- `.ts`/`.js`: `cd $0 && npx ts-node <filename> 2>&1; echo "Exit: $?"`
- `Dockerfile`: `docker build -t test-lab . 2>&1; echo "Exit: $?"`
- Kubernetes YAML: `kubectl apply -f <file> --dry-run=client 2>&1; echo "Exit: $?"`

Apply all rules from the matching `.codex/skills/.anyone-can-code-common/references/tech-standards/<lang>.md` to each file.

### 1b. Script ↔ Lab Alignment

Read `{LAB_PREFIX}-lab.md`, `{LAB_PREFIX}-script-macos.md`, and `{LAB_PREFIX}-script-linux.md`.

**Checks applied to BOTH script files:**
- [ ] Every `## Part N` in the lab has a matching `## PART N` section in this script
- [ ] Every exercise in the lab has a TYPE + OUTPUT beat in this script showing the solution
- [ ] Every run-the-demo block in the lab has a corresponding TYPE + OUTPUT + EXPLAIN sequence in this script
- [ ] Every beat in this script is labeled SPEAK / TYPE / OUTPUT / EXPLAIN — no unlabeled prose
- [ ] This script has INTRO, PUTTING IT TOGETHER, OUTRO, and Recording notes sections

**Checks applied across the two scripts:**
- [ ] The two scripts are in lockstep: same Part count, same exercise count, same SPEAK narration for platform-neutral concepts
- [ ] TYPE commands differ where expected (macOS uses macOS syntax; Linux uses Linux syntax) and match the 🍎 / 🐧 command blocks in the lab markdown
- [ ] OUTPUT blocks differ where expected (macOS output vs Linux output) but come from tested runs on the corresponding platform — never copy-pasted between scripts

### 1c. Scaffolding Consistency

The lab's scaffolding mode must be internally consistent. FAIL the lab if not.

**If `SCAFFOLDED = true`:**
- [ ] `{LAB_PREFIX}-code-walkthrough.md` exists (single shared file, not duplicated per platform)
- [ ] Walkthrough opens files with `code [filename]` (VS Code) — not `cat` or `less`
- [ ] Walkthrough has a conceptual section BEFORE any code sections — every term the code uses is defined before the code section that uses it
- [ ] All EXPLAIN beats have: parenthetical `(lines N–M — description)`, fenced code block in the application language, line-number-specific narration
- [ ] Each Part's "Run the demo" in the lab includes ≥1 student-typed command per platform (not only `bash demo.sh`)

**If `SCAFFOLDED = false`:**
- [ ] `{LAB_PREFIX}-code-walkthrough.md` does NOT exist. A direct-typing lab has nothing to walk through — its presence indicates leftover scaffolded-mode content that should be removed or converted.
- [ ] Each Part's "Run the demo" in each track contains ≥2 discrete TYPE+OUTPUT command blocks in that track's native syntax — no `bash demo.sh` abstraction, no single collapsed dump, no dual 🍎/🐧 blocks inside a single track
- [ ] The lab's header block does NOT have a `**Files:**` line (there are no demo files to point at)

Also — regardless of scaffolding mode — check:
- [ ] Exactly two per-platform script files exist: `-script-macos.md` AND `-script-linux.md` (never just one, never `-script.md` without suffix)

Flag any violation as FAIL with the exact fix instruction.

### 1d. Cross-platform Track Consistency

Every lab must carry a macOS track AND a Linux track, each as a full standalone lab inside its own collapsible at the top of the file. Read `{LAB_PREFIX}-lab.md`.

- [ ] Has a `## Pick your track` section immediately after the file header (no `## What you'll build` or any other section outside the two collapsibles)
- [ ] That section contains exactly two top-level `<details>` blocks — one per platform — and NOTHING else between them except whitespace
- [ ] The first `<details>` summary clearly identifies macOS (e.g., `🍎 Click here if you're on macOS`); the second clearly identifies Linux / WSL
- [ ] Each `<details>` block contains a full standalone track for that platform: What-you'll-build, Setup, all Parts, Putting-it-together, Checklist, Further Reading. The body of the lab lives INSIDE these collapsibles, not outside.
- [ ] The two tracks mirror each other beat-for-beat: same Part count, same exercise count, same conceptual `### What is X?` section count, same WHY question count
- [ ] Inside a track, commands are platform-native — no `**🍎 macOS**` or `**🐧 Linux / WSL**` dual-label blocks inside a single track (that was an old format). The macOS track uses macOS-native commands only; the Linux track uses Linux-native commands only.
- [ ] OUTPUT blocks in the macOS track are verbatim from a macOS run; OUTPUT blocks in the Linux track are verbatim from a Linux run (kubectl pod or Docker Ubuntu). If a Linux output was sourced from research instead of a tested run, it must carry the `*(Linux output from Ubuntu 22.04; your values may differ by distro.)*` marker.
- [ ] Platform-neutral content (conceptual intros, WHY questions, Putting-it-together, Checklist, Further Reading) appears **twice** — once inside each track. This duplication is intentional; flag it as a violation if the content is only present in one track and missing from the other.

Flag any violation as FAIL with the exact fix instruction.

---

## Pass 2: Lab + Report Content Quality

### 2a. Lab Structure and Interactivity

Read `{LAB_PREFIX}-lab.md`.

**Structure checks (follow `.codex/skills/.anyone-can-code-common/references/lab-format.md`):**
- [ ] Header has Section, Prerequisites, Time
- [ ] Header has a `**Files:**` line **only if** `SCAFFOLDED = true` (direct-typing labs omit it)
- [ ] Has `## Pick your track` section immediately after the file header containing two full-track `<details>` collapsibles (the entire lab body lives inside them)
- [ ] Inside each track: `## What you'll build` with numbered concrete outcomes
- [ ] Inside each track: `## Setup` with install commands in that track's platform-native syntax (`brew install` in the macOS track, `sudo apt install` in the Linux track)
- [ ] Inside each track: every `## Part N` has a `### What is X?` intro, a run-the-demo block in that track's platform-native syntax, a conceptual question, and an `### Exercise`
- [ ] Every exercise has `<details><summary>Solution</summary>` collapsible block (with dual solutions when the command is platform-specific)
- [ ] Has `## Putting it together`, `## Checklist`, `## Further Reading` (≥3 links)

**First-principles check (spot-check first 5 technical terms):**
For each of the first 5 technical terms introduced, verify it is explained from first principles before it's used as if already known. Flag any term that appears without prior definition.

**Interactivity check (per `.codex/skills/.anyone-can-code-common/references/standards.md`):**
- [ ] Every Part has the student typing commands directly in the terminal
  - Direct-typing labs (`SCAFFOLDED = false`): every Part has ≥2 discrete student-typed TYPE+OUTPUT command pairs **per platform** — never a single `bash demo.sh` abstraction
  - Scaffolded labs (`SCAFFOLDED = true`): every Part has ≥1 student-typed command per platform alongside or before the `bash demo.sh` / `python3.12 demo.py` run
- [ ] Every Part has ≥1 question testing WHY (not syntax recall or flag trivia)
- [ ] All questions use `<details><summary>Answer</summary>` collapsible format

**Necessity check (ruthless):**
For every section and paragraph, ask: is this required to meet a stated learning objective?

Flag with a specific fix:
- Paragraphs that repeat content from a prior section
- Exercises that test the same skill as a prior exercise without adding new understanding
- Sections that could be cut without the student losing a learning objective

### 2b. Report Quality

Read `{LAB_PREFIX}-report.md`.

- [ ] Has `## Overview` (2–3 paragraphs)
- [ ] Has one section per major concept with Background, How it works, Implementation, and Sources (≥3 real URLs)
- [ ] All URLs are real — spot-check at least 2
- [ ] Has `## Lab Design Decisions` section

### 2c. Course Overlap

Read `LAB_COVERAGE.md` from the repo root. Find all sections for labs OTHER THAN `$0`.

For each concept, tool, and exercise in the current lab (`{LAB_PREFIX}-lab.md`):
- [ ] Check whether it is already listed as a primary teaching point in another lab's entry in `LAB_COVERAGE.md`
- [ ] Report duplicates as **WARN** (not FAIL) — some reinforcement is intentional; full re-explanation of something already taught is not

If `LAB_COVERAGE.md` does not exist or contains no other labs: "No prior lab coverage — overlap check skipped."

---

## Write README.md

After both passes pass, write `LAB_DIR/README.md`. The README is an **instructor-only navigation aid** — it is not distributed to students. Do NOT duplicate prerequisites, setup commands, time estimates, or "how to run" flags — those live in `[LAB_PREFIX]-lab.md`.

Build the file-audience table dynamically from the files that actually exist in `LAB_DIR`. Omit rows for files that do not exist (no-scaffolding labs have no demo files and no code walkthrough).

Template:

```markdown
# Lab $0 — Instructor README

> Instructor-only. Not distributed to students. See `$0-lab.md` for the student handout.

| File | Audience | Purpose |
|------|----------|---------|
| `$0-lab.md` | Student | Lab handout distributed to learners — contains both 🍎 macOS and 🐧 Linux/WSL tracks with a toggle at the top |
| `$0-script-macos.md` | Instructor | macOS terminal screencast shooting script |
| `$0-script-linux.md` | Instructor | Linux / WSL terminal screencast shooting script |
| `$0-report.md` | Instructor | Research background and sources |
| `$0-code-walkthrough.md` | Instructor | VS Code walkthrough script (shared across both platform recordings) |
| `[demo-file-1]` | Both | Reference implementation — instructor runs during recording; students may run as an alternative to typing |
| `[demo-file-2]` | Both | [one-sentence purpose] |

## Recording order

1. Record the code walkthrough (if present — scaffolded labs only).
2. Record the macOS terminal screencast (`$0-script-macos.md`) natively on your Mac.
3. Record the Linux / WSL terminal screencast (`$0-script-linux.md`) from a kubectl pod on the k0s cluster (preferred), a Docker Ubuntu container, WSL2, or a Linux VM.
```

Row-inclusion rules:
- `$0-lab.md`, `$0-script-macos.md`, `$0-script-linux.md`, `$0-report.md` — always present
- `$0-code-walkthrough.md` row — include **only if** the file exists (scaffolded labs)
- One row per demo file — include **only** demo files actually present in `LAB_DIR`; no demo-file rows in a direct-typing lab

Keep each `Purpose` cell to one short sentence. Do not include columns like "How to run" or "Size" — the file table is the student-vs-instructor navigation aid and nothing more.

---

## Report Format

```
# Review Report: Lab $0

**Scaffolding mode:** direct-typing | scaffolded  (state which, based on files present)

## Pass 1: Demo Code + Alignment     [PASS / FAIL]

### Demo Code
- [N/A] Direct-typing lab — no demo files
(or)
- [PASS] hash_demo.py — exits 0, no warnings, all checks pass
- [FAIL] jwt_demo.py — line 22: datetime.utcnow() → fix: use datetime.now(timezone.utc)

### Script ↔ Lab Alignment
- [PASS] All Parts match
- [FAIL] Exercise in Part 2 has no TYPE beat → add solution TYPE + OUTPUT after "### Exercise — Decode by hand"

### Scaffolding Consistency
- [PASS] No demo files present and no code walkthrough — consistent direct-typing mode
- [PASS] Each Part has ≥2 discrete student-typed command pairs
(or)
- [FAIL] 5.7-code-walkthrough.md exists but no demo files → delete the walkthrough (direct-typing lab) OR add the demo files it references (scaffolded lab)

## Pass 2: Lab + Report Quality      [PASS / FAIL]

### Lab Structure and Interactivity
- [PASS] All structural checks pass
- [FAIL] Part 1 has only a single `bash demo.sh` call → split into 2+ discrete TYPE+OUTPUT command pairs the student types live
- [CUT]  Lines 180–195 go beyond lab objectives → recommend removing

### Report Quality
- [PASS] All checks pass

### Course Overlap
- [PASS] No overlapping concepts

---
README.md written to $0/README.md
```

End with either "All components PASS. Ready for commit." or "Fix the FAIL items above, then re-run /review-lab $0."
