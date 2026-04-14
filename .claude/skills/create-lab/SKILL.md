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

**Before writing any deliverable:** read `.claude/skills/shared/STANDARDS.md`, `.claude/skills/shared/lab-template.md`, and `.claude/skills/shared/script-template.md`. These are authoritative — follow them exactly. For any demo files you write, also read the relevant `.claude/skills/shared/tech-standards/<language>.md` file(s) for each language you use.

## Arguments

- `$0` — Lab section ID (e.g., "5.7", "6.1"). Required.

## Paths

- `REPO_ROOT` = current working directory (where `SYLLABUS.md` lives)
- `LAB_ID` = `$0`
- `LAB_DIR` = `$0/` relative to repo root

---

## PHASE 0: Preflight

**Step 1: Check if lab already exists**

Use Glob to check if `LAB_DIR` contains any `.md` files:
```
pattern: $0/*.md
```
If any `.md` files are found, stop immediately:
> "Lab `$0` already exists with existing `.md` files. Delete `$0/` first or choose a different section ID."

**Step 2: Read the syllabus**

Read `SYLLABUS.md`. Find the entry for section `$0`. Extract:
- `TOPIC_TITLE` — the topic name (e.g., "Rate Limiting and Throttling")
- `LEARNING_OBJECTIVES` — the bullet points listed under this section
- `PREREQUISITES` — any prerequisite labs mentioned

If the section is not found, stop and ask the user for the topic title and learning objectives.

**Step 3: Proceed**

Print: `"Creating Lab $0: [TOPIC_TITLE] — starting research phase..."`

---

## PHASE 1: Research

Spawn an Agent to research the topic. This keeps research context (web pages, search results) out of the main context window.

Spawn with:
- `description`: `"Research for Lab $0: [TOPIC_TITLE]"`
- `subagent_type`: `"general-purpose"`
- `prompt`:

---
**[AGENT PROMPT — substitute actual values for $0, TOPIC_TITLE, LEARNING_OBJECTIVES]**

You are researching "[TOPIC_TITLE]" for Lab $0 of the "Anyone Can Code" beginner programming course. The audience is non-technical adults learning to code for the first time — they know basic programming but nothing about [TOPIC_TITLE].

Learning objectives:
[LEARNING_OBJECTIVES]

Use WebSearch and WebFetch to research every concept. For EACH concept, produce:

**1. First-principles explanation**
What problem does this solve? Explain the concept before naming it. No jargon until the idea is established. Write for a smart adult with no CS background.

**2. Internal mechanics**
The actual algorithm, protocol steps, or data flow at the byte/function level. Not just "what it does" — "how it works."

**3. Tools and libraries**
Research ALL viable implementation options:
- Shell/CLI tools (commands, flags, platform notes)
- Python libraries (PyPI name, version, install, key API)
- TypeScript/Node packages (npm name, version, key API)
- Any other relevant tools
- Which tool gives the most direct, least-abstracted view of this concept?

**4. Constraints and gotchas**
- Platform differences (macOS vs. Linux)
- Input type requirements
- Version compatibility issues
- Common student errors

**5. Sources** (minimum 3 per concept)
Official documentation, RFC/spec if applicable, package page, well-known tutorial.

**6. Demo design**
Suggest 3–4 sections for a demo file that shows intermediate values so students see the internals, not just the final result. What contrast or comparison would be most instructive?

After all concepts, produce a **Lab Design Rationale**:
- What is the right tech stack for this lab and why?
- Local demo vs. real external service?
- Concepts demonstrable with stdlib/shell only?
- Minimum viable demo for each key insight?

Return the full research dump in structured markdown. Do not truncate.

```
# Research Dump: Lab $0 — [TOPIC_TITLE]

## Concept 1: [Name]
### First-Principles Explanation
### Internal Mechanics
### Tools and Libraries
### Constraints and Gotchas
### Suggested Demo Sections
### Sources

## Concept 2: [Name]
[same structure]

## Lab Design Rationale
```
---
**[END AGENT PROMPT]**

Store the full return value as `RESEARCH_DUMP`. Do not proceed until the agent completes.

---

## PHASE 2: Scaffold

Using `RESEARCH_DUMP` and `LEARNING_OBJECTIVES`, do all of the following in sequence:

**Step 1: Choose the technology stack**

Based on the topic and research, choose the most direct, least-abstracted tool. Use judgment from the research — there is no hardcoded decision table. Read `.claude/skills/shared/tech-standards/<language>.md` for each language you plan to use.

Document your decision: "This lab uses [TECH STACK] because [REASON]."

**Step 2: Plan the demo files**

Name them descriptively (e.g., `{concept}_demo.py`, `{concept}_flow.sh`). Plan 3–4 sections per file and what each section will output.

**Step 3: Create the directory**

```bash
mkdir -p $0
```

**Step 4: Set up the runtime environment**

- **Python:** `cd $0 && uv venv .venv --python 3.12 && source .venv/bin/activate && uv pip install [packages]`
- **TypeScript/Node:** `cd $0 && npm init -y && npm install [packages]`
- **Next.js:** `npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` then `npx shadcn@latest init`
- **Shell-only:** verify required CLI tools are installed (`which curl nc openssl` etc.)
- **Docker/Kubernetes:** `docker --version && kubectl version --client`; pull required images early

Stop if any install fails — report the exact error.

**Step 5: Write the demo files**

Write each demo file using the `Write` tool. Follow `.claude/skills/shared/tech-standards/<language>.md` for all language-specific rules (headers, section banners, output labeling, known gotchas).

