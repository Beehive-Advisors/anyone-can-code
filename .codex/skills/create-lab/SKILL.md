---
name: create-lab
description: |
  Create a complete lab for the "Anyone Can Code" Udemy course. Fully autonomous:
  reads SYLLABUS.md, researches the topic, writes demo files, tests them, writes
  the student lab, instructor script, and research report, runs a quality review,
  and commits + pushes to GitHub. Use when user says "create lab", "build lab",
  "make lab", "new lab", or gives a section ID like "5.7" and asks to build it.
metadata:
  short-description: Create a full course lab from a section id
---

# /create-lab — Full Lab Creation

You are building a complete lab for the "Anyone Can Code" Udemy course. This is a fully autonomous workflow — run all phases to completion without pausing for user confirmation unless something breaks.

**Default to direct-terminal typing.** Most labs do not need demo files (`.sh` / `.py` / `.ts`) — students learn more by typing individual commands themselves than by running pre-written scripts. Only produce demo files when the lab requires scaffolding (see "The scaffolding test" in `STANDARDS.md`). The research phase is responsible for making this call explicitly; every subsequent phase branches on it.

**Before writing any deliverable:** read `.codex/skills/.anyone-can-code-common/STANDARDS.md`, `.codex/skills/.anyone-can-code-common/lab-template.md`, and `.codex/skills/.anyone-can-code-common/script-template.md`. These are authoritative — follow them exactly. For any demo files you write (only when scaffolding is required), also read the relevant `.codex/skills/.anyone-can-code-common/tech-standards/<language>.md` file(s) for each language you use.

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

**Step 2: Read the syllabus and coverage registry**

Read `SYLLABUS.md`. Find the entry for section `$0`. Extract:
- `TOPIC_TITLE` — the topic name (e.g., "Rate Limiting and Throttling")
- `LEARNING_OBJECTIVES` — the bullet points listed under this section
- `PREREQUISITES` — any prerequisite labs mentioned

If the section is not found, stop and ask the user for the topic title and learning objectives.

Read `LAB_COVERAGE.md` if it exists. Store the full contents as `EXISTING_COVERAGE`. If the file does not exist, set `EXISTING_COVERAGE` to `""` (empty string).

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
**[AGENT PROMPT — substitute actual values for $0, TOPIC_TITLE, LEARNING_OBJECTIVES, EXISTING_COVERAGE]**

You are researching "[TOPIC_TITLE]" for Lab $0 of the "Anyone Can Code" beginner programming course. The audience is non-technical adults learning to code for the first time — they know basic programming but nothing about [TOPIC_TITLE].

Learning objectives:
[LEARNING_OBJECTIVES]

## Already-covered concepts (do NOT re-teach these)

The following concepts, tools, and exercises have been covered in prior labs. Your research should design this lab's content to be distinct — do not repeat these as primary teaching points. Incidental reinforcement is fine; full re-explanation is not.

[EXISTING_COVERAGE — paste full LAB_COVERAGE.md contents here, or "None — this is the first lab." if EXISTING_COVERAGE is empty]

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

After all concepts, produce a **Scaffolding Decision** and a **Lab Design Rationale**.

**Scaffolding Decision** — apply the scaffolding test from `STANDARDS.md`:

A lab requires scaffolding only when the demo cannot reasonably be typed command-by-command in the terminal — multi-step programs with loops/functions/state, multi-file setups (Dockerfile, class hierarchy), or single logical units exceeding ~5 lines of code.

Default to no scaffolding. Produce:
- **Required: Yes / No** (one word)
- **Reasoning**: 2–4 sentences applying the test to this specific lab
- **If Yes**: list the demo files to write and state, per file, why it cannot be typed live
- **If No**: sketch the sequence of terminal commands that replaces scaffolding in each Part

**Lab Design Rationale** — then cover:
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

## Scaffolding Decision
**Required:** Yes / No
**Reasoning:** ...
**If Yes — demo files:** ...
**If No — command sequence per Part:** ...

