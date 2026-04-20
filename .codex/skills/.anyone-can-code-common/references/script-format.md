# Script Format

Use this structure for instructor-facing scripts.

Two script files are possible:
- `<lab-id>-script.md` is always required
- `<lab-id>-code-walkthrough.md` exists only when the lab has scaffolding

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

```md
# Instructor Script - Lab <id>: <title>

**Format:** Screencast - terminal only
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
