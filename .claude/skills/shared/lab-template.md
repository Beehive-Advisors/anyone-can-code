# Lab Formatting Guidelines

Strict formatting rules for all student lab files (`[ID]-lab.md`). Follow these exactly. Do not add sections not listed here. Do not reorder sections. For pedagogical principles, see `STANDARDS.md`.

**Before writing the lab, decide whether it requires scaffolding** (see "The scaffolding test" in `STANDARDS.md`). The decision changes how each Part's "Run the demo" subsection is formatted. Most hands-on exploratory labs should land on *no scaffolding* — students type individual commands in the terminal.

**Every lab ships with two cross-platform tracks** (see "Cross-platform tracks" in `STANDARDS.md`). The macOS track is the instructor's primary platform (screencasts record natively on Mac). The Linux / WSL track lives in the same markdown file as parallel command blocks for students on Ubuntu / WSL2. Per-Part content is dual-labeled `**🍎 macOS**` and `**🐧 Linux / WSL**`.

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

## Section: Before you begin — pick your track

This is the **first section** after the file header — before `## What you'll build`. It is the student-facing toggle. Required format:

```markdown
## Before you begin — pick your track

This lab has two tracks in one file. Pick the one matching your operating system and follow the command blocks labeled for it throughout the lab.

<details>
<summary><b>🍎 I'm on macOS</b> — tap to see what this lab looks like for you</summary>

You'll use: `[tool 1]`, `[tool 2]`, `[tool 3]` — all installed by default on macOS (or via `brew install ...` if not).

Throughout the lab, every command block labeled **🍎 macOS** is yours. The **🐧 Linux / WSL** blocks do the same thing with different commands — skip them.

</details>

<details>
<summary><b>🐧 I'm on Linux or Windows/WSL</b> — tap to see what this lab looks like for you</summary>

You'll use: `[tool 1]`, `[tool 2]`, `[tool 3]` — installed by default on most distributions (or via `sudo apt install ...` if not). WSL students: always use WSL2, not WSL1.

Throughout the lab, every command block labeled **🐧 Linux / WSL** is yours. The **🍎 macOS** blocks do the same thing with different commands — skip them.

</details>
```

Keep each summary block tight — 2–4 lines of markdown. Name the specific tools the student will encounter in their track so they know what to expect.

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

The format depends on whether the lab has scaffolding (see `STANDARDS.md`). In both modes, the command/output content is **dual-labeled by platform** (see "Cross-platform tracks" in `STANDARDS.md`).

**Direct-typing mode (no scaffolding — no demo files):**
Break this subsection into **2–4 discrete command blocks**. Each block demonstrates the same concept on both platforms. Per block:

1. One framing sentence (shared): what the student is about to do and why.
2. 🍎 **macOS** command + Output pair (verbatim from tested macOS run):
   ```markdown
   **🍎 macOS**
   ```bash
   [exact command]
   ```
   **Output:**
   ```
   [verbatim captured output]
   ```
   ```
3. 🐧 **Linux / WSL** command + Output pair (parallel translation; verbatim from tested kubectl-pod or Docker Ubuntu run):
   ```markdown
   **🐧 Linux / WSL**
   ```bash
   [parallel Linux command]
   ```
   **Output:**
   ```
   [verbatim captured Linux output]
   ```
   ```
4. 1–2 sentences (shared) tying the commands' behavior to the concept. Don't repeat the explanation per platform — one paragraph below both blocks.

Do not collapse this into `bash demo.sh` + one giant output. The student should type every command themselves and see each result before moving to the next. This is the primary form of interactivity in no-scaffolding labs.

**Scaffolded mode (lab has demo files):**
The demo-file run command and its expected output are also dual-labeled:
```markdown
**🍎 macOS**
```bash
bash demo.sh        # or: python3.12 demo.py
```
**Output (Section X):**
```
[verbatim tested macOS run]
```

**🐧 Linux / WSL**
```bash
bash demo.sh
```
**Output (Section X):**
```
[verbatim tested Linux run — values differ, structure matches]
```
```
Plus: 1–3 sentences (shared) explaining what each labeled output line means, and one sentence directing students to the code walkthrough video.

**Output block rules:** every OUTPUT block must come from a tested run on the corresponding platform. macOS outputs are captured natively. Linux outputs are captured from a kubectl pod on the k0s cluster (preferred) or a Docker Ubuntu container (fallback). Never fabricate output — see `create-lab/SKILL.md` Phase 3 for the capture procedure.

**3. Conceptual question**
- One question testing WHY, not syntax recall
- Shared across platforms — the concept behind the command is the same regardless of OS
- Uses `<details><summary>Answer</summary>explanation</details>`

**4. `### Exercise`**
- One concrete task, 5–15 minutes
- Must require the student to type code or a command (not just read output)
- Builds directly on what was just demonstrated
- If the exercise involves platform-specific commands: present the exercise prompt once (shared), then provide two solution blocks inside the `<details><summary>Solution</summary>` — one labeled `**🍎 macOS**` and one labeled `**🐧 Linux / WSL**`
- If the exercise is platform-neutral (a pure-Python expression, a `curl` invocation): single solution block, no platform split

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
