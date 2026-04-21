# Script Format

Use this structure for instructor-facing scripts.

Every lab produces **two** terminal screencast shooting scripts — one per platform — and optionally a shared code walkthrough:

- `<lab-id>-script-macos.md` — always required; TYPE commands use macOS syntax; OUTPUT blocks are verbatim from a tested macOS run
- `<lab-id>-script-linux.md` — always required; TYPE commands use Linux / WSL syntax; OUTPUT blocks are verbatim from a tested Linux run (kubectl pod or Docker Ubuntu)
- `<lab-id>-code-walkthrough.md` — only when the lab has scaffolding; shared across both platform recordings (demo code is cross-platform)

The two terminal scripts share structure beat-for-beat — same Parts, same exercises, same SPEAK narration for concepts. They differ only in TYPE commands and OUTPUT blocks. Keep them in lockstep.

## Beat Labels

Every instructor action must be labeled.

### SPEAK

```md
**SPEAK**
> "Short spoken narration."
```

### TYPE

```md
**TYPE**
```bash
exact command or code
```
```

### OUTPUT

```md
**OUTPUT**
```text
verbatim output
```
```

### EXPLAIN

```md
**EXPLAIN**
> "Narration while the output or code is visible."
```

## Terminal Script Structure

Both `<lab-id>-script-macos.md` and `<lab-id>-script-linux.md` follow this structure identically. They differ only in the `**Platform:**` metadata, the exact TYPE commands, and the captured OUTPUT blocks.

```md
# Instructor Script - Lab <id>: <title> (macOS | Linux / WSL)

**Format:** Screencast - terminal only
**Platform:** macOS  |  Linux / WSL (Ubuntu 22.04+)
**Estimated recording time:** ~<n>-<m> min

## How to read this script

## INTRO

## PART N - <concept>

### What is <concept>?
### Run the demo
### Exercise - <exercise name>

## PUTTING IT TOGETHER

## OUTRO

## Recording notes
```

Rules:
- zero unlabeled prose
- TYPE and OUTPUT blocks must match the tested commands and output
- EXPLAIN beats should walk through specific lines or labels, not vague summaries

## Code Walkthrough Structure

Use only when scaffolded.

```md
# Code Walkthrough Script - Lab <id>: <title>

**Format:** Screencast - VS Code editor
**Estimated recording time:** ~<n> min

## INTRO

## Concept: <core idea>

## <filename> - Section A: <description>

## Recording notes
```

Rules:
- the conceptual section comes before code sections
- open files with `code <filename>`
- each EXPLAIN beat names the exact line numbers being discussed
- use fenced code blocks in the application language, not bash, when explaining source code
