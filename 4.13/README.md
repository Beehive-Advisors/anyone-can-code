# Lab 4.13 — Speaking HTTP by Hand

Proves that HTTP is plain, human-readable text by having students craft a raw HTTP request using `nc` (netcat) as a TCP pipe, then use `curl -v` to annotate the same exchange, send POST requests with JSON and form data, and work with HTTP status codes programmatically.

## Prerequisites

- **Lecture 4.12** — HTTP and the Request-Response Model
- **Lab 4.11** — Digging into DNS

## Setup

No installation required on macOS — `curl` and `nc` are built in.

On Linux/WSL:
```bash
sudo apt install curl netcat
```

Verify both tools are present:
```bash
curl --version
nc -h 2>&1 | head -1
```

## Files

| File | Description | How to run |
|------|-------------|-----------|
| `http_demo.sh` | Demo script: raw nc request, curl -v annotation, POST requests, status code loop | `bash http_demo.sh` |
| `4.13-lab.md` | Student lab — four parts with exercises and solutions | Read in VS Code or GitHub |
| `4.13-script.md` | Instructor recording script — SPEAK/TYPE/OUTPUT/EXPLAIN beats | Reference during recording |
| `4.13-code-walkthrough.md` | Code walkthrough script — line-by-line explanation of `http_demo.sh` | Reference during walkthrough recording |
| `4.13-report.md` | Research report — background, sources, and lab design decisions | Reference |

## Time estimate

~45 minutes
