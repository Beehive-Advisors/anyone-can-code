---
name: review-lecture
description: |
  Review a completed "Anyone Can Code" lecture against all quality standards.
  Checks script structure, animation coverage, asset-library usage, beat
  format (SPEAK/SHOW-ANIMATION/EXPLAIN), course overlap, and report quality.
  Creates README.md for the lecture folder. Returns a structured PASS/FAIL
  report by component with specific fix instructions. Invoked by /create-lecture
  or standalone. Use when user says "review lecture", "check lecture", "qa lecture",
  or provides a section ID and asks for review.
user_invocable: true
argument-hint: <section-id>
allowed-tools: Read Glob Bash Write
---

# /review-lecture — Lecture Quality Review

You are the quality review phase of the `/create-lecture` pipeline. Read all files fresh — no assumptions.

**Before starting:** Read `.claude/skills/shared/STANDARDS.md`, `.claude/skills/shared/lecture-template.md`, and `.claude/skills/shared/lecture-script-template.md`.

## Arguments

- `$0` — Lecture section ID (e.g., "1.4"). Required.

## Setup

- `LECTURE_DIR` = `$0/`
- `LECTURE_PREFIX` = `$0`

Required files:
- `{LECTURE_PREFIX}-lecture.md` — the lecture script
- `{LECTURE_PREFIX}-report.md` — research report
- `animations/` — directory with at least one `.py` / `.gif` / `.mp4` triple

If any of these are missing, stop and report what's missing.

---

## Pass 1: Script Structure + Beat Discipline

### 1a. File structure

Read `{LECTURE_PREFIX}-lecture.md`.

- [ ] Header has Section, Prerequisites, Length target, Animations count
- [ ] No `Files:` line (lectures have no external demo files to point at)
- [ ] No `Pick your track` section, no `<details>` blocks, no 🍎 / 🐧 emojis — those are lab conventions
- [ ] Top sections in order: `## Learning Objectives`, `## Opening Hook`, `## Part 1`, ... `## Putting It Together`, `## Outro`, `## Further Reading`
- [ ] At least 3 numbered learning objectives
- [ ] `## Further Reading` has ≥3 links

### 1b. Beat discipline

Every paragraph under a Part heading must sit under one of three labels: **SPEAK**, **SHOW-ANIMATION**, **EXPLAIN**. No unlabeled prose.

- [ ] Every paragraph is under a labeled beat
- [ ] SPEAK blocks are written verbatim (spoken English, no "the instructor explains...")
- [ ] EXPLAIN beats point at specific visual moments ("notice the yellow highlight"), not meta-commentary
- [ ] No lab-script beats present: no **TYPE**, **OUTPUT**, **DEMO**, **RUN**

### 1c. Animation coverage

- [ ] Every `## Part N` has at least one SHOW-ANIMATION beat
- [ ] The animations count in the header matches the actual number of SHOW-ANIMATION beats
- [ ] Every SHOW-ANIMATION uses the final embed form: `[![name](./animations/name.gif)](URL_OR_PATH/name.mp4)`. No leftover `<!-- ANIMATE: ... -->` placeholders.

Flag any violation as FAIL with the exact fix instruction.

---

## Pass 2: Animation Quality and Library Usage

### 2a. File triples

For every animation referenced in the script, the `animations/` folder must contain exactly three files:
- `[name].py` — Manim source (committed)
- `[name].gif` — preview (committed, rendered inline on github.com)
- `[name].mp4` — full video (may be on the pod, NOT committed — check `.gitignore`)

- [ ] Every name referenced in the script has a matching `.py` and `.gif` in `animations/`
- [ ] Every `.py` file in `animations/` is referenced by the script (no orphans)
- [ ] `.gitignore` excludes `$0/animations/*.mp4`

### 2b. Library asset usage

For each `animations/*.py`:

