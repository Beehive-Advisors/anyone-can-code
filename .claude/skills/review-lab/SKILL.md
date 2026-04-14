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

You are the quality review phase of the "Anyone Can Code" lab creation pipeline. You are an independent reviewer — read all files fresh, with no assumptions about what they contain. Your job is to catch every flaw before the lab is committed.

## Arguments

- `$0` — Lab section ID (e.g., "5.7"). Required.

## Setup

Derive paths:
- `LAB_DIR` = `$0/` (relative to repo root, e.g., `5.7/`)
- `LAB_PREFIX` = `$0` (e.g., `5.7`)

Read all files in `LAB_DIR`:
- `{LAB_PREFIX}-report.md`
- `{LAB_PREFIX}-lab.md`
- `{LAB_PREFIX}-script.md`
- All `.py` and `.sh` files in `LAB_DIR`

If the directory or any required file doesn't exist, stop and report what's missing.

---

## Component 1: Demo Code Quality

First, identify what tech stack this lab uses (look at file extensions and content).

**For each `.sh` file:**
```bash
bash <filename> 2>&1; echo "Exit: $?"
```
- [ ] Exits with code 0 (no errors)
- [ ] Has `#!/usr/bin/env bash` header
- [ ] Has section banners with `═══` or `───` separators
- [ ] Every command has a comment above it explaining what it does
- [ ] Output is labeled so students know what each line means

**For each `.py` file:**
```bash
cd LAB_DIR && source .venv/bin/activate && python3.12 <filename> 2>&1; echo "Exit: $?"
```
- [ ] Exits with code 0 (no errors)
- [ ] Zero warnings (no DeprecationWarning, InsecureKeyLengthWarning, etc.)
- [ ] Has shebang `#!/usr/bin/env python3` and a header docstring with `Run: python3.12 <filename>`
- [ ] Section banners present: `# ───` style AND `print("=" * 70)` + section title print
- [ ] No `datetime.utcnow()` — must use `datetime.now(timezone.utc)`
- [ ] If PyJWT: SECRET key is exactly 32 bytes
- [ ] If bcrypt: password inputs are `b"..."` bytes, not `"..."` str
- [ ] Every `print()` line is labeled

**For each `.ts` / `.js` / Node.js file:**
```bash
cd LAB_DIR && npx ts-node <filename> 2>&1; echo "Exit: $?"  # or node <file>.js
```
- [ ] Exits with code 0
- [ ] Zero unhandled errors/warnings
- [ ] Header comment with `Run:` instruction
- [ ] Section banners using `console.log("=".repeat(60))` + section title
- [ ] All console output is labeled

**For Next.js / full-stack apps:**
```bash
cd LAB_DIR && npm run build 2>&1; echo "Exit: $?"
```
- [ ] Build succeeds with no TypeScript errors
- [ ] No ESLint errors
- [ ] Components use shadcn/ui + Tailwind (no inline styles unless intentional)

**For Docker/Kubernetes files:**
- [ ] `Dockerfile` builds: `docker build -t test-lab .`
- [ ] `docker-compose.yaml` or `compose.yaml` starts cleanly: `docker compose up -d`
- [ ] Kubernetes YAML applies: `kubectl apply -f deployment.yaml --dry-run=client`
- [ ] Config files (nginx.conf, etc.) validated if tool is available

**For all files regardless of type:**
- [ ] Every output/log line is labeled — students must know what each line means
- [ ] Section structure is present (3–4 sections per demo file)
- [ ] Last section is a practical contrast/demonstration (not just setup)

---

## Component 2: Script ↔ Lab Alignment

The script IS the solution to the lab. The student follows the lab; the instructor follows the script. They must match exactly.

Read both `{LAB_PREFIX}-lab.md` and `{LAB_PREFIX}-script.md`.

Check:
- [ ] Every `## Part N` in the lab has a corresponding `## PART N` section in the script
- [ ] Every `### What is X?` section in the lab has corresponding **SPEAK** + **EXPLAIN** beats in the script covering the same concept
- [ ] Every `### Run the demo` in the lab (with a `python3.12 <file>` command) has a corresponding **TYPE** + **OUTPUT** + **EXPLAIN** beat sequence in the script
- [ ] Every exercise in the lab (under `### Exercise`) has a corresponding **TYPE** beat in the script showing the solution code, followed by **OUTPUT** showing the result
- [ ] No script section covers something not present in the lab
- [ ] No lab section is missing from the script
- [ ] Script has a `## INTRO` section covering setup (venv + install)
- [ ] Script has `## PUTTING IT TOGETHER` section
- [ ] Script has `## OUTRO` section
- [ ] Script has `## Recording notes` section at the end
- [ ] Every beat in the script is labeled: **SPEAK**, **TYPE**, **OUTPUT**, or **EXPLAIN** — no unlabeled prose

---

## Component 3: Course Overlap

Read all other lab directories in the repo (use Glob: `*/` pattern, exclude `.claude/` and `.venv/`).

For each other lab that exists:
- Read its `{id}-lab.md` (if present)
- Compare concepts, terminology, and demo patterns