Universal rules (all languages):
- Header comment explaining what the file is and how to run it
- 3–4 sections with clear section banners
- Every output line is labeled
- Last section is a practical contrast or demonstration
- No warnings or errors on run — fix the root cause

---

## PHASE 3: Test All Demo Files — Capture Exact Output

**This phase is critical.** Scripts and labs use actual tested output. Never proceed to Phase 4 until all demo files pass.

Run each file:
- Shell: `bash [filename].sh 2>&1`
- Python: `cd $0 && source .venv/bin/activate && python3.12 [filename].py 2>&1`
- TypeScript: `cd $0 && npx ts-node [filename].ts 2>&1`
- Docker: `docker run [image] [command] 2>&1`
- Multi-process: start server in background (`&`), run client, kill server

**If exit code is not 0:** stop, read the error, fix with `Edit`, re-run. Never proceed with a failing file.

**Store each file's complete stdout as `OUTPUT_[filename]`.** This is the ground truth for Phases 4–5. Paste verbatim into all OUTPUT blocks — never paraphrase.

For variable output (hashes, tokens, timestamps): paste the actual captured output, then note: `*(Your [value] will look different — structure is the same.)*`

---

## PHASE 4: Write Research Report

Write `$0/[LAB_ID]-report.md`. Target: 200–400 lines.

```markdown
# Research Report: Lab $0 — [TOPIC_TITLE]

## Overview

[2–3 paragraphs: what the lab covers and why these mechanisms matter. No jargon without definition.]

---

## 1. [Concept One Name]

### Background

[First-principles explanation. Start with the problem being solved.]

### How it works

[Internal mechanics. Tables and ASCII diagrams are fine.]

### Implementation: [tool or library name]

[Key commands or function signatures, and one short usage example.]

**Sources:**
- [Title](URL) — [one-line description]
- [Title](URL)
- [Title](URL)
(minimum 3 per concept — all URLs from RESEARCH_DUMP, never invented)

---

## 2. [Concept Two Name]

[same structure]

---

## Lab Design Decisions

### [Key decision]
[Reasoning for beginner audience.]

### [Other constraint or tradeoff]
[Explanation.]
```

---

## PHASE 5: Write Student Lab

Write `$0/[LAB_ID]-lab.md`. Target: 400–600 lines. Shorter is better.

Follow `.claude/skills/shared/lab-template.md` exactly for section order, heading names, and formatting rules. Follow `STANDARDS.md` for all pedagogical requirements.

Key reminders:
- First principles before jargon — start with the problem, not the solution name
- Students must type in every Part (not just run a script)
- Every Part has a conceptual question testing WHY (see `.claude/skills/shared/STANDARDS.md` for good/bad examples)
- Platform splits for any CLI tool installs
- All output blocks use verbatim Phase 3 captures

---

## PHASE 6: Write Instructor Script(s)

Follow `.claude/skills/shared/script-template.md` exactly for beat format, section structure, and file naming.

**When lesson code exists** (demo files students need to understand, not just run):
Write TWO files:
1. `$0/[LAB_ID]-code-walkthrough.md` — VS Code walkthrough recorded before the lab video
2. `$0/[LAB_ID]-script.md` — terminal screencast recorded after

**When no lesson code exists** (shell-only, infrastructure-only):
Write only `$0/[LAB_ID]-script.md`.

All OUTPUT blocks use verbatim Phase 3 captures. Never write invented output.

---

## PHASE 7: Quality Review

Spawn an Agent to run the review independently — fresh read of all files, no memory of how they were written.

Spawn with:
- `description`: `"Quality review for Lab $0: [TOPIC_TITLE]"`
- `subagent_type`: `"general-purpose"`
- `prompt`:

---
**[AGENT PROMPT — substitute $0]**

You are reviewing Lab $0 of the "Anyone Can Code" course. Read all files in `$0/` fresh.

1. Read `STANDARDS.md`, `lab-template.md`, `script-template.md`, and all relevant `.claude/skills/shared/tech-standards/<lang>.md` files from the repo root.
2. Read and follow the full `/review-lab` skill at `.claude/skills/review-lab/SKILL.md`.
3. Apply it to lab `$0`.
4. Return a structured PASS/FAIL report by component with specific fix instructions.
5. If all components pass, write `$0/README.md`.
---
**[END AGENT PROMPT]**

**If the review returns any FAIL items:** fix them with `Edit`, re-verify the specific check, then proceed.

---

## PHASE 8: Commit and Push

```bash
git remote -v
```
Expected remote: `origin → git@github.com:Beehive-Advisors/anyone-can-code.git`
If wrong: stop and report.

```bash
git add $0/
git status
```

If `.venv` appears in staged files: `git rm -r --cached $0/.venv`

```bash
git commit -m "Add Lab $0: [TOPIC_TITLE]"
git push origin main
```

If push is rejected (non-fast-forward): report the error and tell the user to `git pull --rebase origin main`. Do not force-push.

Print the full push output. On success: `"Lab $0 committed and pushed. Done."`

---

## Error Reference

| Situation | Action |
|-----------|--------|
| LAB_DIR has existing `.md` files | Stop — warn user |
| Section not in SYLLABUS.md | Stop — ask user |
| Install fails | Stop — report exact error |
| Demo file exits non-0 | Fix with Edit, re-run |
| Review FAIL items | Fix, re-verify, proceed |
| Git push rejected | Report, tell user to `git pull --rebase` |
