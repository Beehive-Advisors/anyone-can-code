---
name: review-lab
description: |
  Review a completed "Anyone Can Code" lab against all quality standards. Checks demo
  code quality, script-lab alignment, course overlap, lab structure and necessity, and
  report quality. Creates README.md for the lab folder. Returns a structured PASS/FAIL
  report by component with specific fix instructions. Invoked by /create-lab or
  standalone. Use when user says "review lab", "check lab", "qa lab", or provides a
  section ID and asks for review.
user_invocable: true
argument-hint: <section-id>
allowed-tools: Read Glob Bash Write
---

# /review-lab — Lab Quality Review

You are the quality review phase of the "Anyone Can Code" lab pipeline. Read all files fresh — no assumptions about what they contain.

**Before starting:** Read `.claude/skills/shared/STANDARDS.md`, `.claude/skills/shared/lab-template.md`, and `.claude/skills/shared/script-template.md`. Detect the file extensions present in `$0/` and read the relevant `.claude/skills/shared/tech-standards/<lang>.md` files. These are the complete criteria you will apply.

## Arguments

- `$0` — Lab section ID (e.g., "5.7"). Required.

## Setup

- `LAB_DIR` = `$0/`
- `LAB_PREFIX` = `$0`

Read all files in `LAB_DIR`. If the directory or any required file (`{LAB_PREFIX}-lab.md`, `{LAB_PREFIX}-script.md`, `{LAB_PREFIX}-report.md`) doesn't exist, stop and report what's missing.

---

## Pass 1: Demo Code + Script-Lab Alignment

### 1a. Demo Code Quality

For each demo file, check language-specific rules from the relevant `.claude/skills/shared/tech-standards/*.md` file.

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

Apply all rules from the matching `.claude/skills/shared/tech-standards/<lang>.md` to each file.

### 1b. Script ↔ Lab Alignment

Read both `{LAB_PREFIX}-lab.md` and `{LAB_PREFIX}-script.md`.

- [ ] Every `## Part N` in the lab has a matching `## PART N` section in the script
- [ ] Every exercise in the lab has a TYPE + OUTPUT beat in the script showing the solution
- [ ] Every run-the-demo block in the lab has a corresponding TYPE + OUTPUT + EXPLAIN sequence in the script
- [ ] Every beat in the script is labeled SPEAK / TYPE / OUTPUT / EXPLAIN — no unlabeled prose
- [ ] Script has INTRO, PUTTING IT TOGETHER, OUTRO, and Recording notes sections

**Code walkthrough check:**
For each demo file, determine: is this *lesson code* (students need to understand it) or *infrastructure* (run as a black box)?

For lesson code:
- [ ] `{LAB_PREFIX}-code-walkthrough.md` exists
- [ ] Walkthrough opens files with `code [filename]` (VS Code) — not `cat` or `less`
- [ ] Walkthrough has a conceptual section BEFORE any code sections — every term the code uses is defined before the code section that uses it
- [ ] All EXPLAIN beats have: parenthetical `(lines N–M — description)`, fenced code block in the application language, line-number-specific narration

Exempt: infrastructure run as a black box, code reused unchanged from a prior lab, shell-only labs.

---

## Pass 2: Lab + Report Content Quality

### 2a. Lab Structure and Interactivity

Read `{LAB_PREFIX}-lab.md`.

**Structure checks (follow `.claude/skills/shared/lab-template.md`):**
- [ ] Header has Section, Prerequisites, Time, Files
- [ ] Has `## What you'll build` with numbered concrete outcomes
- [ ] Has `## Setup` with correct stack commands
- [ ] Every `## Part N` has a `### What is X?` intro, run-the-demo block, conceptual question, and `### Exercise`
- [ ] Every exercise has `<details><summary>Solution</summary>` collapsible block
- [ ] Platform splits present for all CLI tool installs
- [ ] Has `## Putting it together`, `## Checklist`, `## Further Reading` (≥3 links)

**First-principles check (spot-check first 5 technical terms):**
For each of the first 5 technical terms introduced, verify it is explained from first principles before it's used as if already known. Flag any term that appears without prior definition.

**Interactivity check (per `.claude/skills/shared/STANDARDS.md`):**
- [ ] Every Part has ≥1 moment where the student types code or a command themselves
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

Use Glob to list all lab directories. For each other lab with an existing `-lab.md`:
- [ ] Flag concepts covered in this lab that are already thoroughly explained elsewhere
- [ ] Flag prerequisites referenced in Setup that don't have a corresponding lab directory

If no other labs exist: "No other labs — overlap check skipped."

---

## Write README.md

After both passes, write `LAB_DIR/README.md`:

```markdown
# Lab $0 — [TOPIC_TITLE]

[1–2 sentence description of what this lab covers and why it matters]

## Prerequisites

[List from lab file]

## Setup

```bash
cd $0
[exact setup commands for this lab's tech stack]
```

## Files

| File | What it does | How to run |
|------|-------------|------------|
| `[filename]` | [description] | `[run command]` |
| `[LAB_PREFIX]-lab.md` | Student lab handout | Open in editor |
| `[LAB_PREFIX]-script.md` | Instructor script | Open in editor |
| `[LAB_PREFIX]-report.md` | Research report | Open in editor |

## Time

~N minutes

## Notes

[Any special requirements, e.g., "Part 3 requires two terminal windows"]
```

---

## Report Format

```
# Review Report: Lab $0

## Pass 1: Demo Code + Alignment     [PASS / FAIL]

### Demo Code
- [PASS] hash_demo.py — exits 0, no warnings, all checks pass
- [FAIL] jwt_demo.py — line 22: datetime.utcnow() → fix: use datetime.now(timezone.utc)

### Script ↔ Lab Alignment
- [PASS] All Parts match
- [FAIL] Exercise in Part 2 has no TYPE beat → add solution TYPE + OUTPUT after "### Exercise — Decode by hand"

## Pass 2: Lab + Report Quality      [PASS / FAIL]

### Lab Structure and Interactivity
- [PASS] All structural checks pass
- [FAIL] Part 1 has no student-typing moment → add a REPL one-liner before the demo
- [CUT]  Lines 180–195 go beyond lab objectives → recommend removing

### Report Quality
- [PASS] All checks pass

### Course Overlap
- [PASS] No overlapping concepts

---
README.md written to $0/README.md
```

End with either "All components PASS. Ready for commit." or "Fix the FAIL items above, then re-run /review-lab $0."
