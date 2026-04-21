# Anyone Can Code Standards

These standards are the **canonical, agent-agnostic** course pedagogy. Both the Codex-native skills (under `.codex/skills/`) and the Claude-native skills (under `.claude/skills/`) read from them. Agent-specific trees keep their own SKILL.md frontmatter and path conventions, but the semantic rules below — audience, scaffolding test, dual-track layout, output discipline, interactivity — are identical across both.

## Audience

The audience is non-technical adults learning to code for the first time. Assume they know a small amount of programming syntax, but not the underlying systems ideas.

Write for clarity:
- first principles before jargon
- one concept per paragraph
- one claim per sentence when possible
- no repetition that does not advance a learning objective

## Operating Rules

- Use current browsing for research. Prefer primary sources.
- Do not use subagents unless the user explicitly asked for delegation.
- For `create-lab`, commit and push by default after review passes and registry files are updated.
- Validate the `origin` remote before pushing and never force-push.
- Detect the current branch with `git rev-parse --abbrev-ref HEAD` and push to that branch (supports worktree workflows).
- Never invent output. Run the commands and capture it.

## Cross-platform Tracks

Every lab ships two parallel tracks in one `[id]-lab.md` file:
- 🍎 **macOS track** — the instructor's primary platform. OUTPUT blocks are verbatim from a tested macOS run.
- 🐧 **Linux / WSL track** — for students on Ubuntu / WSL2. Commands are parallel translations; OUTPUT blocks are verbatim from a tested Linux run.

The first section after the lab file header is `## Before you begin — pick your track`, containing two `<details>` blocks (one per platform) that act as the student-facing toggle. Shared content (conceptual intros, WHY questions, Putting-it-together, Checklist, Further Reading) is written once. Platform-specific content uses dual labeled blocks: every Run-the-demo subsection has a `**🍎 macOS**` TYPE+OUTPUT pair and a `**🐧 Linux / WSL**` TYPE+OUTPUT pair.

Instructor terminal scripts are produced per platform: `[id]-script-macos.md` and `[id]-script-linux.md`. The optional code walkthrough (only when scaffolded) is shared — demo code is cross-platform.

## Linux Testing Environment

The Linux track's OUTPUT blocks are captured from a real Linux host, not macOS. Preferred path: a Kubernetes pod on the bare-metal k0s cluster (node `carlo`). Fallback: a `docker run --rm ubuntu:22.04` container on the instructor's Mac. Docker on macOS runs in a Linux VM, so sysfs-dependent commands (`lsmem`, `lsblk`) may return reduced output; when accuracy matters, prefer the pod.

```bash
# Preferred: kubectl pod
kubectl run lab-capture --image=ubuntu:22.04 --restart=Never -- sleep 600
kubectl wait --for=condition=Ready pod/lab-capture --timeout=60s
kubectl exec lab-capture -- bash -c "apt-get update -qq && apt-get install -y -qq [deps]"
kubectl exec lab-capture -- bash -c "[command]"
kubectl delete pod lab-capture

# Fallback: Docker
docker run --rm ubuntu:22.04 bash -c "apt-get update -qq && apt-get install -y -qq [deps] && [command]"
```

## Scaffolding Test

Default to direct terminal typing.

A lab needs scaffolding only when at least one of these is true:
- the demo is a multi-step program with loops, functions, or state
- the demo needs multiple files
- a single logical unit is too long or error-prone to type live

Use this table:

| Signal | No scaffolding | Scaffolding |
| --- | --- | --- |
| Student interaction | 2 to 5 commands per Part | A program or file is the teaching unit |
| Files beyond markdown | None | One or more demo files |
| Complexity | Small commands or one-liners | Multi-line code with control flow or setup |
| Typing burden | Comfortable live typing | High typo risk or setup friction |

Consequences:
- No scaffolding: no demo files, no code walkthrough file, students type each command themselves.
- Scaffolding required: create only the necessary demo files, and add a code walkthrough file.

## Interactivity

Every Part of the lab must include:
- direct student action in the terminal or editor, on both platforms
- one conceptual question that tests why, not flag memorization

For direct-typing labs:
- each Part must have at least 2 distinct student-typed command blocks **per platform** (🍎 macOS and 🐧 Linux / WSL)
- each command gets its own output block
- do not collapse a Part into one wrapper script

For scaffolded labs:
- each Part still needs at least 1 student-typed command per platform in addition to running the demo

## Output Rules

- Every output block must come from a real run.
- If values vary per run, paste the actual output and add a short note that the learner's value will differ.
- If output is long, keep the most instructive portion and mark that it continues.

## Lab Deliverables

Always write:
- `<lab-id>-lab.md` — student lab with dual tracks (toggle at top, 🍎/🐧 per-Part blocks)
- `<lab-id>-script-macos.md` — macOS terminal screencast shooting script
- `<lab-id>-script-linux.md` — Linux / WSL terminal screencast shooting script
- `<lab-id>-report.md` — research report

Write only when scaffolding is required:
- `<lab-id>-code-walkthrough.md` — shared across both platform recordings; demo code is cross-platform

After review passes, ensure `<lab-id>/README.md` exists as an instructor-only navigation file.

## Research Expectations

The research phase must:
- explain the problem before naming the concept
- cover internal mechanics, not just effects
- compare viable tooling options
- produce **matched macOS and Linux command pairs** for every demo step (this is non-negotiable — the lab can't ship both tracks without them)
- provide at least 3 real sources per major concept

## Coverage Registry

Update `LAB_COVERAGE.md` for every new lab. Capture:
- concepts taught
- tools and commands demonstrated
- external services used, if any
- student exercises

If the matching row in `SYLLABUS.md` has no status, set it to `Draft`.

## README Rules

`README.md` is instructor-only and should not repeat student-facing setup content.

It contains exactly:
- a file-audience-purpose table (rows dynamically built from files actually present in the lab directory — omit rows for files that don't exist)
- a short recording order section naming: walkthrough first (if present), then macOS screencast, then Linux screencast
