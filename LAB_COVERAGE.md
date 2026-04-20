# Lab Coverage Registry

This file tracks what each completed lab taught. The `create-lab` skill reads this before researching a new lab to avoid re-teaching covered concepts. The `review-lab` skill reads it to check for course overlap.

**To approve a lab:** change its Status in `SYLLABUS.md` from `Draft` to `Approved`.

---

## Lab 1.5 — Seeing the Machine

**Status:** Draft
**Completed:** 2026-04-20

### Concepts Taught
- CPU introspection: architecture (x86_64 vs arm64), physical vs logical cores, hyperthreading/SMT
- Cache hierarchy on real hardware: L1 vs L2 vs L3 sizes in bytes; per-core vs per-cluster scope on Apple Silicon
- OS-level hardware discovery mechanism: Linux `/proc/cpuinfo` + `/sys/devices/system/cpu/` vs macOS `sysctl` MIB
- RAM: total capacity in bytes, `MemFree` vs `MemAvailable`, `vm_stat` page counts × page size
- Storage layers: physical device vs partition/volume vs mount point; APFS containers on macOS
- `xxd` hex dump format: offset column, hex pairs, ASCII gutter; printable vs control characters (`.` for non-printable)
- `xxd -b` binary view: each byte as 8 literal bits
- File-format magic bytes / signatures (PNG's `89 50 4e 47 0d 0a 1a 0a`)
- Number bases in Python: `bin()`/`hex()`/`int(s, base)`/`ord()`/`chr()` and f-string format specs `:02x` and `:08b`
- `bytes` objects: `.hex()` and `bytes.fromhex()` as the programmatic equivalent of `xxd`/`xxd -r`
- Cross-platform shell scripting with `uname` OS detection + feature-detection via `sysctl -n key >/dev/null 2>&1`

### Tools and Commands Demonstrated
- `lscpu` — CPU summary (Linux); `lscpu | grep -i cache` — cache lines only
- `cat /proc/cpuinfo` — raw CPU info source (Linux)
- `sysctl -n machdep.cpu.brand_string` — CPU brand (macOS)
- `sysctl -n hw.physicalcpu` / `hw.logicalcpu` — core counts (macOS)
- `sysctl -n hw.cachelinesize` — cache line size in bytes (macOS)
- `sysctl -n hw.perflevel0.l1dcachesize` / `hw.perflevel0.l2cachesize` — Apple Silicon cache keys
- `sysctl -n hw.l1dcachesize` / `hw.l2cachesize` / `hw.l3cachesize` — Intel Mac cache keys
- `system_profiler SPHardwareDataType` — prose hardware overview (macOS)
- `free -h` — RAM table (Linux); `cat /proc/meminfo` — raw memory counters
- `sysctl -n hw.memsize` — total RAM in bytes (macOS)
- `sysctl -n hw.pagesize` — page size (macOS)
- `vm_stat` — live memory page counts (macOS)
- `lsblk` — block-device tree (Linux); `lsblk -f` — with FSTYPE/LABEL/UUID
- `diskutil list` — physical disks, APFS containers, volumes (macOS)
- `df -h ~` — free/used space on the partition backing home (cross-platform)
- `xxd file` — default hex dump (offset + hex pairs + ASCII gutter)
- `xxd -c N file` — N bytes per line
- `xxd -b file` — binary dump (8 bits per byte)
- `xxd -l N file` — limit dump to first N bytes
- `printf '\xHH...'` — write arbitrary byte values from the shell (used for PNG signature)
- Bash arithmetic: `$((16#48))` base-16 literals, `$(( (N >> i) & 1 ))` bit extraction
- `uname` — OS detection for branching shell scripts
- `python3.12 -c "expr"` — one-shot Python expression from the shell
- Python: `ord(c)`, `chr(n)`, `hex(n)`, `bin(n)`, `int(s, base)`
- Python f-strings: `{n:02x}` (zero-padded hex), `{n:08b}` (zero-padded binary), `{x!r}` (repr), `{s:<N}` (left-align)
- Python: `b"..."` bytes literal, `.hex()`, `bytes.fromhex()`

### External Services Used
- None — everything runs against local hardware and local files. No network calls, no third-party services.

### Student Exercises
1. Compute the RAM-to-L1-cache ratio using `python3.12 -c "print(RAM / L1)"` with values read from `hardware_demo.sh` output
2. Dump the first 64 bytes of a file of the student's choosing with `xxd -l 64 file` and identify its first two bytes / magic signature
3. Convert the student's own first initial to decimal, hex, and binary on one line using `python3.12 -c "c='X'; print(f'...')"`

---

## Lab 4.13 — Speaking HTTP by Hand

**Status:** Draft
**Completed:** 2026-04-14

### Concepts Taught
- curl -v: reading raw HTTP request/response lines (>, <, * prefixes meaning request sent, response received, and metadata)
- stderr vs stdout split in curl -v output; `2>&1` redirect pattern for piping verbose output
- curl POST: form data (`-d key=value`) with automatic `application/x-www-form-urlencoded` Content-Type
- curl POST: JSON body (`-H "Content-Type: application/json" -d '{...}'`) and how Content-Type changes server parsing
- HTTP status codes: 200, 201, 301, 404, 500 — what each range (2xx, 3xx, 4xx, 5xx) means
- Redirect behavior: `-L` flag to follow 301/302 automatically; without it curl stops at the redirect
- Cookie lifecycle: Set-Cookie header (server → client), Cookie header (client → server)
- curl cookie jar: `-c` to write cookies to a file, `-b` to send cookies from that file on next request
- HTTP/1.0 vs HTTP/1.1: mandatory Host header in 1.1, Connection: close to prevent nc from hanging
- nc (netcat): sending raw bytes over a TCP socket using `printf "GET / HTTP/1.0\r\n\r\n" | nc -w 5 host 80`
- nc as a listening server: `nc -l PORT` to capture raw HTTP requests from a client

### Tools and Commands Demonstrated
- `curl -v` — verbose HTTP conversation (shows >, <, * lines)
- `curl -s -o /dev/null -w '%{http_code}'` — extract status code only, discard body
- `curl -d 'key=value'` — POST with URL-encoded form body
- `curl -H 'Header: value'` — set or override a request header
- `curl -L` — follow HTTP redirects automatically
- `curl -c cookies.txt` / `curl -b cookies.txt` — write/read a Netscape-format cookie jar
- `curl -I` — HEAD request (returns headers only, no body)
- `printf "GET / HTTP/1.0\r\n\r\n" | nc -w 5 host 80` — raw HTTP/1.0 via netcat
- `printf "GET / HTTP/1.1\r\nHost: host\r\nConnection: close\r\n\r\n" | nc -w 5 host 80` — raw HTTP/1.1
- `nc -l PORT` — nc as a listening server to capture what a client sends

### External Services Used
- `httpbin.org` (HTTPS, port 443) — echo server for curl demos; returns JSON showing what it received
- `httpforever.com` (plain HTTP, port 80) — purpose-maintained server for nc demos; never redirects to HTTPS

### Student Exercises
1. Run `curl -v -s -o /dev/null https://httpbin.org/get 2>&1` and identify what >, <, and * lines mean
2. Send a custom header (`X-My-Name: YourName`) and grep the verbose output to confirm it was sent
3. POST JSON to `httpbin.org/post` and observe data under the "json" key (vs "form" for URL-encoded)
4. Type a complete raw HTTP/1.1 request via `nc` to `httpforever.com` port 80 using two terminal windows
