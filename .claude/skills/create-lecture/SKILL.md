---
name: create-lecture
description: |
  Create a complete video lecture for the "Anyone Can Code" Udemy course.
  Writes a lecture script with inline Manim animations, generates each
  animation via /animate, walks you through a terminal-based approval
  loop per animation, uploads mp4s to the Tailscale video pod, commits
  GIF previews + .py source to the repo, and pushes. Mirrors /create-lab's
  9-phase structure. Use when user says "create lecture", "make lecture",
  "new lecture", "build lecture", or gives a lecture section ID like "1.4"
  and asks to build it.
user_invocable: true
argument-hint: <section-id>
allowed-tools: Read Write Edit Glob Grep Bash Agent WebSearch WebFetch
---

# /create-lecture — Full Lecture Creation

You are building a complete lecture for the "Anyone Can Code" Udemy course — a screencast narration script with inline Manim animations. This is the **lecture** counterpart to `/create-lab`; it mirrors that skill's phase structure wherever possible, and diverges only where lectures genuinely differ from labs.

**Key differences from `/create-lab`:**

1. **Lectures have no platform tracks.** Viewers watch recorded video; they're not typing commands. There is no macOS/Linux dual-track, no `<details>` collapsibles, no `Pick your track`. The output is **one** file: `[ID]-lecture.md`.
2. **Lectures have Manim animations inline.** Each Part contains `SHOW-ANIMATION` beats. Animations are generated via the `/animate` skill, with a terminal-based feedback loop where the instructor approves or regenerates each clip before it lands in the script.
3. **Lectures draw from a shared visual library.** The `anyone_can_code_assets` package at `~/src/projects/manim-library/` holds reusable components (CPU, RAM, cache, etc.). Animations MUST prefer library components over ad-hoc geometry; new assets require explicit approval via `proposed_new_assets.md`.
4. **Lectures host mp4s externally.** GIF previews get committed to the repo (for inline render on github.com); mp4s go to the Caddy pod at `https://videos.tail581af8.ts.net/`. The `VIDEO_BASE_URL` config at the top of this skill swaps the host.

**Before writing any deliverable:** read `.claude/skills/shared/STANDARDS.md`, `.claude/skills/shared/lecture-template.md`, and `.claude/skills/shared/lecture-script-template.md`. Also read `~/src/projects/manim-library/SKILL.md` and `~/src/projects/manim-skill/skill/SKILL.md` so you know how to invoke `/animate` with library-aware prompts.

## Arguments

- `$0` — Lecture section ID (e.g., "1.4", "2.2"). Required. The section in SYLLABUS.md must have `Format: Demo / Animation` — lab rows are not eligible.

## Paths and config

```
REPO_ROOT         = current working directory (where SYLLABUS.md lives)
LECTURE_ID        = $0
LECTURE_DIR       = $0/ relative to repo root
ASSETS_REPO       = ~/src/projects/manim-library
VIDEO_BASE_URL    = https://videos.tail581af8.ts.net        # Tailscale Caddy pod
                    # If the pod is not yet deployed, temporarily set to an empty
                    # string; the skill will leave mp4 URLs as relative paths
                    # and print a reminder at the end.
```

---

## PHASE 0: Preflight

**Step 1: Check if lecture already exists**

Use Glob to check if `LECTURE_DIR` contains `[ID]-lecture.md`:
```
pattern: $0/$0-lecture.md
```
If it exists, stop:
> "Lecture `$0` already exists. Delete `$0/` first or choose a different section ID."

**Step 2: Read the syllabus and coverage registries**

Read `SYLLABUS.md`. Find the entry for section `$0`. Extract:
- `TOPIC_TITLE` — the lecture name
- `LEARNING_OBJECTIVES` — the concepts listed in the syllabus row (the description text after the `:` is the rich objective list)
- `PREREQUISITES` — any prior lecture/lab mentioned

