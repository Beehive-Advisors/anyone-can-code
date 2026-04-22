# Lab Coverage Registry

This file tracks what each completed lab taught. The `create-lab` skill reads this before researching a new lab to avoid re-teaching covered concepts. The `review-lab` skill reads it to check for course overlap.

**To approve a lab:** change its Status in `SYLLABUS.md` from `Draft` to `Approved`.

---

## Lab 1.5 — Seeing the Machine

**Status:** Draft
**Completed:** 2026-04-22

### Concepts Taught
- CPU introspection via kernel interfaces (Linux `/proc/cpuinfo` + sysfs pseudo-files; macOS sysctl MIB tree)
- Apple Silicon performance-level split (P-cores vs E-cores, `hw.perflevel0.*` vs `hw.perflevel1.*`)
- CPU cache hierarchy (L1i, L1d, L2, L3 — per-core vs shared)
- Physical RAM total as a kernel-exposed scalar (`hw.memsize` on macOS; `MemTotal` in `/proc/meminfo` on Linux)
- Live memory accounting: Mach pages (macOS `vm_stat`) vs `MemAvailable` heuristic (Linux `free -h`)
- Page size variability (16384 B on Apple Silicon vs 4096 B on Intel)
- APFS container model and synthesized disks (dynamic space sharing between volumes)
- Linux block-device tree (disk → part → LVM/RAID) via sysfs
- `df -h` as the single cross-platform mounted-filesystem view
- Every file is a sequence of bytes; interpretation lives in the program, not the file
- PNG 8-byte magic signature and chunk structure (IHDR, IDAT, IEND)
- Hex + ASCII canonical dump format (three columns: offset, hex pairs, ASCII gloss)
- Base conversion: decimal ↔ hexadecimal ↔ binary as representations of the same integer
- ASCII code points and the bit-5-flip between uppercase and lowercase letters
- Working-directory primitives: `pwd`, `cd` with no argument returns home, `cd -` jumps to previous

### Tools and Commands Demonstrated
- `sysctl -n <name>` — read one macOS MIB entry
- `sysctl hw machdep.cpu | head -20` — dump CPU-related MIB branch
- `sysctl -n hw.memsize` — total RAM in bytes
- `sysctl -n hw.perflevel0.l2cachesize` — P-core L2 size
- `vm_stat | head -12` — Mach virtual-memory page counts
- `diskutil list` — macOS APFS container + volume hierarchy
- `grep -m1 "model name" /proc/cpuinfo` — first model-name line from Linux pseudo-file
- `nproc` — logical CPU count on Linux
- `lscpu` — aggregated Linux CPU summary
- `lscpu | grep "L1d cache"` — extract one cache line
- `grep MemTotal /proc/meminfo` — total RAM in kB on Linux
- `free -h` — Linux memory table with human units
- `free -m | awk '/Mem:/ {print $7 ...}'` — extract available MiB
- `lsblk` — Linux block-device tree
- `lsblk -f` — with filesystem types and UUIDs
- `df -h /` — root filesystem usage (cross-platform)
- `df -h | grep "/System/Volumes/" | wc -l` — count macOS system volumes
- `echo "Hello, world!" > hello.txt` — create a scratch text file
- `xxd <file>` — canonical hex + ASCII dump
- `xxd -l N <file>` — dump first N bytes only
- `xxd sample.png | head -6` — dump with line limit via pipe
- `printf 'A' > a.txt` — write a single byte without trailing newline
- `pwd`, `cd`, `cd -` — working-directory primitives
- `bc` — command-line calculator for byte-to-GiB conversion
- `echo "scale=2; ... / 1073741824" | bc` — divide to gibibytes
- `echo "$(( ... / 1024 )) KiB"` — integer arithmetic in bash
- `python3.12 -c "print(hex(n))"` — decimal to hex
- `python3.12 -c "print(bin(n))"` — decimal to binary
- `python3.12 -c "print(int(s, 16))"` — hex string to int
- `python3.12 -c "print(ord(c))"` — character to code point
- `python3.12 -c "print(chr(n))"` — code point to character
- `python3.12 -c "print(''.join(chr(int(b,16)) for b in [...]))"` — rebuild a string from hex byte list

### External Services Used
- None — the lab runs entirely against local kernel pseudo-files, local binaries, and the shipped `sample.png`.

### Student Exercises
1. (macOS, Part 1) Print the Performance-core L2 cache size in kilobytes using `sysctl -n` and shell arithmetic.
2. (Linux, Part 1) Extract just the `L1d cache` line from `lscpu`'s output with `grep`.
3. (macOS, Part 2) Compute free memory in MiB by multiplying `vm_stat`'s `Pages free` by the page size and dividing by 2^20.
4. (Linux, Part 2) Print the `available` column of `free -m` for the `Mem:` row using `awk`.
5. (macOS, Part 3) Count how many mounted filesystems live under `/System/Volumes/` using `df`, `grep`, and `wc -l`.
6. (Linux, Part 3) Use `lsblk -f` to see filesystem types and identify the root partition's filesystem.
7. (Both, Part 4) Dump single-byte files containing uppercase `A` and lowercase `a`, and explain the one-bit difference.
8. (Both, Part 5) Print the number 255 in decimal, hex, and binary on three lines with a single `python3.12 -c "..."` invocation.

### Shipped Reference Files
- `sample.png` — 80-byte, 16×16-pixel solid-red PNG generated with Python stdlib (`struct` + `zlib`). Deterministic bytes so every student's `xxd sample.png` produces the same five-line output.
