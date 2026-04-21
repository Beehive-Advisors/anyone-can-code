# Lab Formatting Guidelines

Strict formatting rules for all student lab files (`[ID]-lab.md`). Follow these exactly. Do not add sections not listed here. Do not reorder sections. For pedagogical principles, see `STANDARDS.md`.

**Before writing the lab, decide whether it requires scaffolding** (see "The scaffolding test" in `STANDARDS.md`). The decision changes how each Part's "Run the demo" subsection is formatted. Most hands-on exploratory labs should land on *no scaffolding* — students type individual commands in the terminal.

**Every lab ships with two cross-platform tracks** (see "Cross-platform tracks" in `STANDARDS.md`). The macOS track is the instructor's primary platform (screencasts record natively on Mac). The Linux / WSL track runs under Ubuntu 22.04 / WSL2. The two tracks live in one file as **two full-track `<details>` collapsibles** at the top — the student picks one with a single click and reads top to bottom within it. Commands inside a given track are platform-native (no dual 🍎/🐧 labels inside a single track).

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

## Section: Pick your track

This is the **first section after the file header, and it contains the entire body of the lab**. Nothing lives outside the two collapsible tracks except the header, this intro, and the closing `</details>` tags. Each student clicks one toggle and reads from there to the bottom.

Required format:

```markdown
## Pick your track

This lab has two versions in one file. **Click the one matching your operating system** and follow it top to bottom. You never need to open the other.

<details>
<summary><b>🍎 Click here if you're on macOS</b></summary>

[FULL macOS lab — What you'll build, Setup, Parts 1..N, Putting it together, Checklist, Further Reading — all using macOS commands and outputs only]

</details>

<details>
<summary><b>🐧 Click here if you're on Linux or Windows/WSL</b></summary>

[FULL Linux/WSL lab — same sections as macOS track, mirroring section-for-section, but with Linux commands and outputs only]

</details>
```

**Why this layout:** the student clicks once and sees only their platform. No per-Part switching, no filtering mentally through `🍎`/`🐧` blocks throughout the lab. The tradeoff is that shared conceptual content (What-you'll-build items, WHY answers, Putting-it-together summary) is written twice — once in each track. That duplication is intentional; keeping the tracks self-contained is worth more than a minor reduction in word count.

**Keep the two tracks in lockstep.** Same number of Parts, same exercises, same conceptual intros (`### What is X?`), same WHY questions. The only differences are:
- Setup block install commands (`brew install` vs `sudo apt install`)
- Every TYPE command (macOS-native vs Linux-native)
- Every OUTPUT block (verbatim from that platform's tested run)
- Minor tool-specific notes (e.g., APFS container talk in the macOS disk section vs WSL2 virtual-disk talk in the Linux disk section)

---

## Section: What you'll build

This section and everything else below appears **inside each platform's `<details>` block**, once per track. The following formatting rules apply identically to both track copies.

---

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

Inside a given track, commands are platform-native — the student following the macOS track sees only macOS commands, and vice versa. Do NOT put dual-labeled blocks inside a track; that was the old format.

The format depends on whether the lab has scaffolding (see `STANDARDS.md`).

**Direct-typing mode (no scaffolding — no demo files):**
Break this subsection into **2–4 discrete command blocks**. Per block:
- One framing sentence: what the student is about to do and why
- A fenced code block with the exact command for their platform
- An `**Output:**` heading followed by the verbatim output block (captured from a tested run on that platform)
- 1–2 sentences tying that command's output back to the concept

Do not collapse this into `bash demo.sh` + one giant output. The student types every command themselves and sees each result before moving to the next.

**Scaffolded mode (lab has demo files):**
- Exact command to run the demo file (e.g., `bash demo.sh` or `python3.12 demo.py`)
- `**Output (Section X):**` heading
- Verbatim output block from a tested run on that platform
- 1–3 sentences explaining what each labeled output line means
- One sentence directing students to the code walkthrough video before continuing

**Output block rules:** every OUTPUT block must come from a tested run. For the macOS track, outputs are captured natively on the instructor's Mac. For the Linux track, outputs are captured from a kubectl pod on the k0s cluster (preferred) or a Docker Ubuntu container (fallback). Never fabricate output — see `create-lab/SKILL.md` Phase 3.

**3. Conceptual question**
- One question testing WHY, not syntax recall
- The text of the question can be identical in both tracks (concepts are platform-neutral), but write it into both — don't try to share
- Uses `<details><summary>Answer</summary>explanation</details>`

**4. `### Exercise`**
- One concrete task, 5–15 minutes
- Must require the student to type code or a command (not just read output)
- Builds directly on what was just demonstrated
- Commands use the track's platform-native syntax. No dual blocks inside the Exercise — the student is already in their chosen track.
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