## Lab Design Rationale
```
---
**[END AGENT PROMPT]**

Store the full return value as `RESEARCH_DUMP`. Do not proceed until the agent completes.

---

## PHASE 2: Scaffold

**Step 0: Read the scaffolding decision**

Parse the `## Scaffolding Decision` section from `RESEARCH_DUMP`. Store as `SCAFFOLDING_REQUIRED` (boolean).

- **If `SCAFFOLDING_REQUIRED` is No:** this lab is direct-typing only. Create the directory (Step 3 below) but skip Steps 1, 2, 4, 5 entirely — there are no demo files to write. Extract the per-Part command sequence from the research dump's "If No — command sequence per Part" list and store as `COMMAND_PLAN`. Proceed to Phase 3.
- **If `SCAFFOLDING_REQUIRED` is Yes:** run Steps 1–5 below to write the demo files.

**Step 1: Choose the technology stack** (scaffolded labs only)

Based on the topic and research, choose the most direct, least-abstracted tool. Use judgment from the research — there is no hardcoded decision table. Read `.codex/skills/.anyone-can-code-common/tech-standards/<language>.md` for each language you plan to use.

Document your decision: "This lab uses [TECH STACK] because [REASON]."

**Step 2: Plan the demo files** (scaffolded labs only)

Name them descriptively (e.g., `{concept}_demo.py`, `{concept}_flow.sh`). Plan 3–4 sections per file and what each section will output.

**Step 3: Create the directory** (always)

```bash
mkdir -p $0
```

**Step 4: Set up the runtime environment** (scaffolded labs only)

- **Python:** `cd $0 && uv venv .venv --python 3.12 && source .venv/bin/activate && uv pip install [packages]`
- **TypeScript/Node:** `cd $0 && npm init -y && npm install [packages]`
- **Next.js:** `npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` then `npx shadcn@latest init`
- **Shell-only:** verify required CLI tools are installed (`which curl nc openssl` etc.)
- **Docker/Kubernetes:** `docker --version && kubectl version --client`; pull required images early

Stop if any install fails — report the exact error.

For **direct-typing labs**, the only environment work is verifying that the CLI tools the student will type are installed — no `.venv`, no `npm init`, no `pip install`.

**Step 5: Write the demo files** (scaffolded labs only)

Write each demo file using the `Write` tool. Follow `.codex/skills/.anyone-can-code-common/tech-standards/<language>.md` for all language-specific rules (headers, section banners, output labeling, known gotchas).

Universal rules (all languages):
- Header comment explaining what the file is and how to run it
- 3–4 sections with clear section banners
- Every output line is labeled
- Last section is a practical contrast or demonstration
- No warnings or errors on run — fix the root cause

---

## PHASE 3: Test the Demos — Capture Exact Output

**This phase is critical.** Scripts and labs use actual tested output. Never proceed to Phase 4 until all tests pass.

### Linux Testing Environment

Many labs use Linux-specific commands (`lscpu`, `lsmem`, `lsblk`, `xxd`, `/proc/*`, `/sys/*`, etc.). These do not exist on macOS. You must capture output from a real Linux host — never invent it, never approximate from macOS equivalents.

**Preferred: Kubernetes pod (real x86_64 Linux hardware)**

The cluster node `carlo` runs k0s on bare-metal x86_64 hardware. Output from this pod matches what students see on their own Linux VMs or WSL instances.

```bash
# 1. Create a clean Ubuntu pod
kubectl run lab-capture --image=ubuntu:22.04 --restart=Never -- sleep 600
kubectl wait --for=condition=Ready pod/lab-capture --timeout=60s

# 2. Install tools the lab needs (adjust package list per lab)
kubectl exec lab-capture -- bash -c "apt-get update -qq && apt-get install -y -qq util-linux xxd python3"

# 3. Run each command and capture output
kubectl exec lab-capture -- bash -c "[command]"

# 4. Clean up when all output is captured
kubectl delete pod lab-capture
```

