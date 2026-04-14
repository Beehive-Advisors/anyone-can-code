---
name: create-lab
description: |
  Create a complete lab for the "Anyone Can Code" Udemy course. Fully autonomous:
  reads SYLLABUS.md, researches the topic, writes demo files, tests them, writes
  the student lab, instructor script, and research report, runs a quality review,
  and commits + pushes to GitHub. Use when user says "create lab", "build lab",
  "make lab", "new lab", or gives a section ID like "5.7" and asks to build it.
user_invocable: true
argument-hint: <section-id>
allowed-tools: Read Write Edit Glob Grep Bash Agent WebSearch WebFetch
---

# /create-lab — Full Lab Creation

You are building a complete lab for the "Anyone Can Code" Udemy course. This is a fully autonomous workflow — run all phases to completion without pausing for user confirmation unless something breaks.

## Arguments

- `$0` — Lab section ID (e.g., "5.7", "6.1"). Required.

## Paths

Throughout this skill, use these exact paths:
- `REPO_ROOT` = current working directory (the repo root, where `SYLLABUS.md` lives)
- `LAB_ID` = `$0` (e.g., `5.7`)
- `LAB_DIR` = `$0/` relative to repo root (e.g., `5.7/`)

---

## PHASE 0: Preflight

**Step 1: Check if lab already exists**

Use Glob to check if `LAB_DIR` contains any `.md` files:
```
pattern: $0/*.md
```
If any `.md` files are found, **stop immediately** and tell the user:
> "Lab `$0` already exists with existing `.md` files. Delete `$0/` first or choose a different section ID."
Do not proceed.

**Step 2: Read the syllabus**

Read `SYLLABUS.md` in the repo root. Find the entry for section `$0`.

Extract:
- `TOPIC_TITLE` — the topic name for this lab (e.g., "Rate Limiting and Throttling")
- `LEARNING_OBJECTIVES` — the bullet points listed under this section
- `PREREQUISITES` — any prerequisite labs mentioned

If `SYLLABUS.md` does not exist or section `$0` is not found: **stop** and ask the user:
> "Section `$0` was not found in `SYLLABUS.md`. What is the topic title and learning objectives for this lab?"

**Step 3: Proceed**

Print: `"Creating Lab $0: [TOPIC_TITLE] — starting research phase..."`
Then continue immediately without waiting for confirmation.

---

## PHASE 1: Research

Use the Agent tool to run the research phase in isolation. This keeps the research context (web pages, search results) out of the main context window.

Spawn an Agent with:
- `description`: `"Research for Lab $0: [TOPIC_TITLE]"`
- `subagent_type`: `"general-purpose"`
- `prompt`: the following (substitute `$0`, `TOPIC_TITLE`, and `LEARNING_OBJECTIVES` with actual values):

---
**[AGENT PROMPT — substitute values before spawning]**

You are researching the topic "[TOPIC_TITLE]" for Lab $0 of the "Anyone Can Code" beginner programming course. The audience is non-technical adults learning to code for the first time — they know basic Python but nothing about [TOPIC_TITLE].

Learning objectives from the syllabus:
[LEARNING_OBJECTIVES]

Use WebSearch and WebFetch to research every concept listed. For EACH concept, produce:

**1. First-principles explanation**
What problem does this solve? Explain the concept before naming it. No jargon until the idea is established. Write as if explaining to a smart adult with no CS background.

**2. Internal mechanics**
The actual algorithm, protocol steps, or data flow. What happens at the byte/function level. Not just "what it does" — "how it works."

**3. Python library**
- Exact PyPI package name
- Current stable version
- Install command: `uv pip install <name>`
- Key function signatures
- 5-line core usage example

**4. Constraints and gotchas** (critical for avoiding bugs in demo code)
- Input type requirements (bytes vs. str)
- Key/parameter length requirements
- Deprecated functions in Python 3.12
- Version compatibility issues
- Any other non-obvious requirements

**5. Source URLs** (minimum 3 per concept)
- Official documentation
- RFC or spec (if applicable)
- PyPI page
- A well-known tutorial (Real Python, MDN, OWASP, etc.)

**6. Demo design**
Suggest 3–4 sections for a demo `.py` file that shows the concept working. Each section should print intermediate values so students see the internals, not just the final result.

**Lab design rationale:**
- Local demo server vs. real external API? Which is better for beginners here, and why?
- Any concepts demonstrable with stdlib only (no third-party library)?
- What's the minimum demo that delivers the key insight?

