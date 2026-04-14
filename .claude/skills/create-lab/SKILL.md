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

## PHASE 2: Choose Technology and Plan Demo Files

Using `RESEARCH_DUMP` and `LEARNING_OBJECTIVES`, make a technology decision FIRST. Write the plan down before creating any files.

### Step 2a: Choose the Technology Stack

Apply this decision framework — always prefer the most direct, least-abstracted tool:

| If the lab is about... | Preferred approach |
|------------------------|-------------------|
| Protocols and networking (HTTP, DNS, TCP, TLS) | Shell scripts — `curl`, `nc`, `openssl`, `dig`, `tcpdump` |
| OS and system tools (processes, files, permissions) | Shell commands directly; minimal wrapper scripts |
| Crypto, auth, hashing, JWT | Python 3.12 via `uv` — best libraries, short readable demos |
| Backend API / server | Python (FastAPI/Flask) OR TypeScript (Express/Node) — pick based on what's taught |
| Frontend / full-stack UI | TypeScript + Next.js 15 + shadcn/ui + Tailwind CSS |
| Databases | Direct CLI tools first (psql, redis-cli, mongosh), driver/ORM only if needed |
| Containers | Docker CLI + shell scripts; `kubectl` for Kubernetes labs |
| Infrastructure (nginx, load balancing, VPCs) | Shell + cloud CLI tools (aws, gcloud); YAML/config files |
| GPU / ML workloads | Python 3.12 via `uv` with PyTorch; shell for nvidia-smi |

**Rule: Shell before Python. CLI before library. Add a higher-level language only when its libraries or abstractions are explicitly what's being taught.**

Document your decision: "This lab uses [TECH STACK] because [REASON]."

### Step 2b: Plan the Demo Files

Based on your technology choice, plan:

1. **What files are needed?** Name them descriptively:
   - Shell: `{concept}_demo.sh`, `{concept}_flow.sh`
   - Python: `{concept}_demo.py`
   - TypeScript: `{concept}_demo.ts`, or a Next.js app scaffold
   - Config files: `nginx.conf`, `Dockerfile`, `deployment.yaml`, `compose.yaml`

2. **What sections does each file have?** 3–4 sections per file with clear banners.

3. **What dependencies are needed?**
   - Shell-only: none (check if `nc`, `tcpdump`, etc. need `brew install` on macOS)
   - Python: exact PyPI packages for `uv pip install`
   - TypeScript/Node: exact npm packages
   - Docker: image names and versions to pull
   - Kubernetes: which manifest files to write (Deployment, Service, etc.)

4. **What will each section output?** Describe the expected output structure.

Write the plan as a numbered list before proceeding.

---

## PHASE 3: Create Directory and Set Up Environment

**Step 1: Create the directory**
```bash
mkdir -p $0
```

**Step 2: Set up the runtime environment** (based on technology chosen in Phase 2)

**If Python:**
```bash
cd $0 && uv venv .venv --python 3.12 && source .venv/bin/activate && uv pip install [packages]
```
Stop if install fails — report exact error.

**If TypeScript/Node.js:**
```bash
cd $0 && npm init -y && npm install [packages]
```
For Next.js apps: `npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` then `npx shadcn@latest init`.

**If shell-only:** Confirm required CLI tools are available, then note install commands for BOTH platforms in the lab:
```bash
which curl nc openssl [whatever tools the lab uses]
```
In the lab Setup section, always show both:
```
**macOS:**
brew install [tool]

**Linux / WSL:**
sudo apt install [tool]
```
Never show only one platform. Python (uv) and npm are cross-platform — no split needed for those.

**If Docker/Kubernetes:**
```bash
docker --version && kubectl version --client  # verify tools present
```
Pull any required images early: `docker pull [image]:[tag]`

**Step 3: Write each demo file**

Use the `Write` tool. All demo files must follow these rules regardless of language:

**Section structure (adapt syntax to the language):**
- Shell: `echo ""; echo "═══════════════════════════════════"; echo "SECTION A — [description]"; echo "═══════════════════════════════════"`
- Python: `print(); print("=" * 70); print("SECTION A — [description]"); print("=" * 70)`
- For config files (Dockerfile, YAML): use comment sections `# ─── Section A: [description] ───`

