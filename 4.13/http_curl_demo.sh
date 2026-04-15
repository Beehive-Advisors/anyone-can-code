#!/usr/bin/env bash
# http_curl_demo.sh — Reading raw HTTP with curl -v and sending POST requests
#
# What this shows:
#   - What curl -v reveals about the HTTP conversation (>, <, * lines)
#   - How POST sends a body with a Content-Type label
#   - How the same bytes with a different Content-Type are parsed differently
#   - The stdout vs stderr distinction in curl -v output
#
# Run:
#   bash http_curl_demo.sh

set -e

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION A — Without -v vs With -v: revealing the conversation"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  Without -v, curl shows you only the response body:"
echo "  (what your browser shows you — the end result)"
echo ""
echo "  --- Body only ---"
# -s suppresses the progress meter; we only see the JSON response
curl -s https://httpbin.org/get | head -5
echo "  (output continues...)"

echo ""
echo "  With -v, curl shows you the full conversation:"
echo "  > lines = what YOUR machine sent"
echo "  < lines = what the SERVER sent back"
echo "  * lines = curl's own status messages"
echo ""
echo "  --- Full conversation (headers only, body discarded) ---"
# -s suppresses progress meter
# -o /dev/null discards the body so we see only the header conversation
# 2>&1 merges stderr (where -v output lives) into stdout
curl -v -s -o /dev/null https://httpbin.org/get 2>&1

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION B — The stderr gotcha: why piping -v output fails"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  curl -v sends verbose output to STDERR, not STDOUT."
echo "  Piping only captures STDOUT — so grep misses the > and < lines."
echo ""
echo "  --- Fails: piping without 2>&1 ---"
echo "  Command: curl -v -s https://httpbin.org/get | grep 'Host'"
echo "  Result:"
# This intentionally produces no output — that's the demo point
curl -v -s -o /dev/null https://httpbin.org/get 2>/dev/null | grep 'Host' || echo "  (nothing found — the Host line is on stderr, not stdout)"

echo ""
echo "  --- Works: merge stderr into stdout first ---"
echo "  Command: curl -v -s -o /dev/null https://httpbin.org/get 2>&1 | grep 'Host'"
echo "  Result:"
curl -v -s -o /dev/null https://httpbin.org/get 2>&1 | grep 'Host'

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION C — POST with form data: sending a body"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  A POST request carries a body — extra data sent TO the server."
echo "  -d \"key=value\" sets the body and tells curl to POST automatically."
echo "  curl also sets Content-Type: application/x-www-form-urlencoded."
echo ""
echo "  Watch the > lines: you will see Content-Type and Content-Length"
echo "  appear in YOUR outgoing request."
echo ""
echo "  httpbin.org echoes back what it received under \"form\"."
echo ""
# -v shows the full conversation
# The response JSON shows what httpbin received under "form"
curl -v -s https://httpbin.org/post \
  -d "username=alice&city=Portland" 2>&1

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION D — POST with JSON: same structure, different label"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  JSON POST: the body bytes look different but the HTTP structure"
echo "  is identical. The only change in the request headers is:"
echo "  Content-Type: application/json"
echo ""
echo "  httpbin echoes back JSON under \"json\" instead of \"form\"."
echo "  Same TCP bytes going over the wire — completely different"
echo "  behavior because of one header value."
echo ""
# -H overrides the Content-Type header
# Single quotes protect the JSON from shell interpretation
curl -v -s https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "city": "Portland"}' 2>&1