Return the complete research dump in structured markdown. Do NOT truncate. Use this format:

```
# Research Dump: Lab $0 — [TOPIC_TITLE]

## Concept 1: [Name]
### First-Principles Explanation
### Internal Mechanics
### Python Library: [name]
### Constraints and Gotchas
### Demo Sections
### Sources

## Concept 2: [Name]
[same structure]

## Lab Design Rationale
[key decisions]
```
---
**[END AGENT PROMPT]**

Store the Agent's full return value as `RESEARCH_DUMP`. Do not proceed to Phase 2 until the Agent completes.

---

## PHASE 2: Plan Demo Files

Using `RESEARCH_DUMP` and `LEARNING_OBJECTIVES`, decide and write down a concrete plan before touching any files:

1. **How many Python demo files?** One per major concept. Name them `{concept}_demo.py` (e.g., `hash_demo.py`, `jwt_demo.py`).
2. **Shell scripts needed?** Only if a demo requires two simultaneous processes (e.g., a local server + a client). Name them `{concept}_flow.sh`.
3. **What sections does each file have?** 3–4 sections per file. Name each section (e.g., "Section A: Hashing a password", "Section B: Verifying").
4. **What PyPI packages are needed?** List exact names for `uv pip install`.
5. **What will each section print?** Describe the expected output structure (not exact values — just the labels and data types).

Write this plan as a numbered list. Keep it. It drives the rest of Phase 3.

---

## PHASE 3: Create Directory and Write Demo Files

**Step 1: Create the directory**
```bash
mkdir -p $0
```

**Step 2: Set up Python environment**
```bash
cd $0 && uv venv .venv --python 3.12 && source .venv/bin/activate && uv pip install [packages from Phase 2]
```
If `uv pip install` fails: **stop immediately** and report the exact error. Do not proceed until dependencies install cleanly.

**Step 3: Write each demo file**

Use the `Write` tool to create each `.py` and `.sh` file in `LAB_DIR`.

### Non-negotiable rules for EVERY Python demo file:

**File header (exactly this format):**
```python
#!/usr/bin/env python3
"""
Lab $0 – Part N: [CONCEPT NAME]
Run: python3.12 [filename].py
"""
```

**Imports:** All at top of file. stdlib before third-party. One blank line between stdlib and third-party blocks.

**Section banners (use this exact format for every section):**
```python
# ─────────────────────────────────────────────────────────────────────────────
# Section A: [description]
# ─────────────────────────────────────────────────────────────────────────────

print()
print("=" * 70)
print("SECTION A — [description]")
print("=" * 70)
```

