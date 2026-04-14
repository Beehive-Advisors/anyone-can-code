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
   - How would you explain it to someone who only knows basic terminal usage and Python basics?
   - What is the concept before you give it a name?

2. **Internal mechanics**
   - The actual algorithm, data structure, or protocol steps
   - What happens at the byte/packet/function-call level
   - Not just "what it does" but "how it works"

3. **Tool and library details** (research ALL viable options — don't assume Python)
   - Shell/CLI tools available (curl, nc, openssl, dig, tcpdump, ss, iptables, etc.)
   - Python libraries if applicable (PyPI name, version, key API)
   - TypeScript/Node.js packages if applicable (npm name, version, key API)
   - Which tool gives the most direct, least-abstracted view of the concept?

4. **Constraints and gotchas** (critical — these cause bugs)
   - Platform differences (macOS BSD tools vs. GNU Linux tools)
   - Input type requirements (bytes vs. str, encoding issues, key lengths)
   - Version compatibility issues
   - Common student errors

5. **Source URLs** (minimum 3 per concept)
   - Official documentation or man page
   - RFC or specification (if applicable)
   - Package page (PyPI, npm, etc.)
   - Well-known tutorial or reference (Real Python, MDN, OWASP, etc.)

6. **Demo design suggestions**
   - What sections would make a good demo file?
   - What intermediate values should be printed/output to show students the internals?
   - What contrast/comparison would be most instructive?

## Step 3: Synthesize Lab Design Rationale + Technology Recommendation

After researching all concepts, produce a technology recommendation:

**Technology decision framework:**

| If the lab is about... | Preferred approach | Why |
|------------------------|-------------------|-----|
| Protocols and networking (HTTP, DNS, TCP, TLS) | Shell scripts — curl, nc, openssl, dig | Closest to the wire, shows raw bytes/text |
| OS and system tools (processes, files, permissions) | Shell commands directly | Students should use the real tool |
| Crypto, auth, hashing, JWT | Python 3.12 with uv | Excellent libraries, short readable demos |
| Building a backend API or server | Python (FastAPI/Flask) or TypeScript (Express/Node.js) | Pick based on what's being taught |
| Frontend / full-stack UI | TypeScript + Next.js 15 + shadcn/ui + Tailwind CSS | Modern production stack |
| Databases | Direct CLI tools first (psql, redis-cli, mongosh), then ORM/driver if needed | Students see the protocol, not abstraction |
| Container / infrastructure | Docker CLI, kubectl, shell scripts | The tools themselves are what's being learned |

**Decision rule: Always use the most direct tool first. Shell before Python. CLI before library. Only add a higher-level abstraction when that abstraction is what the lab is explicitly teaching.**

Answer these questions:
- What is the right technology stack for this lab? (shell, Python, TypeScript, multiple?)
- Should the demo use a local server or a real external service? Why?
- Are there any concepts demonstrable without any dependencies (stdlib/shell only)?
- What's the minimum viable demo that delivers the key insight for each concept?
- Any platform considerations for macOS vs. Linux/WSL students?

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

### Tools and Libraries
[For shell tools: exact commands, key flags, platform notes (macOS vs. Linux)]
[For Python: PyPI name, version, `uv pip install <name>`, key function signatures]
[For TypeScript/Node: npm package name, version, `npm install <name>`, key API]
[For Docker/kubectl/CLI tools: exact commands to install and use]
- Recommended approach: [which tool is most direct for this concept?]

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