**Every demo file has:**
- A header comment explaining what it is and how to run it
- At least 3 sections (ideally 4)
- Labeled output — students must know what each line means
- The last section is always a practical contrast/demonstration (e.g., with-vs-without, before-vs-after, break-and-fix)

**No warnings or errors on run.** Fix the underlying cause — never suppress.

**Python-specific rules (only when using Python):**
- `datetime.now(timezone.utc)` not `datetime.utcnow()` (deprecated in 3.12)
- bcrypt inputs must be bytes: `b"password"` not `"password"`
- PyJWT HS256 key must be exactly 32 bytes
- Never `warnings.filterwarnings("ignore")` — fix the cause

**Shell script rules:**
- `#!/usr/bin/env bash` header
- Every command has a comment above it explaining what it does
- Use `set -e` only when you want to stop on errors; otherwise handle errors explicitly

---

## PHASE 4: Run and Test ALL Demo Files — Capture Exact Output

**This phase is critical.** The script and lab must use actual tested output, not invented output. Complete this phase entirely before writing any `.md` files.

**Run command by tech:**

- Shell script: `bash [filename].sh 2>&1`
- Python: `cd $0 && source .venv/bin/activate && python3.12 [filename].py 2>&1`
- TypeScript/Node: `cd $0 && node [filename].js 2>&1` or `npx ts-node [filename].ts 2>&1`
- Docker: `docker run [image] [command] 2>&1`
- Multi-process (server + client): start server in background (`&`), run client, kill server

**If exit code is not 0:** Stop. Read the error. Fix with `Edit`. Re-run. Never proceed until clean.

**Store captured stdout as `OUTPUT_[filename]`.** This is the ground truth for Phases 6 and 7. Never paraphrase — paste verbatim.

**Note on random/variable values:** Some output changes each run (hashes, tokens, ports, timestamps). In OUTPUT blocks: paste the actual captured output, add a note: `*(Your [value] will look different — structure is the same.)*`

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

**Output (Section A):**

```
[EXACT OUTPUT FROM PHASE 4 — paste verbatim]
```

[Explanation of what each labeled line means.]

**Code walkthrough reference (include when lesson code exists):**

Do NOT include inline code walkthroughs in the student lab. Instead, add a short
note directing the student to read the code or refer to the code walkthrough video:

> "Before running this section, open `[filename]` in VS Code and read through it.
> The code walkthrough video covers each section in detail."

This applies to Python, TypeScript, AND bash demo scripts that ARE the lesson.
**Exempt only when** the file is infrastructure run as a black box (provided server,
Docker image, startup script), or code reused unchanged from a prior lab.

### Interactivity requirement (non-negotiable):

Every Part must include at least TWO interactive elements beyond just "run this command":

- **Prediction prompt** — before showing output, ask the student to predict something:
  > "Before running, predict: what status code will this return? Write it down."
  Follow with a `<details><summary>Answer</summary>` collapsible.

- **Fill-in-the-blank** — show a command or code snippet with `_____` where the student
  must supply a flag, value, or keyword. Collapsible solution reveals the answer:
  ```bash
  curl -s _____ /dev/null -w "Status: %{http_code}\n" http://example.com/
  ```
  > What flag goes in the blank? `<details><summary>Answer</summary>-o</details>`

- **Short-answer question** — ask a conceptual question they must answer before revealing:
  > "What does the blank line between headers and body signal to the server?"
  `<details><summary>Answer</summary>The server stops reading headers and waits for the body.</details>`

- **"Try it" variation** — after a working example, ask them to modify it for a slightly different goal before giving the solution.

Goal: students must actively engage at each step, not passively read and run.

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

## PHASE 7: Write Instructor Script(s)

### When lesson code exists (Python, TypeScript, OR bash demo scripts students need to understand):

Write TWO script files:

