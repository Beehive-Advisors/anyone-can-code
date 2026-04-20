# Lab Coverage Registry

This file tracks what each completed lab taught. The `create-lab` skill reads this before researching a new lab to avoid re-teaching covered concepts. The `review-lab` skill reads it to check for course overlap.

**To approve a lab:** change its Status in `SYLLABUS.md` from `Draft` to `Approved`.

---

## Lab 1.5 — Seeing the Machine

**Status:** Draft
**Completed:** 2026-04-20

### Concepts Taught
- CPU topology: sockets, cores, threads, logical CPUs (nproc / lscpu)
- Simultaneous Multithreading (SMT / Hyper-Threading)
- Cache hierarchy: L1d, L1i, L2, L3 — size, level, shared vs. per-core
- Cache lines (64-byte transfer units)
- RAM vs. disk cache: `available` vs. `free` distinction in Linux memory accounting
- `/proc/meminfo` fields: MemTotal, MemFree, MemAvailable, Buffers, Cached
- Physical memory address ranges and memory blocks (`lsmem`)
- Block devices and disk partitions: disk tree, MAJ:MIN device numbers, partition types
- Files as raw bytes: hex dumps, offset column (hex), ASCII sidebar, non-printable bytes
- Magic numbers: file-type identification from first bytes (ELF `7f 45 4c 46`, Mach-O `ca fe ba be`)
- Number base conversions: decimal ↔ binary ↔ hexadecimal ↔ ASCII
- Python `bytes` object: indexing returns int, `.hex()`, `list()`, `bytes.fromhex()`
- ASCII table design: digit codes 48–57, uppercase 65–90, lowercase 97–122, case-flip bit trick (XOR 0x20)

### Tools and Commands Demonstrated
- `nproc` — count total logical CPUs
- `lscpu` — full CPU topology table
- `lscpu -C` — cache hierarchy table (ONE-SIZE, ALL-SIZE, TYPE, LEVEL)
- `grep -E "^CPU\(s\):|Thread|Core|Socket"` — filter lscpu key fields
- `cat /proc/meminfo | head -10` — raw kernel memory counters in kB
- `free -h` — human-readable memory summary (total, used, free, buff/cache, available)
- `lsmem` — physical memory address ranges and block states
- `lsblk` — disk and partition tree (NAME, MAJ:MIN, SIZE, TYPE, MOUNTPOINTS)
- `xxd filename` — full hex dump (default: 16 bytes/line, 2-byte groups)
- `xxd -g 1 filename` — hex dump with 1-byte groups
- `xxd -l 16 /bin/ls` — first 16 bytes only (magic number inspection)
- `echo "hex" | xxd -r -p` — reverse: hex string → binary file
- `python3 -c "format(n,'08b')"` — decimal → zero-padded binary string
- `python3 -c "format(n,'02x')"` — decimal → zero-padded hex string
- `python3 -c "ord('A')"` — character → ASCII integer
- `python3 -c "chr(65)"` — ASCII integer → character
- `python3 -c "int('01000001', 2)"` — binary string → decimal
- `python3 -c "int('41', 16)"` — hex string → decimal
- `python3 -c "b'Hi!'[0]"` — bytes indexing → integer
- `python3 -c "b'Hi!'.hex()"` — bytes → hex string
- `open('file','rb').read()` — read file as raw bytes
- `sysctl -n machdep.cpu.brand_string` — macOS CPU model (callout)
- `sysctl -n hw.physicalcpu hw.logicalcpu` — macOS CPU counts (callout)
- `sysctl -n hw.memsize` — macOS total RAM in bytes (callout)
- `vm_stat` — macOS page statistics (callout)
- `diskutil list` — macOS disk and partition tree (callout)

### External Services Used
None — entirely local kernel and filesystem inspection.

### Student Exercises
1. Verify the logical CPU formula (sockets × cores × threads = nproc) and convert one cache size to bytes with Python
2. Calculate what percentage of total RAM is currently available using `/proc/meminfo` values in Python
3. Create a file with their first name, xxd it, and verify the first byte's hex code with `hex(ord(...))`
4. Predict the hex code for uppercase 'B', verify with Python, then use XOR 0x20 to convert it to lowercase