**Fallback: Docker (only if cluster is unavailable)**

```bash
docker run --rm ubuntu:22.04 bash -c "apt-get update -qq && apt-get install -y -qq util-linux xxd python3 2>/dev/null && [command]"
```

Note: Docker on macOS runs in a Linux VM, not bare metal. `lsmem` and `lsblk` may return reduced output inside containers because sysfs memory/block topology is not fully exposed. Always prefer the pod.

**macOS-native commands** (`sysctl`, `diskutil`, `vm_stat`) run directly in the local shell without a pod.

---

Two modes, per `SCAFFOLDING_REQUIRED`:

**Scaffolded labs — run each demo file:**
- Shell: `bash [filename].sh 2>&1`
- Python: `cd $0 && source .venv/bin/activate && python3.12 [filename].py 2>&1`
- TypeScript: `cd $0 && npx ts-node [filename].ts 2>&1`
- Docker: `docker run [image] [command] 2>&1`
- Multi-process: start server in background (`&`), run client, kill server

Store each file's complete stdout as `OUTPUT_[filename]`.

**Direct-typing labs — run each command from `COMMAND_PLAN` individually:**

For each Part in the plan, execute every command in sequence, capturing the output of each. Store each pair as `OUTPUT_partN_cmdM`. These become the verbatim OUTPUT blocks in the lab file, one per discrete student-typed command. Typical shapes:
- `sysctl -n hw.memsize` → one-line number
- `xxd hello.txt` → a few lines
- `python3.12 -c "print(ord('H'))"` → one-line result

Do NOT collapse multiple commands into one wrapper script — the point of this lab's design is that the student types each command individually. Capture each output independently.

**If exit code is not 0 (either mode):** stop, read the error, fix the command or file with `Edit`, re-run. Never proceed with a failing test.

Paste each captured output verbatim into all lab/script OUTPUT blocks — never paraphrase. For variable output (hashes, tokens, timestamps): paste the actual captured output, then note: `*(Your [value] will look different — structure is the same.)*`

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

Follow `.codex/skills/.anyone-can-code-common/lab-template.md` exactly for section order, heading names, and formatting rules. Follow `STANDARDS.md` for all pedagogical requirements.

Key reminders:
- First principles before jargon — start with the problem, not the solution name
- Students must type commands directly in the terminal in every Part
  - **Direct-typing labs:** each Part's "Run the demo" section is 2–4 discrete TYPE+OUTPUT command pairs the student types individually (no `bash demo.sh` wrapper)
  - **Scaffolded labs:** `bash demo.sh` / `python3.12 demo.py` plus at least one student-typed command per Part
- Every Part has a conceptual question testing WHY (see `.codex/skills/.anyone-can-code-common/STANDARDS.md` for good/bad examples)
- Platform splits for any CLI tool installs
- All output blocks use verbatim Phase 3 captures (by-file for scaffolded labs, by-command for direct-typing labs)

---

## PHASE 6: Write Instructor Script(s)

Follow `.codex/skills/.anyone-can-code-common/script-template.md` exactly for beat format, section structure, and file naming.

The decision is purely the scaffolding test:

- **If `SCAFFOLDING_REQUIRED` is Yes:** write both files.
  1. `$0/[LAB_ID]-code-walkthrough.md` — VS Code walkthrough recorded before the lab video
  2. `$0/[LAB_ID]-script.md` — terminal screencast recorded after

- **If `SCAFFOLDING_REQUIRED` is No:** write only `$0/[LAB_ID]-script.md`. **Do NOT write a code walkthrough** — there is no code to walk through; the terminal script is the complete instructor asset.

All OUTPUT blocks use verbatim Phase 3 captures. Never write invented output. In direct-typing labs, each captured `OUTPUT_partN_cmdM` maps to one TYPE+OUTPUT+EXPLAIN beat in the terminal script (not a single bulk output for the whole Part).

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