**File 1: `$0/[LAB_ID]-code-walkthrough.md`**
This is a separate instructor script recorded as its own video segment — before the lab video.
It serves TWO purposes:
1. **Conceptual foundation** — explain the *why* before showing the code. This is where the deep "why does bcrypt need to be slow?", "why is the JWT payload not encrypted?", "why does HTTP need the blank line?" explanations live. The regular lab script focuses on output; the walkthrough is where concepts are taught.
2. **Code reading** — walk through the lesson code file(s) section by section so students understand what they're about to run.

Opening files: use `code [filename]` to open in VS Code. Do NOT use `cat` or `less`. The instructor narrates from the open editor view.

Structure:
```
# Code Walkthrough Script — Lab $0: [TOPIC_TITLE]

**Format:** Screencast — VS Code editor
**Estimated recording time:** ~N min

---

## INTRO

**SPEAK**
> "Before we run the lab, I want to cover two things: the concept behind what
> we're about to do, and then the code that implements it. Understanding both
> means you can reason about what's happening — not just run commands."

---

## Concept: [The core idea]

**SPEAK**
> "[Conceptual explanation — the problem this solves, the mental model students
> need. No code yet. 2-4 minutes of pure concept. This is the deepest explanation
> of the concept in the whole course — the lab script will reference it but not
> re-explain it.]"

---

## [filename] — Section A: [description]

**TYPE**
```bash
code [filename]
```
(opens the file in VS Code — instructor narrates from the editor)

**EXPLAIN**
> "[Line-by-line narration. What does this function do? Why bytes not strings?
> Why this constant? Connect code decisions back to the concept just explained.]"

[Repeat for each section / key function in the file]

---

[Repeat for each lesson code file]

## Recording notes

- [Tips for pacing, scrolling, font size]
- [Remind: conceptual section first, code second]
```

**File 2: `$0/[LAB_ID]-script.md`**
The regular lab script — runs the demos, walks through output, covers exercises.
This is the second video, recorded AFTER the code walkthrough video.

**Target length for each:** code-walkthrough.md 200–400 lines; script.md 500–700 lines.

### When NO lesson code exists (shell-only labs):

Write only `$0/[LAB_ID]-script.md`. No code walkthrough file needed.

---

### `[LAB_ID]-script.md` — non-negotiable beat format:

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
> "[Walk through the output. Reference specific labeled fields. Connect to what
students just saw in the code: 'that line printed the value of X that we saw
defined on line N'.]"

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
Identify the tech stack from file extensions. For each demo file:
- `.sh`: `bash <file> 2>&1; echo "Exit: $?"` — check exits 0, has bash header, every command commented, output labeled
- `.py`: `cd $0 && source .venv/bin/activate && python3.12 <file> 2>&1; echo "Exit: $?"` — check exits 0, zero warnings, shebang+docstring, section banners, no `datetime.utcnow()`, bcrypt bytes, PyJWT 32-byte key, every print labeled
- `.ts`/`.js`: `cd $0 && npx ts-node <file> 2>&1; echo "Exit: $?"` — check exits 0, no unhandled errors, labeled console output, section banners
- `Dockerfile`: `docker build -t test-lab . 2>&1` — check build succeeds
- Kubernetes YAML: `kubectl apply -f <file> --dry-run=client 2>&1` — check no validation errors
- All files: section structure present (3–4 sections), last section is a practical demonstration

**Component 2: Script ↔ Lab Alignment**
Read both `$0/$0-lab.md` and `$0/$0-script.md`.
- Every Part in lab has a section in script
- Every exercise in lab has a TYPE + OUTPUT beat in script with the solution
- Every output shown to students in lab has a corresponding OUTPUT beat in script
- Every SPEAK beat in script covers a concept introduced in the lab
- Every beat in script is labeled SPEAK/TYPE/OUTPUT/EXPLAIN — no unlabeled prose
- For labs with lesson code (Python/TypeScript files students need to understand): a `{id}-code-walkthrough.md` exists as a separate instructor script with SPEAK/TYPE/EXPLAIN beats reading through the code; the student lab has a short note referencing it (NOT inline code blocks). Exempt: infrastructure files (provided servers, Docker images, reused prior-lab code), shell-only labs.

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
