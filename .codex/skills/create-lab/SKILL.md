---
name: create-lab
description: Create a complete Anyone Can Code lab from a syllabus section, including research, demo assets when justified, the student lab, instructor script, review pass, and coverage updates. Use when the user asks to create, build, make, or draft a lab for a specific section.
metadata:
  short-description: Create a full course lab from a section id
---

# Create Lab

Use this skill only in the Anyone Can Code course repo.

Before writing deliverables, read:
- `../.anyone-can-code-common/references/standards.md`
- `../.anyone-can-code-common/references/lab-format.md`
- `../.anyone-can-code-common/references/script-format.md`
- Relevant files under `../.anyone-can-code-common/references/tech-standards/` for each demo language you choose

Inputs:
- Required: lab section id such as `5.7`

Operate autonomously unless blocked by missing source material or a failing environment check you cannot fix safely.

## Workflow

### 1. Preflight

- Confirm `SYLLABUS.md` exists in the repo root.
- Stop if `<lab-id>/` already contains markdown files.
- Read `SYLLABUS.md` and extract the matching section title, learning objectives, and prerequisites.
- Read `LAB_COVERAGE.md` if present to avoid reteaching prior material.

### 2. Research

- Research the topic with current primary sources. Prefer official docs, RFCs, standards, man pages, language docs, MDN, package docs, and other primary references.
- Capture enough detail to explain:
  - first principles
  - internal mechanics
  - viable tool choices
  - platform gotchas
  - at least 3 real URLs per major concept
- Apply the scaffolding test from `standards.md`.
- Default to direct terminal typing unless scaffolding is clearly necessary.
- Do not use subagents unless the user explicitly asked for delegation.

### 3. Build The Lab Assets

- Create `<lab-id>/`.
- If scaffolding is required, set up the smallest runtime needed and write only the demo files that the research supports.
- If scaffolding is not required, do not create demo files.
- Run every demo file or terminal command sequence yourself.
- Capture verbatim output from real runs. Never invent output.
- Fix failures before proceeding.

### 4. Write Deliverables

Write:
- `<lab-id>/<lab-id>-report.md`
- `<lab-id>/<lab-id>-lab.md`
- `<lab-id>/<lab-id>-script.md`

Write only when scaffolding is required:
- `<lab-id>/<lab-id>-code-walkthrough.md`

Follow the shared reference docs exactly for structure, pedagogy, and formatting.

### 5. Review

- Run the checklist in `../review-lab/SKILL.md` against the finished lab.
- Fix every FAIL item before finishing.
- If the review passes, ensure `<lab-id>/README.md` exists and matches the review skill requirements.

### 6. Update Registry Files

- Append or update the lab entry in `LAB_COVERAGE.md`.
- If the matching lab row in `SYLLABUS.md` has no status, set it to `Draft`.
- Make the smallest safe edits. Do not rewrite unrelated rows.

### 7. Git Rules

- Do not commit, amend, or push unless the user explicitly asked for git actions.
- If the user did ask for git actions, stage only the new lab files and the intentional registry updates.

## Output Expectations

When the skill completes, report:
- the lab id and title
- whether scaffolding was required
- which files were created
- what verification you ran
- any residual risks or follow-up items
