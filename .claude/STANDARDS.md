# Course Lab Standards

All three lab skills — `create-lab`, `research-lab`, and `review-lab` — read and apply these standards. They represent the pedagogical principles and quality criteria that every lab must meet.

For language-specific rules (Python, shell, TypeScript, Docker), read the relevant file in `tech-standards/` based on the file extensions present in the lab.

See also:
- `lab-template.md` — exact formatting rules for student lab files
- `script-template.md` — exact formatting rules for instructor script files

---

## Audience

Students are beginner programmers — non-technical adults learning to code for the first time. They know basic programming syntax but nothing about the specific topic being taught. Every explanation must be accessible without being condescending.

---

## Pedagogical Principles

**First principles before jargon.**
Every technical term is explained from scratch the first time it appears. Start with the problem being solved, then the concept, then the name. Never use a term as if it's already understood.

**Ruthless simplicity.**
One thing per sentence. One concept per paragraph. If a sentence can be cut without losing meaning, cut it. Never repeat a concept already explained in a prior section. Minimum content for maximum clarity.

**Students build, not watch.**
Every lab produces something concrete. Outcomes are stated as actions: "I hashed a password with bcrypt", not "I learned about hashing."

---

## Interactivity — First-Class Requirement

Interactivity is not optional. Every Part of a lab must include both:

**1. Student types code or a command themselves.**
Not just runs a pre-written script. Acceptable forms: a one-liner in a REPL, a `curl` command they type manually, a short code block they write and run as part of an exercise. Pre-written demo scripts are fine *after* the student has typed something first.

**2. A conceptual question testing WHY.**
Not syntax recall or flag trivia. The question requires the student to reason through the concept.

Good: *"Why would the server wait forever if you don't send the blank line?"*
Bad: *"What flag suppresses the progress bar?"*

The test: can a student answer this by thinking through the concept, without memorizing syntax? If yes, it's good. If it's flag trivia, replace it.

Format questions with a collapsible answer:
```
> **Why does X work this way?**
> `<details><summary>Answer</summary>explanation from first principles</details>`
```

---

## Output Standards

**Never invent output.** Every OUTPUT block in a lab or script must be captured from an actual test run of the demo code. No approximations, no reconstructions from memory.

**Variable values:** Some output changes each run (hashes, tokens, timestamps). Paste the actual captured output and add: `*(Your [value] will look different — structure is the same.)*`

**Long output:** If output exceeds 25 lines, use the most instructive portion and add `(output continues...)`.

---

## Demo Code Standards

Regardless of language, every demo file must:

- Have a header comment explaining what it is and how to run it
- Have 3–4 sections with clear section banners
- Label every output line so students know what each line means
- End the last section with a practical contrast or demonstration (with-vs-without, tamper detection, before-vs-after)
- Exit with code 0 — no unhandled errors or warnings. Fix the root cause; never suppress.

See `tech-standards/` for language-specific rules.

---

## Research Report Standards

Each report covers:
- **Overview:** 2–3 paragraphs on what the lab covers and why it matters. No jargon without definition.
- **One section per concept:** Background → How it works → Implementation → Sources (≥3 real URLs per concept)
- **Lab Design Decisions:** Key choices explained for a beginner audience (local vs. external API, which tool, why)

All source URLs must be real — taken from actual research, never invented.

---

## README Standards

Each completed lab directory gets a `README.md` containing:
- 1–2 sentence description
- Prerequisites
- Exact setup commands
- File table: filename → description → how to run
- Time estimate
- Notes for any special requirements (e.g., two terminal windows)
