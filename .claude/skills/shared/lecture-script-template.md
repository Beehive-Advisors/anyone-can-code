# Lecture Script Template

Lecture scripts are distinct from lab scripts:

- **Lab scripts** are terminal screencasts: `SPEAK / TYPE / OUTPUT / EXPLAIN`, dual-platform, one file per OS.
- **Lecture scripts** are animation screencasts: `SPEAK / SHOW-ANIMATION / EXPLAIN`, single file, no platform split.

This file is the authoritative format for the **instructor-facing** shooting script that pairs with `[ID]-lecture.md`. In practice, for lectures, the lecture markdown IS the shooting script — there is no separate `-script.md` because there is no terminal being filmed. The instructor reads the SPEAK blocks into a microphone while the animations play in the edit.

## File identity

There is only one lecture file per section: `[ID]-lecture.md`. Unlike labs (which produce `-script-macos.md` AND `-script-linux.md`), a lecture does not need platform variants. The same file is both the student-facing reference (if ever published) and the instructor's teleprompter.

## Beat labels

- **SPEAK** — spoken narration, verbatim. Markdown blockquote, italics optional for emphasis only.
- **SHOW-ANIMATION** — an inline animation. Before generation: a `<!-- ANIMATE: ... -->` comment. After generation: the `[![gif](path)](mp4-url)` embed.
- **EXPLAIN** — 1–3 sentences pointing at specific visual moments in the animation that just played. Not a restatement of SPEAK.

**Do not use** `TYPE`, `OUTPUT`, `DEMO`, `RUN`, or any lab-script beat labels. Those have no meaning in a lecture.

## Recording hints (end of file, optional)

Optional trailing section with instructor notes:

```markdown
## Recording Notes

- **Pacing:** most animations are 4-8 seconds; pause 0.5s after each before continuing SPEAK.
- **Emphasis moments:** mark words or phrases in the SPEAK that should carry stress — bold them.
- **Retakes welcomed:** narration is re-recordable; animations should be approved before recording starts.
```

## The feedback loop (for the skill author, not the template)

During animation generation, each rendered clip is shown to the user in the terminal. The user responds with (a)pprove / (r)egenerate / (s)kip / (e)dit. See `create-lecture/SKILL.md` Phase 6 for the exact protocol.
