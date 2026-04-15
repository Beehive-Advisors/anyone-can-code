#!/usr/bin/env bash
# http_nc_demo.sh — HTTP is just text: speaking the protocol by hand with netcat
#
# What this shows:
#   - nc (netcat) as a raw TCP pipe — no HTTP awareness, just bytes
#   - HTTP/1.0 request sent by hand: GET, blank line, server responds
#   - HTTP/1.1 request: same structure but Host header is required
#   - nc as a server: seeing the raw request that curl actually sends
#
# Run:
#   bash http_nc_demo.sh
#
# Note: Sections A, B, D connect to httpforever.com:80 (plain HTTP, no TLS).
#       Section C uses localhost port 18080 (no network required).

set -e

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION A — HTTP/1.0 by hand: the minimal request"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  nc connects a TCP socket to httpforever.com port 80."
echo "  printf sends the HTTP request bytes — no HTTP library involved."
echo ""
echo "  The request is exactly two lines:"
echo "    GET / HTTP/1.0   <-- request-line: method, path, version"
echo "    (blank line)     <-- signals end of headers"
echo ""
echo "  --- Raw server response (every byte, uninterpreted) ---"
echo ""
# printf correctly handles \r\n (CRLF) which HTTP requires
# nc connects, sends the request, and prints whatever the server sends back
# -w 5 times out after 5 seconds so the script does not hang
# head -20 shows headers + start of body (full body is HTML, not relevant here)
printf "GET / HTTP/1.0\r\n\r\n" | nc -w 5 httpforever.com 80 | head -20
echo ""

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION B — HTTP/1.1 by hand: adding the required Host header"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  HTTP/1.1 requires a Host header — without it, compliant servers"
echo "  return 400 Bad Request. This is because one server IP can host"
echo "  many domain names; the Host header tells the server which site"
echo "  you want. Connection: close asks the server to close after"
echo "  responding, so nc exits rather than waiting for another request."
echo ""
echo "  --- HTTP/1.1 raw server response (headers only) ---"
echo ""
# Three parts: request-line, Host header, Connection header, blank line
# head -15 shows just the response headers without the HTML body
printf "GET / HTTP/1.1\r\nHost: httpforever.com\r\nConnection: close\r\n\r\n" \
  | nc -w 5 httpforever.com 80 | head -15
echo ""
echo "  Compare Section A to Section B: HTTP/1.1 response has more headers"
echo "  and the server respected the Connection: close we sent."

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION C — nc as server: reading curl's raw request"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  nc -l 18080 turns nc into a listening TCP server on port 18080."
echo "  Whatever connects is a client — nc shows you the raw bytes"
echo "  that client sent, exactly as they arrived."
echo ""
echo "  Here: curl connects as the client. nc reveals what curl sends."
echo "  This is the same request curl sends to httpbin.org or any server."
echo ""

# Start nc listening in background; write what it receives to a temp file
RAW_REQUEST_FILE="$(mktemp)"

# nc -l 18080 receives data from curl and writes it to the temp file
nc -l 18080 > "$RAW_REQUEST_FILE" &
NC_PID=$!

# Give nc a moment to start listening
sleep 0.3

# curl connects to our nc server; nc will receive the request and exit
# -o /dev/null discards any response body (nc sends none)
# --max-time 2 prevents hanging; || true prevents set -e from exiting
curl -s -o /dev/null --max-time 2 \
  http://localhost:18080/index.html \
  -H "User-Agent: curl-lab-demo" \
  -H "X-Lab: speaking-http-by-hand" \
  2>/dev/null || true

# Wait for nc to finish receiving
sleep 0.3
kill "$NC_PID" 2>/dev/null || true
wait "$NC_PID" 2>/dev/null || true

echo "  --- Raw HTTP request that curl sent to nc ---"
cat "$RAW_REQUEST_FILE"
rm -f "$RAW_REQUEST_FILE"

echo ""
echo "  This is the exact text that curl sends to EVERY server."
echo "  httpbin.org, google.com, your own API — all receive this"
echo "  same formatted text and parse it. HTTP is just text."

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION D — curl -v vs nc: two views of the same conversation"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  curl -v shows the conversation with labels (>, <, *)."
echo "  nc shows the raw bytes with no interpretation."
echo "  Both reveal the same underlying HTTP text — just formatted differently."
echo ""
echo "  --- curl -v view of a GET request to httpforever.com (labeled) ---"
echo ""
# --http1.1 forces HTTP/1.1 so the > lines show plain text (not HTTP/2 frames)
# -o /dev/null discards the body; 2>&1 merges stderr for display
curl --http1.1 -v -s -o /dev/null http://httpforever.com/ 2>&1

echo ""
echo "  --- nc view of the same request (raw bytes, same server) ---"
echo ""
# Same request path, same server, just using nc to send it and show the raw response
printf "GET / HTTP/1.1\r\nHost: httpforever.com\r\nConnection: close\r\n\r\n" \
  | nc -w 5 httpforever.com 80 | head -15
echo ""
echo "  Both tools made the same TCP connection and sent the same HTTP text."
echo "  curl labeled the lines with > and <. nc passed the raw bytes straight through."
echo "  The server did not know or care which tool was on the other end."
