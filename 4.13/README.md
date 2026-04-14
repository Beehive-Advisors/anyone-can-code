# Lab 4.13 — Speaking HTTP by Hand

HTTP is just structured ASCII text sent over a TCP connection. This lab strips away every abstraction — browser, library, framework — and shows students the raw protocol using `curl -v` and `nc`.

## Prerequisites

- Lab 2.11 (curl basics)
- Lab 3.7 (TCP)
- Lab 4.12 (HTTP concepts)

## Setup

```bash
cd 4.13
# No install needed — curl and nc are pre-installed on macOS
# On Ubuntu/WSL: sudo apt install netcat-openbsd
```

## Files

| File | What it does | How to run |
|------|-------------|------------|
| `http_demo.sh` | Demo script: curl -v, status codes, POST, cookies, nc | `bash http_demo.sh` |
| `4.13-lab.md` | Student lab handout | Open in editor |
| `4.13-script.md` | Instructor recording script | Open in editor |
| `4.13-report.md` | Research report and citations | Open in editor |

## Time

~50 minutes

## Notes

Part 5 (nc exercise) requires two terminal windows open simultaneously — one running `python3 -m http.server 8080`, one running nc. The two-terminal note is included in the lab's Setup section. On macOS, use `nc -c` for automatic CRLF conversion. On Linux, use `printf "..." | nc -q 3 hostname port` instead.
