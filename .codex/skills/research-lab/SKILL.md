---
name: research-lab
description: Research an Anyone Can Code lab topic from a syllabus section and produce a structured research dump with first-principles explanations, mechanics, tooling options, gotchas, sources, and a scaffolding decision. Use when the user asks to research or look up a lab topic.
metadata:
  short-description: Research a lab topic and decide scaffolding
---

# Research Lab

Use this skill only in the Anyone Can Code course repo.

Before starting, read:
- `../.anyone-can-code-common/references/standards.md`

Inputs:
- Required: lab section id such as `5.7`

## Workflow

### 1. Resolve The Topic

- Read `SYLLABUS.md`.
- Extract the section title, learning objectives, and prerequisites for the requested lab id.
- If the section is missing, stop and ask for the topic and objectives.
- Read `LAB_COVERAGE.md` if present so prior labs are not repeated as primary teaching points.

### 2. Research Each Concept

For each major concept in the syllabus entry, gather:
- a first-principles explanation for beginners
- internal mechanics
- viable shell, Python, and TypeScript or Node options when relevant
- platform and version gotchas
- demo design ideas
- at least 3 real source URLs

Use current browsing because the research can be time-sensitive. Prefer primary sources.

### 3. Make A Scaffolding Decision

Apply the scaffolding test from `standards.md`.

Return one of:
- `Required: Yes`
- `Required: No`

Include 2 to 4 sentences of reasoning.

If `Yes`, list the recommended demo files and explain why each one cannot reasonably be typed live.

If `No`, sketch the command sequence that should replace scaffolding for each lab part.

### 4. Check Prerequisites

- Confirm which prerequisite lab directories already exist in the repo.
- Flag missing prerequisites.

## Output Format

Return a structured markdown report in this shape:

```md
# Research Dump: Lab <id> - <title>

## Concepts Covered

## Concept 1: <name>
### First-Principles Explanation
### Internal Mechanics
### Tools and Libraries
### Constraints and Gotchas
### Suggested Demo Sections
### Sources

## Scaffolding Decision
**Required:** Yes / No
**Reasoning:** ...
**If Yes - demo files to write:** ...
**If No - command sequence per Part:** ...

## Lab Design Rationale

## Prerequisite Check
```

Do not truncate. Include real links.