Validate:
- The row's `Format` column must be `Demo / Animation`, not `Lab`. If it's a Lab row, stop and tell the user to use `/create-lab`.
- The row's `Status` must be empty or `Draft` — not `Approved` (would overwrite approved work).

Read `LAB_COVERAGE.md` and `LECTURE_COVERAGE.md` (if they exist). Store contents as `LAB_COVERAGE_EXISTING` and `LECTURE_COVERAGE_EXISTING`. Missing file → empty string.

**Step 3: Verify the asset library is installed**

```bash
python3 -c "import anyone_can_code_assets" 2>&1
```

If this fails with ImportError:
```bash
cd ~/src/projects/manim-library && uv venv .venv --python 3.12 && source .venv/bin/activate && uv pip install -e .
```

Print: `"Creating Lecture $0: [TOPIC_TITLE] — starting research phase..."`

---

## PHASE 1: Research

Spawn an Agent to research the topic. Same pattern as `/create-lab`, but tuned for conceptual teaching (not hands-on labs).

Spawn with:
- `description`: `"Research for Lecture $0: [TOPIC_TITLE]"`
- `subagent_type`: `"general-purpose"`
- `prompt`:

---
**[AGENT PROMPT — substitute actual values for $0, TOPIC_TITLE, LEARNING_OBJECTIVES, LAB_COVERAGE_EXISTING, LECTURE_COVERAGE_EXISTING]**

You are researching "[TOPIC_TITLE]" for Lecture $0 of the "Anyone Can Code" beginner programming course. This is a **recorded video lecture** — narration over animations, not a hands-on lab. The audience is non-technical adults who know basic programming but nothing about this specific topic.

Learning objectives / concepts from the syllabus:
[LEARNING_OBJECTIVES]

## Already-covered concepts (do NOT re-teach as primary)

Lab coverage:
[LAB_COVERAGE_EXISTING — or "None — no labs covered yet."]

Lecture coverage:
[LECTURE_COVERAGE_EXISTING — or "None — this is the first lecture."]

Use WebSearch and WebFetch to research every concept. For EACH concept, produce:

**1. First-principles explanation**
What problem does this solve? Start with the problem before naming the concept. No jargon until the idea is established.

**2. Internal mechanics**
The actual algorithm, protocol, or mechanism at the byte / transistor / packet level. Not "what it does" — "how it works."

**3. Visual metaphor candidates**
What picture or motion shows this concept clearly? Think animation-first. Suggest 2–3 possible visual treatments, each describable as a 4–8 second animation. For each:
- **Frame 0 (static)**: what the viewer sees before motion starts
- **Motion**: what changes and why
- **Ending state**: what the viewer takes away
- **Which library assets would this use?** (refer to `registry.json` at ~/src/projects/manim-library — candidates: CPU, RAM, NVMe, HDD, Bus, Register, Cache, ALU)

**4. Constraints and gotchas**
- Common misconceptions beginners hold about this topic
- Terms that SOUND similar but are distinct (latency vs bandwidth, cache miss vs page fault, etc.)
- Depth boundary — what we explicitly WON'T cover because it belongs in a later section

**5. Sources** (minimum 3 per concept)
Official specs, canonical textbook chapters, well-known explainers (e.g., Computerphile, Ben Eater), recent benchmarks or articles.

After all concepts, produce **Animation Plan** and **Lecture Design Rationale**.

**Animation Plan** — for the whole lecture, enumerate the animations you propose:
- Table: `| # | name | purpose | library assets | est duration |`
- Target: 4–8 animations per 10 minutes of lecture. Lectures targeting 15-20 min typically have 6-12 animations.
- Every row's `library assets` column lists registry names; any row that cannot be covered by existing assets is marked `NEW:<proposed-asset-name>` and briefly describes what the new asset would be.

