# Lab Coverage Registry

This file tracks what each completed lab taught. The `create-lab` skill reads this before researching a new lab to avoid re-teaching covered concepts. The `review-lab` skill reads it to check for course overlap.

**To approve a lab:** change its Status in `SYLLABUS.md` from `Draft` to `Approved`.

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
