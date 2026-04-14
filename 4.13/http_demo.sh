#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Lab 4.13 — Speaking HTTP by Hand
# Run: bash http_demo.sh
#
# What this script does: makes real HTTP requests against httpbin.org and
# example.com, printing the raw headers and annotating what each part means.
# Section E shows the same thing with nc — no library, just text over TCP.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "SECTION A — Basic GET: reading the raw HTTP conversation"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "curl -v shows you exactly what's happening on the wire:"
echo "  Lines starting with *  =  curl metadata (DNS, TCP connection, TLS)"
echo "  Lines starting with >  =  headers WE sent to the server"
echo "  Lines starting with <  =  headers the SERVER sent back"
echo ""
echo "─── Request to example.com ───────────────────────────────────────────"

# -v shows all headers; -s suppresses the progress bar; 2>&1 merges
# stderr (where -v output goes) into stdout so we see everything together
curl -v -s http://example.com/ 2>&1

echo ""
echo "─── Same request, but print only the status code ─────────────────────"

# -o /dev/null throws away the body; -w prints what we ask for after
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://example.com/

echo ""
echo "Notice the > blank line after the headers — that blank line is the"
echo "CRLF separator. The server won't process the request until it sees it."


echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "SECTION B — Response Codes: 200, 301, 404"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "─── 200 OK ───────────────────────────────────────────────────────────"

curl -s -o /dev/null -w "Status: %{http_code}  →  %{url_effective}\n" \
  http://httpbin.org/get

echo ""
echo "─── 301 Redirect — WITHOUT -L (curl stops at the redirect) ──────────"

# grep filters to just the * > < lines so output fits on screen
curl -v -s -o /dev/null http://httpbin.org/status/301 2>&1 \
  | grep -E "^[*<>]"

echo ""
echo "  ↑ See the 'location:' header? That's where the server is sending you."
echo "  Without -L, curl shows you the 301 and stops. With -L it follows."

echo ""
echo "─── 301 Redirect — WITH -L (curl follows it automatically) ──────────"

curl -s -o /dev/null \
  -w "Final status: %{http_code}  →  final URL: %{url_effective}\n" \
  -L http://httpbin.org/status/301

echo ""
echo "─── 404 Not Found ────────────────────────────────────────────────────"

curl -s -o /dev/null -w "Status: %{http_code}\n" http://httpbin.org/status/404


echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "SECTION C — POST: sending data to the server"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "─── POST with a JSON body ────────────────────────────────────────────"
echo ""
echo "Watch the > section: you'll see Content-Type and Content-Length headers"
echo "that GET requests don't have. That's how the server knows what we sent."
echo ""

# -X POST sets the method; -H adds a header; -d sets the body
# httpbin.org /post echoes back what it received as JSON — great for learning
curl -v -s \
  -X POST http://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","course":"Anyone Can Code"}' \
  2>&1

echo ""
echo "─── POST with form data (URL-encoded, like an HTML form submit) ──────"
echo ""

# Without -H, -d defaults to Content-Type: application/x-www-form-urlencoded
# Note how the Content-Type changes compared to the JSON POST above
curl -s \
  -X POST http://httpbin.org/post \
  -d "username=alice&message=Hello+World" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('Content-Type sent:', d['headers']['Content-Type']); print('Form data received:', json.dumps(d['form'], indent=2))"


echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "SECTION D — Cookies: how servers remember you"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "─── Step 1: Server sends a Set-Cookie header ─────────────────────────"
echo ""
echo "httpbin.org /cookies/set?name=value returns a 302 redirect with"
echo "a Set-Cookie header. Let's see the headers before following it."
echo ""

# Without -L, we see the 302 response and the Set-Cookie header it carries
curl -v -s -o /dev/null http://httpbin.org/cookies/set?flavor=chocolate 2>&1 \
  | grep -E "^[<>]"

echo ""
echo "─── Step 2: Save that cookie to a file, follow the redirect ──────────"
echo ""

# -c saves all Set-Cookie headers to a file in Netscape cookie format
# -L follows the 302 redirect to /cookies
curl -s -c /tmp/lab413_cookies.txt \
  "http://httpbin.org/cookies/set?flavor=chocolate" \
  -L -o /dev/null

echo "Cookie file contents:"
cat /tmp/lab413_cookies.txt

echo ""
echo "─── Step 3: Send the cookie back on the next request ─────────────────"
echo ""
echo "Watch the > section: curl adds 'Cookie: flavor=chocolate' automatically"
echo "because it's in the cookie file for this domain."
echo ""

# -b reads cookies from the file and sends them as Cookie: headers
curl -v -s -b /tmp/lab413_cookies.txt "http://httpbin.org/cookies" 2>&1

echo ""
echo "─── Inline cookie (no file needed) ───────────────────────────────────"
echo ""

curl -v -s -b "flavor=chocolate" "http://httpbin.org/cookies" 2>&1 \
  | grep -E "^[<>]|cookies"

# Cleanup
rm -f /tmp/lab413_cookies.txt


echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "SECTION E — Raw HTTP with nc: no library, just text over TCP"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "curl does the same thing you're about to do, but automates it."
echo "nc opens a raw TCP connection. We type the request by hand."
echo ""
echo "─── Scripted version (same as typing it manually) ────────────────────"
echo ""
echo "Sending this request over a raw TCP socket to example.com:80:"
echo ""
echo "  GET / HTTP/1.0"
echo "  Host: example.com"
echo "  [blank line]"
echo ""

# printf sends the exact bytes we want (including \r\n CRLF endings)
# HTTP requires \r\n, not just \n — printf handles this explicitly
# sleep 3 keeps stdin open long enough for the server to send its response
# (macOS BSD nc closes the socket very fast when stdin hits EOF)
(printf "GET / HTTP/1.0\r\nHost: example.com\r\n\r\n"; sleep 3) | nc example.com 80

echo ""
echo "─── Why HTTP/1.0 and not HTTP/1.1? ───────────────────────────────────"
echo ""
echo "HTTP/1.1 keeps the connection open after the response (keep-alive)."
echo "The server sends the response, then waits for more requests."
echo "nc would just sit there. HTTP/1.0 tells the server: close when done."
echo ""
echo "─── Interactive exercise instructions ────────────────────────────────"
echo ""
echo "  macOS:  nc -c example.com 80"
echo "  Linux:  nc example.com 80"
echo ""
echo "  Then type each line and press Enter:"
echo "    GET / HTTP/1.0"
echo "    Host: example.com"
echo "    [press Enter one more time — this is the blank line]"
echo ""
echo "  The -c flag on macOS converts your Enter (LF) to CRLF."
echo "  HTTP requires CRLF. Most servers are lenient, but nc -c is correct."
echo ""
echo "─── Bonus: nc against a local Python server ──────────────────────────"
echo ""
echo "  Terminal 1:  python3 -m http.server 8080"
echo "  Terminal 2:  nc -c 127.0.0.1 8080"
echo "               GET / HTTP/1.0"
echo "               Host: 127.0.0.1"
echo "               [blank line]"
echo ""
echo "  Terminal 1 will print the log line when your request arrives."
echo "  You can see both sides of the HTTP conversation at once."