**Lecture Design Rationale** — cover:
- What's the right narrative arc? (problem → first-principles → mechanism → why it matters)
- Which concept deserves the most animation time, and which can be a single static diagram?
- Length target (minutes of finished video). Default 10–15 min.
- Does this lecture depend on a concept from a lab or prior lecture not yet built? Flag gaps.

Return the full research dump in structured markdown:

```
# Research Dump: Lecture $0 — [TOPIC_TITLE]

## Concept 1: [Name]
### First-Principles Explanation
### Internal Mechanics
### Visual Metaphor Candidates
### Constraints and Gotchas
### Sources

## Concept 2: [Name]
[same structure]

## Animation Plan

| # | name | purpose | library assets | est duration |
|---|------|---------|----------------|--------------|
| 1 | cpu-intro | establish CPU as compute engine | CPU | 6s |
...

## Lecture Design Rationale

### Narrative arc
### Animation emphasis
### Length target
### Prerequisite gaps
```
---
**[END AGENT PROMPT]**

Store the full return value as `RESEARCH_DUMP`. Do not proceed until the agent completes.

---

## PHASE 2: Asset Planning

**Step 1: Parse the Animation Plan**

Extract every `library assets` cell from the RESEARCH_DUMP's Animation Plan table. Produce two lists:
- `EXISTING_ASSETS` — registry names (CPU, RAM, etc.)
- `NEW_ASSETS` — entries prefixed with `NEW:`

**Step 2: Verify existing asset names**

For each name in `EXISTING_ASSETS`, run:
```bash
python3 ~/src/projects/manim-library/scripts/search_assets.py "[name]" --json
```

If `search_assets.py` returns an empty matches list for any name, the research phase got a name wrong. Move that name to `NEW_ASSETS` and note the correction.

**Step 3: If `NEW_ASSETS` is empty, skip to Phase 3.**

**Step 4: Write `proposed_new_assets.md`** (only if `NEW_ASSETS` is non-empty)

Create `LECTURE_DIR/proposed_new_assets.md`:

```markdown
# Proposed New Assets — Lecture $0

The research phase identified animations that no existing asset in
`registry.json` can satisfy. Review each proposal below.

Approve or edit each proposal, then reply with:

  - **"approve all"** — accept all proposals as-is
  - **"approve 1,3"** — accept only these (comma-separated numbers)
  - **"revise 2: <new description>"** — redraft a proposal
  - **"reject all"** — cancel the lecture build

## Proposed assets

### 1. [AssetName]
- **Category:** [e.g., hardware, memory, network]
- **Used by animation:** [animation name from the plan]
- **Description:** [one sentence]
- **When to use elsewhere:** [future lectures where this might be reused]
- **Synonyms:** [comma-separated]

### 2. [AssetName]
[same structure]
```

Then **pause** and print to the terminal:
```
Lecture $0 proposes [N] new assets to the library. See LECTURE_DIR/proposed_new_assets.md.
Respond: "approve all" | "approve 1,3" | "revise 2: ..." | "reject all"
```

Wait for the user's chat response. Do not continue until they reply.

**Step 5: On approval, scaffold and build new assets**

For each approved proposal:
```bash
cd ~/src/projects/manim-library && source .venv/bin/activate && python3 scripts/scaffold_asset.py \
    --name [AssetName] \
    --category [category] \
    --description "[description]" \
    --when-to-use "[when_to_use]" \
    --synonyms "[synonyms]"
```

The scaffold generates a minimal stub. Open the new file and flesh out geometry to match the description — look at `hardware/cpu.py` as the reference pattern (Rectangle + sub-part accessors + `attach_label`). Keep it simple; the goal is usable-in-a-lecture, not a masterpiece.

Render a thumbnail:
```bash
python3 scripts/build_catalog.py --only [AssetName]
```

Commit the library changes:
```bash
cd ~/src/projects/manim-library && git add -A && git commit -m "feat: add [AssetName] for Lecture $0"
```

Delete `LECTURE_DIR/proposed_new_assets.md` after all approved assets are built.

---

