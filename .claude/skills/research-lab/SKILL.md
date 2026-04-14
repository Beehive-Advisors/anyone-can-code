---
name: research-lab
description: |
  Research a topic for an "Anyone Can Code" course lab. Reads SYLLABUS.md to find
  the topic for the given section ID, then uses WebSearch and WebFetch to build a
  structured research dump. Returns: first-principles concept explanations, internal
  mechanics, Python library details, known constraints/gotchas, ≥3 source URLs per
  concept, and demo file structure suggestions. Invoked by /create-lab or standalone.
  Use when user says "research lab", "look up topic for", or provides a section ID
  and asks for research.
user_invocable: true
argument-hint: <section-id>
allowed-tools: Read WebSearch WebFetch Glob
---

# /research-lab — Lab Topic Research

You are the research phase of the "Anyone Can Code" lab creation pipeline. Your job is to produce a comprehensive, structured research dump that will be used to write the student lab, instructor script, and research report for a new lab.

## Arguments

- `$0` — Lab section ID (e.g., "5.7", "6.1"). Required.

## Step 1: Read the Syllabus

Read the file at: `SYLLABUS.md` (in the repo root, same directory as this `.claude/` folder).

Find the line(s) matching section `$0`. Extract:
- **Topic title** (e.g., "Rate Limiting and Throttling")
- **Learning objectives** (bullet points listed under that section)
- **Prerequisite labs** mentioned

If `SYLLABUS.md` does not exist or section `$0` is not found, stop and ask: "What is the topic and learning objectives for lab `$0`?"

## Step 2: Research Each Concept

For each concept identified in the syllabus entry, use `WebSearch` and `WebFetch` to gather:

### What to find for each concept:

1. **First-principles explanation**
   - What problem does this solve?
   - How would you explain it to someone who only knows basic programming?
   - What is the concept before you give it a name?

2. **Internal mechanics**
   - The actual algorithm, data structure, or protocol steps
   - What happens at the byte/packet/function-call level
   - Not just "what it does" but "how it works"

3. **Python library details**
   - PyPI package name (exact, for `uv pip install`)
   - Current stable version
   - Key function names and signatures
   - How to import and use it in 5 lines or fewer (core usage)

4. **Constraints and gotchas** (critical — these cause bugs)
   - Input type requirements (bytes vs. str, encoding issues)
   - Key length requirements (e.g., PyJWT HS256 needs exactly 32-byte key)
   - Deprecated functions (e.g., `datetime.utcnow()` deprecated in Python 3.12)
   - Version compatibility issues

5. **Source URLs** (minimum 3 per concept)
   - Official documentation
   - RFC or specification (if applicable)
   - PyPI package page
   - Well-known tutorial or reference (e.g., Real Python, MDN, OWASP)

6. **Demo design suggestions**
   - What sections would make a good demo file?
   - What intermediate values should be printed to show students the internals?
   - What contrast/comparison would be most instructive (e.g., fast hash vs. slow hash)?

## Step 3: Synthesize Lab Design Rationale

After researching all concepts, answer:
- Should the demo use a local server or a real external API? Why?
- What are the tradeoffs of the approach you'd recommend for a beginner audience?
- Are there any concepts that can be demonstrated with stdlib only (no third-party library)?
- What's the minimum viable demo that shows the key insight for each concept?

## Output Format

Return the full research dump in this structure. Do NOT truncate. This will be used verbatim by the lab writer.

```
# Research Dump: Lab $0 — [TOPIC_TITLE]

## Concepts Covered
1. [Concept One]
2. [Concept Two]
(list from syllabus)

---

## Concept 1: [Name]

### First-Principles Explanation
[2–4 paragraphs, no jargon until the concept is established]

### Internal Mechanics
[How it actually works — algorithm, steps, data flow]

### Python Library: [package-name]
- PyPI: `package-name`
- Version: X.Y.Z
- Install: `uv pip install package-name`
- Core usage:
  [5-line code example]
- Key functions: [list with signatures]

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

## Lab Design Rationale

### [Key decision, e.g., "Local server vs. real API"]
[Reasoning]

### [Other constraint or tradeoff]
[Reasoning]

---

## Prerequisite Check
- Lab $0 requires: [list prereq labs from syllabus]
- These labs exist in the repo: [check with Glob]
- These labs do NOT exist yet: [flag any missing]
```
