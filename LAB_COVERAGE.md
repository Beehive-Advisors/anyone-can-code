# Lab Coverage Registry

This file tracks what each completed lab taught. The `create-lab` skill reads this before researching a new lab to avoid re-teaching covered concepts. The `review-lab` skill reads it to check for course overlap.

**To approve a lab:** change its Status in `SYLLABUS.md` from `Draft` to `Approved`.

---

## Lab 1.5 — Seeing the Machine

**Status:** Draft
**Completed:** 2026-04-20

### Concepts Taught
- Machine architecture and CPU identity
- Core counts and cache sizes
- Memory as page-based accounting
- Storage layout and volume hierarchy
- Files as raw bytes
- Converting between decimal, binary, hexadecimal, and text

### Tools and Commands Demonstrated
- `uname -m` — reports machine architecture
- `sysctl` — reads kernel-maintained hardware and memory facts on macOS
- `vm_stat` — shows virtual memory counters as page statistics on macOS
- `diskutil list` — lists disks, containers, and volumes on macOS
- `xxd -g 1` — shows file bytes in hexadecimal
- `xxd -b` — shows file bytes in binary
- `python3 -c` — runs short conversion snippets directly from the terminal
- `bin()` and `hex()` — format integers in binary and hexadecimal
- `int(text, base)` — parses text in a specific base
- `ord()` and `chr()` — convert between characters and code points

### External Services Used
- None

### Student Exercises
1. Convert cache sizes from bytes into KiB and MiB.
2. Compute wired memory in MiB from page counts.
3. Change a text file and observe the byte sequence change.
4. Convert the character `e` into a code point and hexadecimal.