## PHASE 3: Lecture Directory Scaffold

```bash
mkdir -p $0/animations
```

`animations/` holds the per-lecture `.py` source files AND the GIF previews (both committed). mp4s are generated here first, then uploaded to the pod and NOT committed.

Add the GitHub-side ignore rule:
```bash
echo "$0/animations/*.mp4" >> .gitignore
# (only add if not already present)
```

---

## PHASE 4: Write Research Report

Write `$0/[LECTURE_ID]-report.md`. Same shape as the lab research report — 200–400 lines, `## Overview` + one section per concept with Background / How it works / Implementation (here: "visual treatment" instead of "tool") / Sources.

```markdown
# Research Report: Lecture $0 — [TOPIC_TITLE]

## Overview
[2–3 paragraphs, no jargon without definition.]

## 1. [Concept]

### Background
[First-principles explanation.]

### How it works
[Internal mechanics. ASCII diagrams, tables, short code samples are fine.]

### Visual treatment
[Which animation(s) teach this concept, referencing the Animation Plan.
State the library assets used and the motion that shows the concept.]

### Sources
- [Title](URL)
- [Title](URL)
- [Title](URL)

## 2. [Concept]
[same structure]

## Lecture Design Decisions
### [Key decision]
### [Tradeoff]
```

---

## PHASE 5: Write Lecture Script (with ANIMATE placeholders)

Write `$0/[LECTURE_ID]-lecture.md`. Follow `.claude/skills/shared/lecture-template.md` exactly.

Every animation beat is written as a placeholder:

```markdown
**SHOW-ANIMATION**
<!-- ANIMATE: "Natural-language description of what happens in the animation" {name: cpu-intro, assets: [CPU]} -->
```

Rules:
- **Every** SHOW-ANIMATION uses the placeholder form. Do not attempt to embed a rendered GIF here — Phase 6 generates all animations.
- **`name:`** values must be unique within this lecture and are file-system safe (lowercase, hyphens, no spaces).
- **`assets:`** values must appear in `registry.json`. Re-run `search_assets.py` to confirm.
- Every `## Part N` has at least one animation. Lectures without animations are not lectures — use plain markdown.

Target length: mirror the Animation Plan's duration estimate (≈100 spoken words per minute of video; a 10-min lecture is ~1000 words of SPEAK total).

---

## PHASE 6: Generate Animations (WITH FEEDBACK LOOP)

This is the longest phase. For each `<!-- ANIMATE: ... -->` placeholder in the script, run this loop:

### 6a. Parse the placeholder

From the comment, extract:
- `prompt` — the natural-language description
- `name` — the file stem
- `assets` — the library asset names

### 6b. Build the animation Python file

Write `LECTURE_DIR/animations/[name].py` directly (do **not** delegate to `/animate` for scene authoring, because we need to ensure the library assets are used). Template:

```python
from manim import Scene, LEFT, RIGHT, UP, DOWN, ORIGIN
from anyone_can_code_assets import [assets_imported]

class [PascalCaseName](Scene):
    """[the prompt, verbatim]"""
    def construct(self):
        # Build: instantiate library assets with sensible placement.
        # Animate: one beat per self.play, run_time 1-3s.
        # Hold: self.wait(1) at end.
        ...
        self.wait(1)
```

Use the patterns in `~/src/projects/manim-skill/skill/SKILL.md` ("Canonical Patterns" section) — `ReplacementTransform`, `ValueTracker`, `always_redraw`, `TransformMatchingTex`. Draw sub-part accessors from the library (e.g., `cpu.get_core(1)`).

Target: 4–8 seconds of total animation time. Short is better.

### 6c. Render at low quality for fast feedback

```bash
cd LECTURE_DIR/animations && source ~/src/projects/manim-library/.venv/bin/activate && \
  manim render -ql --media_dir ./media [name].py [PascalCaseName] 2>&1
```

