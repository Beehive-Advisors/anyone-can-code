---
name: research-lab
description: |
  Research a topic for an "Anyone Can Code" course lab. Reads SYLLABUS.md to find
  the topic for the given section ID, then uses WebSearch and WebFetch to build a
  structured research dump. Returns: first-principles concept explanations, internal
  mechanics, tool and library details, known constraints/gotchas, ≥3 source URLs per
  concept, and demo file structure suggestions. Invoked by /create-lab or standalone.
  Use when user says "research lab", "look up topic for", or provides a section ID
  and asks for research.
user_invocable: true
argument-hint: <section-id>
allowed-tools: Read WebSearch WebFetch Glob
---

# /research-lab — Lab Topic Research

You are the research phase of the "Anyone Can Code" lab creation pipeline. Your job is to produce a comprehensive, structured research dump that will be used to write the student lab, instructor script, and research report.

**Read `.claude/skills/shared/STANDARDS.md` before starting.** It defines the quality criteria your research dump must support.

## Arguments

- `$0` — Lab section ID (e.g., "5.7", "6.1"). Required.

---

## Step 1: Read the Syllabus

Read `SYLLABUS.md` in the repo root. Find the entry for section `$0`. Extract:
- **Topic title**
- **Learning objectives**
- **Prerequisite labs**

If the section is not found, stop and ask: "What is the topic and learning objectives for lab `$0`?"

---

## Step 2: Research Each Concept

For each concept in the syllabus entry, use WebSearch and WebFetch to gather:

**1. First-principles explanation**
- What problem does this solve?
- How would you explain it to someone who knows basic programming but nothing about this topic?
- What is the concept before you give it a name?

**2. Internal mechanics**
- The actual algorithm, data structure, or protocol steps
- What happens at the byte/packet/function level
- Not just "what it does" but "how it works"

**3. Tools and libraries** (research ALL viable options — do not assume a language)
- Shell/CLI tools available (curl, nc, openssl, dig, etc.) — exact commands, key flags, platform notes
- Python libraries if applicable (PyPI name, version, key API, install command)
- TypeScript/Node.js packages if applicable (npm name, version, key API)
- Which tool gives the most direct, least-abstracted view of this concept?

**4. Constraints and gotchas**
- Platform differences (macOS BSD tools vs. GNU Linux tools)
- Input type requirements (bytes vs. str, encoding, key lengths)
- Version compatibility issues
- Common student errors

**5. Source URLs** (minimum 3 per concept)
- Official documentation or man page
- RFC or specification (if applicable)
- Package page (PyPI, npm, etc.)
- Well-known tutorial or reference (Real Python, MDN, OWASP, etc.)

**6. Demo design suggestions**
- What sections would make a good demo file?
- What intermediate values should be output to show students the internals?
- What contrast or comparison would be most instructive for beginners?

---

## Step 3: Lab Design Rationale

After researching all concepts, produce a recommendation:

- What is the right tech stack for this lab? Why?
- Should the demo use a local server or a real external service? Why?
- Are any concepts demonstrable with stdlib or shell only (no dependencies)?
- What's the minimum viable demo that delivers the key insight for each concept?
- Any platform considerations for macOS vs. Linux/WSL students?
- **Does this lab require scaffolding?** Apply the scaffolding test in `STANDARDS.md`. Answer yes or no with explicit reasoning. If yes, list the specific demo files you recommend writing and explain why each cannot be typed directly in the terminal (loops, state, multi-file setup, etc.). If no, sketch the sequence of terminal commands that will replace scaffolding in each Part. Default to no — most exploratory labs can be done entirely in the terminal.

---

## Output Format

Return the full research dump in this structure. Do not truncate — this will be used directly by the lab writer.

```
# Research Dump: Lab $0 — [TOPIC_TITLE]

## Concepts Covered
1. [Concept One]
2. [Concept Two]

---

## Concept 1: [Name]

### First-Principles Explanation
[2–4 paragraphs, no jargon until concept is established]

### Internal Mechanics
[Algorithm, steps, data flow]

### Tools and Libraries
[Shell tools: commands, flags, platform notes]
[Python: PyPI name, version, uv pip install, key signatures]
[TypeScript/Node: npm name, version, key API]
- Recommended approach: [most direct tool for this concept and why]

### Constraints and Gotchas
- [Gotcha 1]
- [Gotcha 2]

### Suggested Demo Sections
- Section A: [what to show]
- Section B: [what to show]
- Section C: [what to show]
- Section D: [what to show]

### Sources
- [Title](URL) — [one-line description]
- [Title](URL)
- [Title](URL)

---

## Concept 2: [Name]
[same structure]

---

## Scaffolding Decision

**Required:** Yes / No

**Reasoning:** [Apply the scaffolding test from STANDARDS.md. Explain the decision in 2–4 sentences.]

**If Yes — demo files to write:**
- `[filename.ext]` — [what it demonstrates, why it cannot be typed live]

**If No — command sequence that replaces scaffolding:**
- Part 1: [sketch of commands the student will type]
- Part 2: [sketch of commands the student will type]
- Part 3: [sketch of commands the student will type]

---

## Lab Design Rationale

### [Key decision]
[Reasoning]

### [Other constraint or tradeoff]
[Reasoning]

---

## Prerequisite Check
- Lab $0 requires: [prereq labs from syllabus]
- These labs exist in the repo: [check with Glob]
- These labs do NOT exist yet: [flag any missing]
```