**Labeled output:** Every print statement must have a label so students know what they're reading:
- Good: `print(f"Hash      : {hash_value}")`
- Good: `print(f"Token:\n{token}\n")`
- Bad: `print(hash_value)` (unlabeled — student doesn't know what this is)

**Python 3.12 datetime:** Always use `datetime.now(timezone.utc)`, never `datetime.utcnow()` (deprecated).

**PyJWT HS256 key:** Must be exactly 32 bytes. Use: `SECRET = "this-is-exactly-32-bytes-long!!!"` (count: 32 chars). Do not use any other length.

**bcrypt inputs:** Must be bytes: `bcrypt.hashpw(b"my-password", salt)` — not `"my-password"`.

**No `warnings.filterwarnings("ignore")`:** Never suppress warnings. Fix the underlying cause instead.

**Section count:** At least 3 sections per file, ideally 4. The last section should always be a practical demonstration (tampering attempt, timing comparison, verification, etc.).

### Non-negotiable rules for shell scripts:

```bash
#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# [Description of what this script demonstrates]
# ─────────────────────────────────────────────────────────────────────────────
```

Each `curl` command must have a comment above it explaining what it does and why.

---

## PHASE 4: Run and Test ALL Demo Files — Capture Exact Output

**This phase is the most critical.** The script and lab must use actual tested output, not invented output. Do this phase completely before writing any `.md` files.

### For each Python file:

```bash
cd $0 && source .venv/bin/activate && python3.12 [filename].py 2>&1
```

**If exit code is not 0:** Stop. Read the error. Fix the file using `Edit`. Re-run. Do NOT proceed to the next file until this one exits cleanly.

**Common errors and fixes:**
- `ImportError` → run `uv pip install <missing-package>` in the venv
- `ValueError: The secret ... is too short` (PyJWT) → count the SECRET characters — must be exactly 32
- `DeprecationWarning: datetime.utcnow()` → replace with `datetime.now(timezone.utc)`
- `TypeError: Unicode-objects must be encoded before hashing` (bcrypt) → use `b"..."` bytes, not `"..."` str

### For shell scripts (if any):

These typically require a background server:
```bash
cd $0 && source .venv/bin/activate
python3.12 [server_file].py &
SERVER_PID=$!
sleep 1
bash [script_file].sh 2>&1
kill $SERVER_PID
```

### Store the output:

After each file runs successfully, mentally store its complete stdout as `OUTPUT_[filename]` (e.g., `OUTPUT_hash_demo`, `OUTPUT_jwt_demo`). These stored outputs will be pasted **verbatim** into the OUTPUT blocks in Phase 6 (script). Never paraphrase or reconstruct from memory — use the actual captured text.

**Note on random values:** Some output contains random values (bcrypt hashes, JWT tokens, nonces). These will differ on every run. When writing OUTPUT blocks, paste the actual output you captured, and add a note after the block: `*(Your [value] will look different — the salt/key is random each run. Structure won't change.)*`

---

## PHASE 5: Write Research Report

Write `$0/[LAB_ID]-report.md`.

**Target length:** 200–400 lines.

**Structure:**

```markdown
# Research Report: Lab $0 — [TOPIC_TITLE]

## Overview

[2–3 paragraphs summarizing what the lab covers and why these mechanisms matter
in real systems. No jargon without definition.]

---

## 1. [Concept One Name]

### Background

[First-principles explanation. Assume reader knows basic programming but not this topic.
Start with the problem being solved, not the solution.]

### How it works

[Internal mechanics. Use tables for comparisons where helpful. ASCII diagrams are fine.]

### Python library: [package-name]

[Key functions, signatures, and one short code example showing core usage.]

```python
import package
# core usage in 5 lines
```

**Sources:**
- [Title](URL) — [one-line description]
- [Title](URL)
- [Title](URL)
(minimum 3 per concept, from RESEARCH_DUMP — all URLs must be real)

---

## 2. [Concept Two Name]

[same structure as Concept 1]

---

## Lab Design Decisions

### [Key decision heading]
[Explain why this approach was chosen for a beginner audience.]

### [Other constraint or tradeoff]
[Explanation.]
```

All source URLs must come from `RESEARCH_DUMP`. Do not invent URLs.

---

## PHASE 6: Write Student Lab

Write `$0/[LAB_ID]-lab.md`.

**Target length:** 500–700 lines.

### Critical accessibility rule (non-negotiable):

Every technical term must be defined from first principles **the first time it appears**. Never use a term as if the reader already knows it.

- **Wrong:** "bcrypt is a password hashing function that..."
- **Right:** "A hash function takes any input — a word, a file, a whole database — and produces a fixed-length string of characters. [explain hash properties] ... bcrypt is a hash function designed specifically for passwords."

Pattern: establish the concept → then name it → then use it freely.

### Structure:

```markdown
# Lab $0 — [TOPIC_TITLE]

**Section:** [Course section name, e.g., "Security"]
**Prerequisites:** [List from PREREQUISITES]
**Time:** ~N minutes
**Files:** `$0/`

---

## What you'll build

[Numbered list of 3–5 concrete, specific things the student will have done by the end.
Each item should be something they can show someone: "I hashed a password with bcrypt",
not "I learned about hashing".]

---

## Setup

### Prerequisites

[Short checklist of required tools with version-check commands.]

### Install dependencies

```bash
cd ~/src/courses/anyone-can-code/$0
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install [packages]
```

[Explain what each package does in one plain-English sentence.]

### Terminal setup [INCLUDE ONLY if multi-process demo needed]

[Explain which terminal runs which process and when to open the second one.
Be specific: "Terminal 1 runs the server. Terminal 2 runs the curl commands."]

---

## Part 1 — [Concept Name]

### What is [term]?

[First-principles explanation. Start with an analogy or a problem statement before the
technical definition. 2–4 paragraphs. No term left undefined.]

### [Mechanic or detail]

[Internal mechanics explained with the student's perspective in mind. Reference specific
output from the demo to ground the explanation.]

### Run the demo

```bash
python3.12 [filename].py
```

[Paste the output of Section A from OUTPUT_[filename] verbatim. After each section's output,
explain what the student is looking at.]

```
[EXACT OUTPUT FROM PHASE 4 — paste verbatim]
```

[Explanation of what each labeled line means.]

### Exercise

[One concrete exercise that takes 5–15 minutes. Must require them to write code or run
a command, not just read. Must build directly on what was just demonstrated.]

<details>
<summary>Solution</summary>

```python
[solution code]
```

[Brief explanation of why this is the solution]

</details>

---

[Repeat Part structure for each concept]

---

## Putting it together

[Comparison table with columns: Mechanism | What problem it solves | Key idea | Where you see it in real systems]

[1–3 sentences describing how these mechanisms work together in a real authentication system.]

---

## Checklist

- [ ] [One checkbox per concrete skill the student should now be able to do or explain]
- [ ] [...]

---

## Further Reading

- [Title](URL) — [one-line description]
- [Title](URL) — [one-line description]
- [Title](URL) — [one-line description]
(minimum 3 links, from RESEARCH_DUMP — must be real URLs)
```

**Output blocks in the lab must use the exact text from Phase 4 captures.** Never invent output.

---

## PHASE 7: Write Instructor Script

Write `$0/[LAB_ID]-script.md`.

**Target length:** 600–800 lines.

### Non-negotiable beat format:

Every single instructor action must be labeled. No unlabeled prose anywhere in the script body.

```
**SPEAK**
> "Spoken words. First-principles explanation before any jargon. Short sentences."

**TYPE**
```bash
exact command to type
```

**OUTPUT**
```
exact terminal output — copied verbatim from Phase 4 captures
```

**EXPLAIN**
> "What to say while the output is visible. Walk through specific lines. Reference exact labels."
```

**Rules for each beat type:**

**SPEAK beats:**
- First-principles explanation before every new concept
- No jargon until the concept is established
- Conversational, short sentences — this is spoken aloud
- Set up what the student is about to see BEFORE they see it

**TYPE beats:**
- Exact keystrokes only
- If it's a code edit (exercise solution), show the code block to add
- Never paraphrase commands

**OUTPUT beats:**
- **EXACT text from Phase 4 captures — never invented**
- If output is long (>25 lines), use the most instructive portion and add `(output continues...)`
- Add a note after random-value outputs: `*(Your [hash/token/value] will look different — structure is the same.)*`

**EXPLAIN beats:**
- Walk through output line by line for the key sections
- Reference specific labels: "Look at the `$12` — that's the cost factor"
- Connect back to the first-principles explanation from the SPEAK beat

### Structure:

```markdown
# Instructor Script — Lab $0: [TOPIC_TITLE]

**Format:** Screencast — terminal only
**Estimated recording time:** ~N–M min
**Terminal:** VS Code integrated terminal or iTerm2. Font size 16+, dark theme.

---

## How to read this script

Every beat is labeled:

> **SPEAK** — say this out loud
> **TYPE** — type this into the terminal
> **OUTPUT** — what you will see on screen (exact, from tested run)
> **EXPLAIN** — say this while the output is visible on screen

---

## INTRO

**SPEAK**
> "[Opening line setting up why these mechanisms matter. What will the student be able to do after this lab?]"

**TYPE**
```bash
cd ~/src/courses/anyone-can-code/$0
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install [packages]
```

**OUTPUT**
```
[Paste exact install output from Phase 4]
```

**EXPLAIN**
> "[Explain what uv is and why we use it. Point to the package versions in the output.]"

---

## PART N — [CONCEPT NAME]

---

### What is [concept]?

**SPEAK**
> "[First-principles explanation. Establish the concept without naming it first. Then name it.]"

---

### Run the demo

**TYPE**
```bash
python3.12 [filename].py
```

**OUTPUT**
```
[Paste SECTION A output verbatim from Phase 4]
```

*(Your [value] will look different — structure is the same.)*

**EXPLAIN**
> "[Walk through the output. Reference specific labeled fields. Connect to the SPEAK explanation.]"

[Continue with OUTPUT + EXPLAIN pairs for each remaining section of the demo output]

---

### Exercise — [Exercise Name]

**SPEAK**
> "[Describe what the exercise asks the student to do. Explain WHY this exercise matters.]"

**TYPE**
```python
[solution code to add to the file]
```

**TYPE**
```bash
python3.12 [filename].py
```

**OUTPUT**
```
[Paste exact output showing the exercise result from Phase 4]
```

**EXPLAIN**
> "[Walk through what the solution does and what the output shows.]"

---

[Repeat PART N structure for each concept]

---

## PUTTING IT TOGETHER

**SPEAK**
> "[2–4 sentences connecting all the mechanisms in a real system. How do these three things work together in a login flow?]"

---

## OUTRO

**SPEAK**
> "[3 concrete things the student can now do. Frame as skills, not knowledge: 'You can now decode any JWT with two shell commands', not 'You now understand JWT'.]"

---

## Recording notes

- [Specific tip for this lab's content — e.g., "Let the timing table sit on screen for 2 seconds before speaking"]
- [Multi-terminal tip if applicable — "Keep both terminals visible simultaneously during Part 3"]
- [Font/zoom reminder for any particularly long output blocks]
- [Tip about pacing around the most complex output section]
```

**All OUTPUT blocks must use verbatim Phase 4 captures.** Never write invented output.

---

## PHASE 8: Quality Review

Use the Agent tool to run the review phase independently. This ensures the review agent reads the files fresh, with no memory of how they were written.

Spawn an Agent with:
- `description`: `"Quality review for Lab $0: [TOPIC_TITLE]"`
- `subagent_type`: `"general-purpose"`
- `prompt`: the following (substitute actual values for `$0`):

---
**[AGENT PROMPT — substitute values]**

You are a quality reviewer for the "Anyone Can Code" course. Review the lab at `$0/` against the following checklist. Read every file fresh. Run every demo file. Be ruthless.

**Component 1: Demo Code Quality**
For each `.py` file in `$0/`:
- Run it: `cd $0 && source .venv/bin/activate && python3.12 <file> 2>&1; echo "Exit: $?"`
- Check: exits 0, zero warnings, has shebang + docstring, section banners present, no `datetime.utcnow()`, bcrypt inputs are bytes, PyJWT key is exactly 32 bytes, every print line is labeled

**Component 2: Script ↔ Lab Alignment**
Read both `$0/$0-lab.md` and `$0/$0-script.md`.
- Every Part in lab has a section in script
- Every exercise in lab has a TYPE + OUTPUT beat in script with the solution
- Every output shown to students in lab has a corresponding OUTPUT beat in script
- Every SPEAK beat in script covers a concept introduced in the lab
- Every beat in script is labeled SPEAK/TYPE/OUTPUT/EXPLAIN — no unlabeled prose

**Component 3: Course Overlap**
Use Glob to list all `*/` directories. For each other lab, read its lab `.md` if present.
- Flag concepts already covered in another lab
- Flag prerequisites referenced that don't have a corresponding directory

**Component 4: Lab Structure + Necessity**
- Every technical term defined before first use (spot-check first 5)
- Every Part has an Exercise with `<details><summary>Solution`
- Has Checklist and Further Reading sections
- Necessity check: flag any paragraph or section that could be cut without losing a learning objective

**Component 5: Report Quality**
- Has Sources with ≥3 real URLs per concept
- Has Lab Design Decisions section

**Then: Write `$0/README.md`** with: 1–2 sentence description, prerequisites, setup commands (`uv venv .venv --python 3.12`, activate, uv pip install), file table (filename → description → how to run), time estimate.

Return a structured PASS/FAIL report by component. For each FAIL, include the specific fix.
---
**[END AGENT PROMPT]**

**If the review agent returns any `[FAIL]` items:**
Fix them using `Edit`. Re-run the specific check (e.g., re-run the demo file, re-read the failing section). Then proceed to Phase 9.

**If all items PASS:** Proceed to Phase 9.

---

## PHASE 9: Commit and Push

```bash
# Verify remote
git remote -v
```
Expected: `origin → git@github.com:Beehive-Advisors/anyone-can-code.git` (or https equivalent)
If wrong remote: **stop** and report.

```bash
# Stage only the lab directory — never .venv
git add $0/
git status
```

Read the `git status` output. If `.venv` appears in the staged files:
```bash
git rm -r --cached $0/.venv
```

```bash
git commit -m "Add Lab $0: [TOPIC_TITLE]"
git push origin main
```

If push is rejected (non-fast-forward): report the exact error and tell the user:
> "Remote has changes. Run `git pull --rebase origin main`, then re-run Phase 9."
Do **not** force-push.

Print the full `git push` output. If it succeeds, confirm:
> "Lab $0 committed and pushed to Beehive-Advisors/anyone-can-code. Done."

---

## Error Reference

| Situation | Action |
|-----------|--------|
| LAB_DIR has existing `.md` files | Stop — warn user, do not overwrite |
| SYLLABUS.md missing or section not found | Stop — ask user for topic title |
| `uv pip install` fails | Stop — report exact error |
| Demo file exits non-0 | Fix with Edit, re-run before proceeding |
| Review returns FAIL items | Fix, re-verify, then proceed |
| Git push rejected | Report error, tell user to `git pull --rebase`, do not force-push |