1. Read `STANDARDS.md`, `lab-template.md`, `script-template.md`, and all relevant `.codex/skills/.anyone-can-code-common/tech-standards/<lang>.md` files from the repo root.
2. Read and follow the full `/review-lab` skill at `.codex/skills/review-lab/SKILL.md`.
3. Apply it to lab `$0`.
4. Return a structured PASS/FAIL report by component with specific fix instructions.
5. If all components pass, write `$0/README.md`.
---
**[END AGENT PROMPT]**

**If the review returns any FAIL items:** fix them with `Edit`, re-verify the specific check, then proceed.

---

## PHASE 7.5: Update Lab Coverage Registry

Read `$0/[LAB_ID]-lab.md` and `$0/[LAB_ID]-report.md`. Extract:
- **Concepts Taught** — the core concepts each Part introduced (from the `### What is X?` sections and report)
- **Tools and Commands Demonstrated** — every CLI flag, function, or API method shown in the demo files and exercises
- **External Services Used** — any external hosts or services the demo files connect to (with protocol and port if non-standard)
- **Student Exercises** — one-line summary of each exercise (from `### Exercise` sections)

Then append to `LAB_COVERAGE.md` (or create it with the header if it doesn't exist):

```markdown
## Lab $0 — [TOPIC_TITLE]

**Status:** Draft
**Completed:** [today's date]

### Concepts Taught
- [concept 1]
- [concept 2]
...

### Tools and Commands Demonstrated
- `[command or flag]` — [what it does]
...

### External Services Used
- `[host]` ([protocol, port]) — [purpose]
...

### Student Exercises
1. [one-line description]
2. [one-line description]
...
```

Use the Write tool to append to `LAB_COVERAGE.md`. If the file does not exist, create it with this header first:

```markdown
# Lab Coverage Registry

This file tracks what each completed lab taught. The `create-lab` skill reads this before researching a new lab to avoid re-teaching covered concepts. The `review-lab` skill reads it to check for course overlap.

**To approve a lab:** change its Status in `SYLLABUS.md` from `Draft` to `Approved`.

---
```

---

## PHASE 8: Commit and Push

```bash
git remote -v
```
Expected remote: `origin → git@github.com:Beehive-Advisors/anyone-can-code.git`
If wrong: stop and report.

**Detect the current branch** — the lab may be created in a worktree on a feature branch, not on `main`:

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"
```

Update `SYLLABUS.md` to set the Status for this lab to `Draft`:

```bash
python3.12 - <<'PYEOF'
import sys
LAB_ID = '$0'
path = 'SYLLABUS.md'
lines = open(path).read().splitlines()
out = []
changed = False
for line in lines:
    cols = [c.strip() for c in line.split('|')]
    # cols[0] = '', cols[1] = Section, cols[2] = ID, cols[3] = Lecture Name, cols[4] = Format, cols[5] = Status, cols[6] = ''
    if len(cols) >= 6 and cols[2] == LAB_ID and cols[4] == 'Lab' and cols[5] == '':
        cols[5] = 'Draft'
        line = '| ' + ' | '.join(cols[1:6]) + ' |'
        changed = True
    out.append(line)
if not changed:
    print('WARNING: Could not find empty-Status Lab row for', LAB_ID, '— update SYLLABUS.md manually')
else:
    print('SYLLABUS.md updated: Lab', LAB_ID, 'Status → Draft')
open(path, 'w').write('\n'.join(out) + '\n')
PYEOF
```

```bash
git add $0/
git add LAB_COVERAGE.md SYLLABUS.md
git status
```

If `.venv` appears in staged files: `git rm -r --cached $0/.venv`

```bash
git commit -m "Add Lab $0: [TOPIC_TITLE]"
git push origin $CURRENT_BRANCH
```

If push is rejected (non-fast-forward): report the error and tell the user to `git pull --rebase origin $CURRENT_BRANCH`. Do not force-push.

Print the full push output. On success: `"Lab $0 committed and pushed to $CURRENT_BRANCH. Done."`

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
