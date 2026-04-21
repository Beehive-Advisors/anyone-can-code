# Lab Coverage Registry

This file tracks what each completed lab taught. The `create-lab` skill reads this before researching a new lab to avoid re-teaching covered concepts. The `review-lab` skill reads it to check for course overlap.

**To approve a lab:** change its Status in `SYLLABUS.md` from `Draft` to `Approved`.

---

## Lab 1.5 — Seeing the Machine

**Status:** Draft
**Completed:** 2026-04-21

### Concepts Taught
- CPU inspection: architecture (x86_64 vs arm64), physical vs logical cores, SMT / Hyper-Threading
- Cache hierarchy on real hardware: L1d / L1i / L2 / L3 sizes; per-core vs cluster-shared; Apple Silicon perf/efficiency tiers
- Apple Silicon peculiarities: `hw.perflevel0.*` keys; no classical L3 on Apple Silicon
- Kernel-as-hardware-registry: Linux `/proc/cpuinfo` + `/sys/devices/system/cpu/` vs macOS `sysctl` MIB
- RAM: total installed (bytes vs kB vs GiB vs GB units distinction), live breakdown categories
- Linux memory categories: MemTotal / MemFree / MemAvailable / Buffers / Cached; why free ≠ available
- macOS memory categories: free / active / inactive / wired down / speculative pages; `vm_stat` page-count units (16 KiB on Apple Silicon)
- Storage layers: physical device → partition / APFS container → mount point; `lsblk` tree on Linux vs `diskutil list` on macOS
- APFS synthesized containers (modern macOS): one physical disk, synthesized second device node, volumes sharing a pool
- `df -h` as the cross-platform "how full is this mount?" command
- Hex dump format: offset / hex pairs / ASCII sidecar; printable vs control bytes (`.` placeholder)
- `xxd -b` binary view: bytes as 8-bit patterns
- File-format magic bytes: PNG signature `89 50 4e 47 0d 0a 1a 0a`; ELF `7f 45 4c 46`; Mach-O `cf fa ed fe`; JPEG `ff d8 ff`
- Number bases in Python: `bin()` / `hex()` / `int(s, base)` / `ord()` / `chr()`
- `bytes` objects: `.hex()` and `bytes.fromhex()` as the programmatic equivalent of `xxd` / `xxd -r`
- Python f-string format specs: `{n:02x}` (zero-padded hex), `{n:08b}` (zero-padded binary)
- ASCII case-toggle bit: upper vs lower differs by exactly `0x20`

### Tools and Commands Demonstrated
- `sysctl -n machdep.cpu.brand_string` — CPU brand (macOS)
- `sysctl -n hw.physicalcpu` / `hw.logicalcpu` — core counts (macOS)
- `sysctl -n hw.perflevel0.l1dcachesize` / `hw.perflevel0.l2cachesize` — Apple Silicon cache keys
- `sysctl -n hw.memsize` — total RAM in bytes (macOS)
- `system_profiler SPHardwareDataType` — prose hardware overview (macOS)
- `vm_stat` — live memory page counts (macOS)
- `diskutil list` — physical disks, APFS containers, volumes (macOS)
- `lscpu` — CPU summary (Linux); `lscpu -C` — cache hierarchy table
- `nproc` — logical CPU count (Linux)
- `free -h` — human-readable memory table (Linux)
- `grep MemTotal /proc/meminfo` / `head -5 /proc/meminfo` — raw kernel memory counters
- `lsblk` — block-device tree (Linux)
- `df -h ~` — free/used space on the partition backing home (cross-platform)
- `echo 'Hello!' > hello.txt` — write a tiny test file (cross-platform)
- `xxd file` — default hex dump (offset + hex pairs + ASCII sidecar)
- `xxd -b file` — binary dump (8 bits per byte)
- `xxd -l N file` — limit dump to first N bytes
- `curl -sO URL` — download a known PNG for signature inspection
- `python3.12 -c "expr"` (macOS) / `python3 -c "expr"` (Linux) — one-shot Python expression
- Python: `ord(c)`, `chr(n)`, `hex(n)`, `bin(n)`, `int(s, base)`
- Python f-strings: `{n:02x}` (zero-padded hex), `{n:08b}` (zero-padded binary), `{c!r}` (repr)
- Python: `b"..."` bytes literal, `.hex()`, `bytes.fromhex()`

### External Services Used
- `libpng.org` (HTTPS, port 443) — single `curl -sO` to download a reference PNG logo for magic-byte inspection in Part 4

### Student Exercises
1. Compute the L2-to-L1 cache ratio using `python3 -c "print(L2 / L1)"` with values read from their own machine
2. Convert total RAM from the OS's native units (bytes on macOS, kB on Linux) into both GiB and GB, showing the 7% marketing mismatch
3. Find which partition backs their home directory using `df -h ~`
4. Hex-dump any file of their choosing with `xxd -l 32` and identify its format from the first few bytes
5. Convert their own first initial to decimal, hex, and binary on one line using a Python one-liner
