#!/usr/bin/env bash
# http_status_cookies_demo.sh — HTTP status codes, redirects, and cookie lifecycle
#
# What this shows:
#   - Status codes as data: 200, 404, 500 — what the first digit means
#   - Redirect behavior: curl stops at a 302 without -L, follows with -L
#   - Cookie lifecycle: server sets a cookie, you save it, you send it back
#   - HEAD request: headers only, no body download
#
# Run:
#   bash http_status_cookies_demo.sh

set -e

# Clean up any leftover cookie jar from a previous run
COOKIE_JAR="$(dirname "$0")/cookies.txt"
rm -f "$COOKIE_JAR"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION A — Status code gallery"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  Every HTTP response starts with a 3-digit code."
echo "  The first digit tells you the category — no body needed."
echo "  -s -o /dev/null -w \"%{http_code}\" prints just the code."
echo ""

# httpbin /status/NNN returns exactly that status code
echo "  200 (Success):"
echo "  $(curl -s -o /dev/null -w '%{http_code}' https://httpbin.org/status/200) — 2xx means the request succeeded"

echo ""
echo "  201 (Created — POST created a new resource):"
echo "  $(curl -s -o /dev/null -w '%{http_code}' https://httpbin.org/status/201) — 2xx still, but signals something was made"

echo ""
echo "  301 (Moved Permanently):"
echo "  $(curl -s -o /dev/null -w '%{http_code}' https://httpbin.org/status/301) — 3xx means redirect: look at the Location header"

echo ""
echo "  404 (Not Found):"
echo "  $(curl -s -o /dev/null -w '%{http_code}' https://httpbin.org/status/404) — 4xx means YOUR request had a problem"

echo ""
echo "  500 (Internal Server Error):"
echo "  $(curl -s -o /dev/null -w '%{http_code}' https://httpbin.org/status/500) — 5xx means the SERVER had a problem"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION B — Redirect: stopping vs following"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  Without -L, curl shows the 302 response and stops."
echo "  The server's Location header tells you where to go next —"
echo "  but curl does not follow it automatically."
echo ""
echo "  --- Without -L (curl stops at the redirect) ---"
curl -v -s -o /dev/null https://httpbin.org/redirect/1 2>&1

echo ""
echo "  --- With -L (curl follows the redirect automatically) ---"
echo "  Watch for two separate request/response cycles in the > and < lines."
echo ""
curl -v -s -o /dev/null -L https://httpbin.org/redirect/1 2>&1

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION C — Cookie lifecycle: set, store, send"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  HTTP is stateless — the server forgets you after each request."
echo "  Cookies are the workaround: the server says 'remember this text'."
echo "  Your client stores it and sends it back on every future request."
echo ""

echo "  Step 1: Ask the server to set a cookie."
echo "  -L follows the redirect; -c saves cookies to a file."
echo ""
# /cookies/set returns a 302 redirect; -L follows it
# -c writes the cookie jar (Netscape format) to a file
curl -s -L -c "$COOKIE_JAR" "https://httpbin.org/cookies/set?user=alice&role=student"
echo ""

echo "  Step 2: Look at the cookie jar file curl saved:"
echo ""
cat "$COOKIE_JAR"
echo ""

echo "  Step 3: Send those cookies back to the server."
echo "  httpbin /cookies echoes back whatever cookies it received."
echo ""
# -b reads from the cookie jar and adds a Cookie: header to the request
curl -s -b "$COOKIE_JAR" https://httpbin.org/cookies
echo ""

echo "  The server received the same cookie values it set in Step 1."
echo "  This is how login sessions work — the server set a session ID,"
echo "  you stored it, and now every request proves it is still you."

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION D — HEAD request: check status without downloading the body"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "  HEAD is like GET but the server sends headers only, no body."
echo "  Useful for checking whether a resource exists or reading metadata"
echo "  without downloading potentially large content."
echo ""
echo "  --- HEAD request to httpbin (just headers, no body) ---"
curl -s -I https://httpbin.org/get
echo ""
echo "  --- Contrast: same URL with GET, showing Content-Length header ---"
echo "  Status code only (GET downloads body, we discard it):"
echo "  $(curl -s -o /dev/null -w 'Status: %{http_code}  Size: %{size_download} bytes' https://httpbin.org/get)"
echo ""
echo "  HEAD returned the same Content-Length with zero bytes downloaded."

# Clean up the cookie jar
rm -f "$COOKIE_JAR"