On success, manim prints `File ready at <path>`. Extract the mp4 path.
On failure: diagnose (LaTeX? API? updater?), edit `.py`, re-render. After 2 failed retries, surface the full error to the user and ask for guidance.

### 6d. Generate the GIF preview

```bash
ffmpeg -y -i [mp4-path] -vf "fps=12,scale=480:-1:flags=lanczos" -loop 0 \
  LECTURE_DIR/animations/[name].gif 2>&1 | tail -2
```

Move the mp4 next to the GIF:
```bash
mv [manim-output-mp4] LECTURE_DIR/animations/[name].mp4
```

### 6e. Open and present to the user

```bash
open LECTURE_DIR/animations/[name].mp4
```

Then print in the terminal:

```
────────────────────────────────────────────────────────────────
Animation [K]/[TOTAL] · [name]
  prompt: [prompt text]
  assets: [assets list]
  files:  LECTURE_DIR/animations/[name].{mp4,gif,py}

(a)pprove  (r)egenerate with feedback  (s)kip  (e)dit .py directly  (q)uit

Waiting for your reply...
────────────────────────────────────────────────────────────────
```

### 6f. Act on the reply

- **`a` / "approve"**: keep as-is. Swap the placeholder in `[LECTURE_ID]-lecture.md` for:
  ```markdown
  [![name](./animations/[name].gif)]($VIDEO_BASE_URL/$0/[name].mp4)
  ```
  If `VIDEO_BASE_URL` is empty, use `./animations/[name].mp4` and note it in a `UPLOAD_REMINDER` variable. Move to the next animation.

- **`r` / "regenerate: <feedback>"**: append the user's feedback to the original prompt, rewrite `[name].py` accordingly, and loop back to 6c. Keep a counter — if the same animation regenerates >5 times, pause and ask the user to (e)dit or (s)kip.

- **`s` / "skip"**: leave the placeholder unchanged. Add a note to a `SKIPPED_ANIMATIONS` list; present at the end.

- **`e` / "edit"**: print the path to the `.py`, ask the user to edit it, and wait for them to reply `done`. Then loop back to 6c (re-render).

- **`q` / "quit"**: stop Phase 6 entirely. Report what was approved vs skipped and let the user decide whether to commit partial progress.

### 6g. Upload approved mp4s to the pod

After ALL animations are approved / skipped, upload the approved mp4s:

```bash
# Confirm pod is reachable
kubectl get deploy course-videos -n course-videos 2>/dev/null | tail -1

# If the deployment exists and is ready:
POD=$(kubectl get pod -n course-videos -l app=course-videos -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n course-videos $POD -- mkdir -p /srv/$0
for mp4 in LECTURE_DIR/animations/*.mp4; do
  kubectl cp "$mp4" course-videos/$POD:/srv/$0/$(basename "$mp4")
done

# Verify
curl -sI $VIDEO_BASE_URL/$0/ | head -1
```

If the pod is not yet deployed (beehive-dev PR pending), skip this step and record `UPLOAD_DEFERRED=true`. The lecture markdown will have relative `./animations/*.mp4` links that resolve when the mp4s are uploaded later. Print a reminder at the end of Phase 8.

---

## PHASE 7: Quality Review

Spawn an Agent to run `/review-lecture` independently — fresh read of all files.

Spawn with:
- `description`: `"Quality review for Lecture $0: [TOPIC_TITLE]"`
- `subagent_type`: `"general-purpose"`
- `prompt`:

---
**[AGENT PROMPT — substitute $0]**

You are reviewing Lecture $0 of the "Anyone Can Code" course. Read all files in `$0/` fresh.

1. Read `STANDARDS.md`, `lecture-template.md`, `lecture-script-template.md` from `.claude/skills/shared/`.
2. Read and follow the full `/review-lecture` skill at `.claude/skills/review-lecture/SKILL.md`.
3. Apply it to lecture `$0`.
4. Return a structured PASS/FAIL report by component with specific fix instructions.
5. If all components pass, write `$0/README.md`.
---
**[END AGENT PROMPT]**

