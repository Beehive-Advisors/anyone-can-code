---
name: review-lab
description: Review a completed Anyone Can Code lab for correctness, pedagogy, output accuracy, script alignment, and overlap with prior labs. Use when the user asks to review, QA, or check a lab, or when a newly created lab needs a final pass.
metadata:
  short-description: Review a completed lab and write README
---

# Review Lab

Use this skill only in the Anyone Can Code course repo.

Before starting, read:
- `../.anyone-can-code-common/references/standards.md`
- `../.anyone-can-code-common/references/lab-format.md`
- `../.anyone-can-code-common/references/script-format.md`
- Relevant files under `../.anyone-can-code-common/references/tech-standards/` for each demo language present in the lab

Inputs:
- Required: lab section id such as `5.7`

## Workflow

### 1. Read The Lab Fresh

- Read every file in `<lab-id>/`.
- Required files:
  - `<lab-id>-lab.md`
  - `<lab-id>-script.md`
  - `<lab-id>-report.md`
- If any required file is missing, stop and report that immediately.

### 2. Detect The Mode

Determine whether the lab is:
- scaffolded
- direct-typing only

Use the presence of demo files plus the scaffolding rules from `standards.md`.

### 3. Verify Demo Execution

If scaffolded:
- run every demo file with the appropriate runtime
- require exit code 0
- check headers, section structure, labeled output, and a practical final section

If direct-typing:
- verify each Part contains multiple student-typed commands with individual output blocks
- confirm there is no leftover walkthrough file and no hidden script-wrapper approach

### 4. Review Written Material

Check:
- lab structure against `lab-format.md`
- script structure against `script-format.md`
- first-principles explanations before jargon
- question quality
- exercise quality
- output blocks match real tested runs
- README rules from `standards.md`

### 5. Review Course Overlap

- Compare the lab against `LAB_COVERAGE.md`.
- Duplicated primary teaching points are `WARN`, not `FAIL`, unless the new lab is plainly reteaching the same concept.

### 6. Write Or Rewrite README

If the lab passes:
- write `<lab-id>/README.md`
- keep it instructor-only
- include only the file-audience table and recording order required by `standards.md`

## Output Format

Return findings first, ordered by severity.

Use this structure:

```md
## Findings
- [FAIL] path:reason
- [WARN] path:reason

## Result
All components PASS. Ready for commit.
```

If there are no findings, say so explicitly.