- [ ] Imports at least one name from `anyone_can_code_assets`
- [ ] If the `.py` defines new Manim geometry beyond what library assets provide, that geometry is minimal composition (placement, highlights) — not a re-invention of an existing asset
- [ ] Class name is PascalCase and matches the filename stem (case-normalized)

For each asset name imported, verify the name exists in the library registry:
```bash
python3 ~/src/projects/manim-library/scripts/search_assets.py "[AssetName]" --json
```
Return must contain the asset. If not → FAIL ("import of AssetName which is not in registry.json — add via scaffold_asset.py or remove").

### 2c. Render smoke test

For every `.py` file, verify it renders cleanly:
```bash
cd $0/animations && source ~/src/projects/manim-library/.venv/bin/activate && \
  manim render -ql --media_dir ./media [name].py [ClassName] 2>&1 | tail -5
```

Exit code must be 0. The rendered mp4 size should be > 5KB. If not → FAIL ("animation `name` does not render cleanly — see stderr").

---

## Pass 3: Lecture + Report Content Quality

### 3a. Content quality

- [ ] First 5 technical terms are defined from first principles before used as if known
- [ ] No paragraph repeats content from a prior section
- [ ] No Part could be cut without losing a learning objective (necessity check)
- [ ] Opening Hook does NOT immediately name the concept (it poses the problem first)

### 3b. Report quality

Read `{LECTURE_PREFIX}-report.md`:

- [ ] Has `## Overview` (2-3 paragraphs)
- [ ] One `## [Concept]` section per major concept
- [ ] Each concept has Background / How it works / Visual treatment / Sources
- [ ] ≥3 real URLs per concept (spot-check at least 2)
- [ ] Has `## Lecture Design Decisions`

### 3c. Course overlap

Read `LAB_COVERAGE.md` and `LECTURE_COVERAGE.md` from repo root. For each concept in this lecture:

- [ ] Not already a primary teaching point of another lecture or lab — WARN (not FAIL) if found; some reinforcement is intentional

---

## Write README.md

After both passes pass, write `LECTURE_DIR/README.md`:

```markdown
# Lecture $0 — Instructor README

> Instructor-only. Not distributed to students directly — final distribution is the recorded Udemy video. This folder is the shooting-script package.

| File | Audience | Purpose |
|------|----------|---------|
| `$0-lecture.md` | Instructor | Teleprompter script with inline animations (primary recording asset) |
| `$0-report.md` | Instructor | Research background and sources |
| `animations/*.py` | Instructor | Manim source for each animation (for re-renders and tweaks) |
| `animations/*.gif` | Both | Inline preview on github.com (also committed) |
| `animations/*.mp4` | Both | Full-quality clip served from `videos.tail581af8.ts.net/[id]/` |

## Recording order

1. Review every animation by expanding the `$0-lecture.md` preview — click each GIF to play the mp4.
2. Record audio narration while reading each SPEAK block; pause 0.5s between beats.
3. Edit audio + animations together in your editor of choice.
```

---

## Report Format

```
# Review Report: Lecture $0

## Pass 1: Script Structure + Beat Discipline     [PASS / FAIL]
### File structure
- [PASS] ...
### Beat discipline
- [PASS] ...
### Animation coverage
- [PASS] ...

## Pass 2: Animation Quality + Library Usage      [PASS / FAIL]
### File triples
- [PASS] All 7 animations have .py + .gif
### Library usage
- [PASS] All library imports resolve in registry
### Render smoke test
- [PASS] All animations render cleanly at -ql

## Pass 3: Content Quality                        [PASS / FAIL]
### Content
- [PASS] First-principles discipline holds
### Report
- [PASS] ...
### Course overlap
- [WARN] "cache line" also touched in Lecture 2.4 — acceptable reinforcement

---
README.md written to $0/README.md
```

End with either "All components PASS. Ready for commit." or "Fix the FAIL items above, then re-run /review-lecture $0."
