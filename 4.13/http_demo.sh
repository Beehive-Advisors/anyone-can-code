#!/usr/bin/env bash
# http_demo.sh — Speaking HTTP by Hand
#
# Shows that HTTP/1.1 is plain, human-readable text. You can compose a valid
# HTTP request yourself and send it directly using nc (netcat) as a raw TCP pipe.
#
# Run: bash http_demo.sh
#
# Requirements:
#   curl  — macOS: built-in  |  Linux/WSL: sudo apt install curl
#   nc    — macOS: built-in  |  Linux/WSL: sudo apt install netcat


echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "SECTION A — HTTP Is Just Text"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "An HTTP/1.1 GET request is plain, human-readable text."
echo "Every request has exactly three parts:"
echo ""
echo "  GET /path HTTP/1.1           request line  (method, path, version)"
echo "  Host: example.com            headers       (one per line, colon-separated)"
echo "  Connection: close"
echo "                               blank line    (signals: headers are done)"
echo ""
echo "The blank line is required by the HTTP spec (RFC 9112)."
echo "Without it, the server keeps waiting for more headers — the connection hangs."
echo ""
echo "Sending that exact request to info.cern.ch port 80 via nc ..."
echo "(info.cern.ch is the original WWW server at CERN where the web was invented)"
echo "(nc is a raw TCP pipe — no HTTP library, no magic, just text over a socket)"
echo ""

# Send a raw HTTP/1.1 GET request to info.cern.ch port 80
# printf sends true CRLF (\r\n) after each header — required by the HTTP spec
# Connection: close prevents nc hanging on HTTP/1.1 keep-alive
# -w 5: exit after 5 seconds of inactivity (safety timeout)
printf 'GET / HTTP/1.1\r\nHost: info.cern.ch\r\nConnection: close\r\n\r\n' \
  | nc -w 5 info.cern.ch 80

echo ""
echo "─── What you just saw ───────────────────────────────────────────"
echo "Line 1:   status line  — HTTP version + three-digit code + reason phrase"
echo "Lines 2+: response headers — Server, Content-Length, Content-Type ..."
echo "Blank:    end of headers"
echo "Rest:     body — the actual HTML page"
echo ""


echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "SECTION B — Annotated HTTP: curl -v"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "curl -v annotates the conversation line by line:"
echo ""
echo "  *  connection events  (DNS lookup, TCP handshake)"
echo "  >  text YOUR computer sent  (the HTTP request)"
echo "  <  text the SERVER sent back (the HTTP response headers)"
echo ""
echo "Running: curl -v http://info.cern.ch ..."
echo ""

# -v: verbose (annotated output)  -s: no progress bar
# -o /dev/null: discard body      2>&1: curl writes -v to stderr; merge here
curl -v -s -o /dev/null http://info.cern.ch 2>&1

echo ""
echo "The > block above IS the HTTP request — the same text nc sent in Section A."
echo "The < block IS the HTTP response headers — the same text nc received."
echo ""


echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "SECTION C — POST: Sending Data to the Server"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "GET fetches data. POST sends it."
echo "The data travels in the body — the bytes after the blank line."
echo ""
echo "httpbin.org/post echoes the full request back as JSON."
echo "Look at the 'headers' field — it shows what curl sent."
echo ""
echo "--- JSON POST ---"
echo "(must set Content-Type manually — curl does not default to JSON)"
echo ""

# -H sets a custom header
# -d sets the request body (implies POST — no -X POST needed)
curl -s https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name": "alice", "age": 30}'

echo ""
echo ""
echo "--- Form data POST (what HTML forms submit) ---"
echo "(no -H needed: curl defaults to application/x-www-form-urlencoded)"
echo ""

curl -s https://httpbin.org/post \
  -d "username=alice&city=boston"

echo ""


echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "SECTION D — Status Codes: The Server's Verdict"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Every HTTP response begins with a three-digit status code."
echo "The first digit is the category:"
echo ""
echo "  2xx = success            3xx = redirect (go somewhere else)"
echo "  4xx = client error       5xx = server error"
echo ""
echo "httpbin.org/status/N returns exactly status code N. Trying several:"
echo ""

# -o /dev/null: discard body
# -w "%{http_code}": print just the status code after the transfer
for code in 200 201 301 400 404 500; do
  received=$(curl -s -o /dev/null -w "%{http_code}" "https://httpbin.org/status/${code}")
  echo "  Requested ${code}  →  received ${received}"
done

echo ""
echo "--- curl exit code vs HTTP status ---"
echo ""
echo "curl exits 0 even when the server returns 404 or 500."
echo "The exit code means: did the network transfer complete?"
echo "It does NOT mean: did the server accept the request?"
echo ""

# curl -s: silent  -o /dev/null: discard body
curl -s -o /dev/null "https://httpbin.org/status/404"
echo "curl exit code after a 404 response: $?"

echo ""
echo "Add --fail to exit non-zero on 4xx/5xx:"
echo ""

curl -s --fail "https://httpbin.org/status/404" -o /dev/null 2>/dev/null
FAIL_EXIT=$?
echo "curl exit code with --fail on 404: ${FAIL_EXIT}  (non-zero = server returned error)"
echo ""
