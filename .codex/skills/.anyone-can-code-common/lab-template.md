# Lab Formatting Guidelines

Strict formatting rules for all student lab files (`[ID]-lab.md`). Follow these exactly. Do not add sections not listed here. Do not reorder sections. For pedagogical principles, see `STANDARDS.md`.

**Before writing the lab, decide whether it requires scaffolding** (see "The scaffolding test" in `STANDARDS.md`). The decision changes how each Part's "Run the demo" subsection is formatted. Most hands-on exploratory labs should land on *no scaffolding* — students type individual commands in the terminal.

---

## File header (top of file)

```markdown
# Lab [ID] — [TOPIC_TITLE]

**Section:** [Course section name]
**Prerequisites:** [Comma-separated list, or "None"]
**Time:** ~N minutes
```

Add a `**Files:** \`[ID]/\`` line **only** when the lab has scaffolding (i.e., there are demo files in the folder beyond the markdown). No-scaffolding labs omit this line — there are no demo files to point at.

---

## Section: What you'll build

Numbered list of 3–5 items.

Rules:
- Each item is a concrete, demonstrable outcome
- Past tense: "Hashed a password with bcrypt" not "Learn about hashing"
- No "understood" or "learned about" — only actions and artifacts

---

## Section: Setup

### Prerequisites
Checklist of required tools with version-check commands.

### Install dependencies
Exact setup commands for this lab's tech stack. After the install block, explain each package in one plain-English sentence.

For any CLI tool requiring installation, show both platforms side by side:
```
**macOS:** `brew install [tool]`
**Linux / WSL:** `sudo apt install [tool]`
```
Package managers that are cross-platform (uv, npm, Docker) do not need platform splits.

### Terminal setup
Include only if the lab requires two simultaneous processes. Specify which terminal runs which process and when to open the second one.

---

## Section: Part N — [Concept Name]

One Part per concept. Parts are numbered sequentially starting at 1.

### Required subsections (in this order)

**1. `### What is [term]?`**
- Start with the problem being solved, not the solution name
- 2–4 paragraphs
- Define every term before using it

**2. Run the demo**

The format depends on whether the lab has scaffolding (see `STANDARDS.md`).

**Direct-typing mode (no scaffolding — no demo files):**
Break this subsection into **2–4 discrete command blocks**. Each block is the smallest self-contained step a student types and observes. Per block:
- One framing sentence: what the student is about to do and why
- A fenced code block containing the exact command for the student to type
- An `**Output:**` heading followed by the verbatim output block (captured from a real tested run)
- 1–2 sentences tying that command's output to the concept

Do not collapse this into `bash demo.sh` + one giant output. The student should type every command themselves and see each result before moving to the next. This is the primary form of interactivity in no-scaffolding labs.

**Scaffolded mode (lab has demo files):**
- Exact command to run the demo file (e.g., `bash demo.sh` or `python3.12 demo.py`)
- `**Output (Section X):**` heading
- Verbatim output block (never invented — from tested run)
- 1–3 sentences explaining what each labeled output line means
- One sentence directing students to the code walkthrough video before continuing

**3. Conceptual question**
- One question testing WHY, not syntax recall
- Uses `<details><summary>Answer</summary>explanation</details>`

**4. `### Exercise`**
- One concrete task, 5–15 minutes
- Must require the student to type code or a command (not just read output)
- Builds directly on what was just demonstrated
- Uses `<details><summary>Solution</summary>solution + brief explanation</details>`

---

## Section: Putting it together

- Comparison table with columns: Mechanism | What problem it solves | Key idea | Real systems
- 1–3 sentences connecting all mechanisms

---

## Section: Checklist

Checkboxes for each concrete skill the student can now do or explain:
```markdown
- [ ] [Skill one]
- [ ] [Skill two]
```

---

## Section: Further Reading

Minimum 3 links. All URLs must be real — from the research dump, never invented.
```markdown
- [Title](URL) — one-line description
```

---

## Writing rules

- One thing per sentence
- One concept per paragraph
- Never repeat a concept from a prior section
- Every paragraph earns its place — if it can be cut without losing a learning objective, cut it