Check:
- [ ] Flag any concept covered in this lab that is already thoroughly covered in another lab (report: "Concept X also appears in Lab Y — consider a cross-reference instead of re-explaining")
- [ ] Flag any prerequisite mentioned in `Setup` → Prerequisites that doesn't correspond to an existing lab directory (report: "Prereq 'Lab Z' referenced but directory Z/ does not exist")
- [ ] Flag any terminology inconsistency (e.g., this lab calls it "access token" but another lab calls the same thing "bearer token")

If no other labs exist yet, report: "No other labs to compare against — overlap check skipped."

---

## Component 4: Lab Structure and Necessity Review

Read `{LAB_PREFIX}-lab.md`.

**Structure checks:**
- [ ] Has header with: Section name, Prerequisites, Time estimate, Files
- [ ] Has `## What you'll build` with a numbered list of concrete outcomes
- [ ] Has `## Setup` with the correct setup commands for this lab's tech stack (uv+Python, npm+Node, Docker pull, or brew install for CLI tools)
- [ ] Two-terminal setup note present IF any demo requires two simultaneous processes (server + client)
- [ ] Every `## Part N` has at least one `### Exercise` subsection
- [ ] Every exercise has a `<details><summary>Solution` collapsible block
- [ ] Has `## Putting it together` section
- [ ] Has `## Checklist` section with checkboxes
- [ ] Has `## Further Reading` with at least 3 links

**First-principles check (spot-check first 5 technical terms):**
For the first 5 technical terms introduced (e.g., "hash function", "salt", "JWT", "bearer token", "authorization code"):
- [ ] Each term is explained from first principles BEFORE being used as if already known
- Report any term that appears without prior explanation

**Necessity review (ruthless):**
For every Part, section, and paragraph, ask: is this absolutely required for the stated learning objectives?

Flag any of the following with a specific fix suggestion:
- Paragraphs that repeat what was already said in a prior section
- Exercises that test the same skill as a prior exercise without adding new understanding
- Setup steps that aren't needed for the exercises that follow
- "Background" sections that go deeper than what the exercise actually requires
- Any section that could be cut without the student losing a learning objective

Goal: minimum content for maximum clarity. This lab should be tight.

---

## Component 5: Report Quality

Read `{LAB_PREFIX}-report.md`.

Check:
- [ ] Has `## Overview` section (2–3 paragraphs)
- [ ] Has one `## N. Concept Name` section per major concept covered in the lab
- [ ] Each concept section has: `### Background`, `### How it works`, `### Python library: <name>` subsections
- [ ] Each concept section has a `**Sources:**` block with at least 3 URLs
- [ ] All URLs are real (not invented — spot-check 2 URLs by looking at them critically)
- [ ] Has `## Lab Design Decisions` section explaining key pedagogical choices

---

## Create README.md

After running all checks, write `LAB_DIR/README.md` with this content:

```markdown
# Lab $0 — [TOPIC_TITLE]

[1–2 sentence description of what this lab covers and why it matters]

## Prerequisites

[List prereqs from the lab file]

## Setup

```bash
cd [LAB_ID]
# Python labs:
uv venv .venv --python 3.12 && source .venv/bin/activate && uv pip install [packages]
# Node.js labs:
npm install
# Docker labs:
docker pull [image]:[tag]
# Shell-only labs: brew install [tool] / apt install [tool]
```

## Files

| File | What it does | How to run |
|------|-------------|------------|
| `[filename].py` | [description] | `python3.12 [filename].py` |
| `[filename].sh` | [description] | `bash [filename].sh` |
| `[id]-lab.md` | Student lab handout | Open in editor |
| `[id]-script.md` | Instructor recording script | Open in editor |
| `[id]-report.md` | Research report and citations | Open in editor |

## Time

~[N] minutes

## Notes

[Any special notes, e.g., "Part 3 requires two terminal windows simultaneously"]
```

---

## Report Format

Return the full review report in this exact structure:

```
# Review Report: Lab $0

## Component 1: Demo Code Quality     [PASS / FAIL]
- [PASS] hash_demo.py — exits 0, no warnings, all checks pass
- [FAIL] jwt_demo.py — datetime.utcnow() on line 22 → fix: use datetime.now(timezone.utc)

## Component 2: Script ↔ Lab Alignment   [PASS / FAIL]
- [PASS] All Parts match between lab and script
- [FAIL] Exercise in Part 2 has no TYPE beat in script → add solution TYPE + OUTPUT after "### Exercise — Decode by hand"

## Component 3: Course Overlap           [PASS / FAIL]
- [PASS] No overlapping concepts with other labs
- OR: [FLAG] "Hash function" concept also appears in Lab 4.5 — consider cross-reference

## Component 4: Lab Structure + Necessity   [PASS / FAIL]
- [PASS] All structural checks pass
- [FAIL] Part 1 "Background" section (lines 45–62) repeats setup explanation from intro → cut lines 50–55
- [CUT]  Section "Advanced bcrypt tuning" (lines 180–195) goes beyond lab objectives → recommend removing

## Component 5: Report Quality           [PASS / FAIL]
- [PASS] All checks pass

---
README.md written to $0/README.md
```

If all components pass, end with: "All components PASS. Ready for commit."
If any fail, end with: "Fix the FAIL items above, then re-run /review-lab $0."