**If the review returns any FAIL items:** fix them with `Edit`, re-verify, proceed.

---

## PHASE 7.5: Update Lecture Coverage Registry

Read `$0/[LECTURE_ID]-lecture.md` and `$0/[LECTURE_ID]-report.md`. Extract:
- **Concepts Taught** — from the Part headers and `### What is X?` sections
- **Library Assets Used** — every asset name that appears in an embed filename's provenance (recovered from `animations/*.py` imports)
- **Animations Produced** — one-line summary per clip

Then append to `LECTURE_COVERAGE.md` (create with header if missing):

```markdown
# Lecture Coverage Registry

Tracks what each completed lecture taught. The `/create-lecture` skill reads this
before researching a new lecture to avoid re-teaching covered concepts.

**To approve a lecture:** change its Status in `SYLLABUS.md` from `Draft` to `Approved`.

---

## Lecture $0 — [TOPIC_TITLE]

**Status:** Draft
**Completed:** [today's date]

### Concepts Taught
- ...

### Library Assets Used
- CPU, Register, Cache, ...

### Animations Produced
1. cpu-intro — [one-line summary]
2. ...
```

Append via Write / Edit. Never overwrite existing lecture sections.

---

## PHASE 8: Commit and Push

```bash
git remote -v
```
Expected: `origin → git@github.com:Beehive-Advisors/anyone-can-code.git`

Detect current branch:
```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
```

Update `SYLLABUS.md` — set Status from empty to `Draft` for this row:

```bash
python3.12 - <<'PYEOF'
LECTURE_ID = '$0'
path = 'SYLLABUS.md'
lines = open(path).read().splitlines()
out, changed = [], False
for line in lines:
    cols = [c.strip() for c in line.split('|')]
    if len(cols) >= 6 and cols[2] == LECTURE_ID and cols[4] == 'Demo / Animation' and cols[5] == '':
        cols[5] = 'Draft'
        line = '| ' + ' | '.join(cols[1:6]) + ' |'
        changed = True
    out.append(line)
if changed:
    open(path, 'w').write('\n'.join(out) + '\n')
    print('SYLLABUS.md: Lecture', LECTURE_ID, 'Status -> Draft')
else:
    print('WARNING: could not update SYLLABUS for', LECTURE_ID)
PYEOF
```

Stage and commit:
```bash
git add $0/                           # lecture folder
git add LECTURE_COVERAGE.md SYLLABUS.md .gitignore
# Note: $0/animations/*.mp4 is ignored via .gitignore — verify it's not staged
git status
```

If any `.mp4` is about to be committed: `git rm --cached $0/animations/*.mp4` and fix `.gitignore`.

```bash
git commit -m "Add Lecture $0: [TOPIC_TITLE]"
git push origin $CURRENT_BRANCH
```

On success, print:
- Lecture path
- Animations produced (count + names)
- If `UPLOAD_DEFERRED=true`: "MP4 upload deferred — run Phase 6g manually once beehive-dev PR #49 is merged and videos.tail581af8.ts.net is live."
- Any SKIPPED_ANIMATIONS
- Next step: "Record your voiceover while reading `$0/[LECTURE_ID]-lecture.md`; animations play inline as you reach each SHOW-ANIMATION."

---

## Error Reference

| Situation | Action |
|-----------|--------|
| Lecture file already exists | Stop — warn user |
| Section not in SYLLABUS.md or Format != Demo / Animation | Stop — tell user |
| Asset library not installed | Auto-install via uv |
| Animation generation fails after 2 retries | Surface full error, ask user |
| Same animation regenerated >5 times | Pause — suggest edit or skip |
| Cluster pod not reachable for upload | Defer upload, note `UPLOAD_DEFERRED` |
| Git push rejected | Report, tell user to `git pull --rebase` |
