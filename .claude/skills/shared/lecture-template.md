# Lecture Template

This file is the authoritative format for `[ID]-lecture.md` — the lecture script that contains inline Manim animations. It is the lecture analog of `lab-template.md`.

**A lecture is different from a lab.** Labs are hands-on terminal work with dual macOS/Linux tracks. Lectures are narration + animated visuals; they have **no platform tracks** because the viewer is watching a recorded screencast, not typing along. The file is a screencast shooting script from which the instructor reads narration while animations play on screen.

## File header

```markdown
# Lecture [ID] — [Lecture Title]

**Section:** [Course section]
**Prerequisites:** [prior lectures/labs, or "None"]
**Length target:** [~N minutes spoken]
**Animations:** [N animations]
```

No `Files:` line. No `Pick your track` section. No platform toggles.

## Section order (top to bottom)

1. `## Learning Objectives` — 3-5 numbered future-tense outcomes ("By the end, you'll understand...")
2. `## Opening Hook` — SPEAK + optional SHOW-ANIMATION that grabs attention before the concept is named
3. `## Part 1 — [Concept Name]` (repeated per concept)
4. `## Putting It Together` — synthesis beat
5. `## Outro` — one-line closer and preview of the next lecture
6. `## Further Reading` — ≥3 links (mirror the lab "Further Reading" rule)

## Part anatomy

Each `## Part N` follows exactly this beat order:

```markdown
## Part N — [Concept Name]

### What is [concept]?

**SPEAK**
> "First-principles narration. Start with the problem, then name the concept. Identical rule to lab intros — no jargon before it's defined."

**SHOW-ANIMATION**
[![concept-name](./animations/concept-name.gif)](https://videos.tail581af8.ts.net/[id]/concept-name.mp4)

**EXPLAIN**
> "1–3 sentences pointing at specific moments in the animation."

### How it works

[Repeat SPEAK / SHOW-ANIMATION / EXPLAIN as many times as the Part needs.
Each animation is one discrete beat — one idea per animation.]

### Why it matters

**SPEAK**
> "Tie back to what the viewer cares about — the next layer up the stack, or a real-world consequence."
```

## Animation placeholders (pre-generation)

**During script drafting, before animations are rendered**, each SHOW-ANIMATION beat is a placeholder comment:

```markdown
**SHOW-ANIMATION**
<!-- ANIMATE: "A 4-core CPU appears, one core lights up in yellow and a short instruction pointer
runs through it" {name: cpu-fetch, assets: [CPU, Register]} -->
```

The placeholder has three fields in the comment:
- **Prompt** — natural-language description passed to `/animate`. Always wrapped in quotes.
- **`name:`** — stable slug for the animation file (`cpu-fetch.mp4`, `cpu-fetch.gif`, `cpu-fetch.py`).
- **`assets:`** — registry asset names the animation MUST use. Each name is verified against `registry.json` before the animation is generated. If any name is missing, the generation phase pauses and writes `proposed_new_assets.md` for approval.

**After generation**, the skill replaces the placeholder with the rendered embed (GIF preview + mp4 click-through):

```markdown
**SHOW-ANIMATION**
[![cpu-fetch](./animations/cpu-fetch.gif)](https://videos.tail581af8.ts.net/1.4/cpu-fetch.mp4)
```

## Rules

- **SPEAK / SHOW-ANIMATION / EXPLAIN are the only beat labels.** Every prose paragraph sits under one of these three headers. No unlabeled prose.
- **SPEAK is spoken verbatim.** Write it the way the instructor will say it. No "the instructor will explain…"; write the actual sentence.
- **One idea per SHOW-ANIMATION.** Don't stack three animations with no narration between.
- **EXPLAIN points at specific visual moments.** "Notice the yellow highlight — that's the instruction moving from L1 into the register." Not "let me explain this animation."
- **Every `assets:` name must appear in `registry.json`.** The asset library is the source of truth for visual vocabulary; lectures cannot drift away from it.
- **No platform tracks.** Direct-typing, dual-`<details>`, `🍎 / 🐧` emojis — none of that. Those are lab conventions.
- **Length discipline.** Most Parts have 3-6 animation beats; most Parts are 150-300 words of SPEAK total. If a Part needs more, it's probably two Parts.
- **Embed pattern is fixed.** `[![name](./animations/name.gif)](VIDEO_BASE_URL/[id]/name.mp4)` — GIF committed to the repo, mp4 hosted on the pod. Change nothing about this pattern; the `VIDEO_BASE_URL` config is the one swappable piece.
