# Lab 4.13 — Speaking HTTP by Hand

Students use `curl -v` and `nc` (netcat) to make the invisible HTTP conversation visible — reading raw headers, sending POST requests, inspecting status codes and cookies, and typing a complete HTTP request by hand over a raw TCP socket.

## Prerequisites

- Lab 4.11 (DNS)
- Lecture 4.12 (HTTP and the Request-Response Model)
- `curl` installed (pre-installed on macOS and most Linux distributions)
- `nc` (netcat) installed (pre-installed on macOS and most Linux distributions)

## Setup

```bash
cd 4.13
curl --version
nc -h 2>&1 | head -1
```

If either tool is missing:

**macOS:** `brew install curl netcat`
**Linux / WSL:** `sudo apt install curl netcat-openbsd`

## Files

| File | What it does | How to run |
|------|-------------|------------|
| `http_curl_demo.sh` | Demonstrates `curl -v` (verbose HTTP conversation), the stderr/stdout split, form POST, and JSON POST | `bash http_curl_demo.sh` |
| `http_status_cookies_demo.sh` | Demonstrates status codes (200/201/301/404/500), redirect behavior, cookie lifecycle, and HEAD requests | `bash http_status_cookies_demo.sh` |
| `http_nc_demo.sh` | Demonstrates raw HTTP/1.0 and HTTP/1.1 requests via `nc`, nc as a listening server, and curl-vs-nc comparison | `bash http_nc_demo.sh` |
| `4.13-lab.md` | Student lab handout | Open in editor |
| `4.13-script.md` | Instructor screencast script | Open in editor |
| `4.13-code-walkthrough.md` | Instructor VS Code walkthrough script | Open in editor |
| `4.13-report.md` | Research report | Open in editor |

## Time

~60 minutes

## Notes

- Parts 1–3 use one terminal window. Part 4 exercise requires **two terminal windows open simultaneously**: one runs `nc -l 8080` as a server, the other runs `curl` as the client.
- `http_nc_demo.sh` uses port 18080 for the automated nc-as-server section. That port must be free before running the script.
- All three demo scripts connect to external hosts (`httpbin.org`, `httpforever.com`). An internet connection is required.
