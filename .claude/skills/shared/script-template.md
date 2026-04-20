# Script Formatting Guidelines

Strict formatting rules for all instructor script files. For pedagogical principles, see `STANDARDS.md`.

There are two possible script file types. The second is **conditional on the scaffolding test** (see `STANDARDS.md`):

1. **`[ID]-script.md`** — Terminal screencast shooting script. **Always written.**
2. **`[ID]-code-walkthrough.md`** — VS Code editor walkthrough (recorded before the terminal screencast). **Written only when the lab has scaffolding** (i.e., `.sh` / `.py` / `.ts` / Dockerfile / etc. demo files exist). A lab without demo files has nothing to walk through — skip this file entirely. Labs without scaffolding produce only the terminal script.

---

## Beat Format — Non-Negotiable

Every instructor action is labeled. Zero unlabeled prose anywhere in the script body.

### SPEAK
```
**SPEAK**
> "Spoken words. Short sentences. Establish concept before naming it."
```
Use for: conceptual intros, setup explanations, exercise framing, transitions, outro.

### TYPE
```
**TYPE**
```bash
exact command or code to type
```
```
Use for: all terminal commands, code edits, file opens. Never paraphrase. Exact keystrokes only.

### OUTPUT
```
**OUTPUT**
```
exact terminal output — verbatim from test run
```
```
Rules:
- Always verbatim from a tested run — never invented, never paraphrased
- For variable values, add on the next line: `*(Your [value] will look different — structure is the same.)*`
- For output >25 lines, show the most instructive portion and add `(output continues...)`

### EXPLAIN
```
**EXPLAIN**
> "What to say while output is visible. Walk through specific lines and labels."
```
Use for: narrating output, connecting output back to the concept.

---

## `[ID]-script.md` Structure

```markdown
# Instructor Script — Lab [ID]: [TOPIC_TITLE]

**Format:** Screencast — terminal only
**Estimated recording time:** ~N–M min
**Terminal:** VS Code integrated terminal or iTerm2. Font size 16+, dark theme.

---

## How to read this script

> **SPEAK** — say this out loud
> **TYPE** — type into the terminal
> **OUTPUT** — what you will see (verbatim from tested run)
> **EXPLAIN** — say this while output is visible

---

## INTRO

[SPEAK: why this lab matters — what the student will be able to do]
[TYPE: cd + env setup commands]
[OUTPUT: setup output verbatim]
[EXPLAIN: what the setup does]

---

## PART N — [CONCEPT NAME]

### What is [concept]?

[SPEAK: first-principles explanation — establish the idea before naming it]

### Run the demo

[TYPE: run command]
[OUTPUT: Section A output verbatim]
[EXPLAIN: walk through labeled output line by line]
[Continue OUTPUT + EXPLAIN pairs for each demo section]

### Exercise — [Exercise Name]

[SPEAK: what the exercise asks + why it matters]
[TYPE: solution code]
[TYPE: run command]
[OUTPUT: result verbatim]
[EXPLAIN: what the solution does]

---

## PUTTING IT TOGETHER

[SPEAK only: 2–4 sentences connecting all mechanisms]

---

## OUTRO

[SPEAK: 3 concrete skills the student can now do — frame as skills, not knowledge]

---

## Recording notes

[Lab-specific tips: pacing, font size, multi-terminal setup, pause points]
```

---

## `[ID]-code-walkthrough.md` Structure

```markdown
# Code Walkthrough Script — Lab [ID]: [TOPIC_TITLE]

**Format:** Screencast — VS Code editor
**Estimated recording time:** ~N min

---

## INTRO

[SPEAK: explain the two purposes of this video — the concept and the code]

---

## Concept: [The core idea]

[SPEAK: deep first-principles explanation — NO code yet. 2–4 minutes.
Every term the code uses is defined here before the code section that uses it.]

---

## [filename] — Section A: [description]

[TYPE: `code [filename]` to open in VS Code]

**EXPLAIN** (lines N–M — [brief description])
```[language]
# paste exact lines being explained — use application language, not bash
```
> "[Line-by-line narration. Every code reference must name the specific line(s):
> 'Line 49 is the speedup formula'. Never say 'this line' without a number.]"

[Repeat EXPLAIN block for each section]

---

[Repeat file section for each demo file]

---

## Recording notes

[Tips for pacing, scrolling, font size, conceptual-before-code reminder]
```

---

## Code walkthrough EXPLAIN format (required)

Every EXPLAIN beat in a code walkthrough must have all three of these:

1. **Parenthetical** immediately after `**EXPLAIN**`: `(lines N–M — brief description)`
2. **Fenced code block** using the application language (`python`, `typescript`, etc. — never `bash`)
3. **Narration** referencing specific line numbers — never "this line" without a number

Open files with `code [filename]` only. Never `cat`, `less`, or any terminal file display.

**Conceptual sections always come before code sections.** No exceptions.
