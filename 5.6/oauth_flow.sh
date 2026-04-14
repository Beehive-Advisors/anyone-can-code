#!/usr/bin/env bash
# oauth_flow.sh — Walk through the OAuth 2.0 authorization code flow with curl
#
# This script starts oauth_server.py in the background, walks through every
# HTTP step of the authorization code flow, and then shuts the server down.
#
# Run with:
#   cd ~/src/courses/anyone-can-code/5.6
#   source .venv/bin/activate
#   bash oauth_flow.sh

set -e

BASE_URL="http://localhost:5001"
CLIENT_ID="demo-client"
CLIENT_SECRET="demo-secret"
REDIRECT_URI="http://localhost:5001/callback"
STATE="csrf-token-$(date +%s)"

# ─── Start the server in the background ────────────────────────────────────────
echo ""
echo "Starting oauth_server.py in the background..."
python3.12 oauth_server.py > /tmp/oauth_server.log 2>&1 &
SERVER_PID=$!

# Clean up the background server when this script exits (success or failure)
trap "echo ''; echo 'Stopping server (PID $SERVER_PID)...'; kill $SERVER_PID 2>/dev/null; wait $SERVER_PID 2>/dev/null || true; echo 'Server stopped.'" EXIT

# Wait for Flask to be ready
sleep 2

# Quick health check
if ! curl -s "${BASE_URL}/callback" > /dev/null 2>&1; then
    echo "ERROR: Server did not start. Check /tmp/oauth_server.log"
    exit 1
fi

echo "Server is running."


echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 1 — The authorization URL the client builds"
echo "══════════════════════════════════════════════════════════════════════"

# Construct the authorization URL
AUTH_URL="${BASE_URL}/authorize?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=read_profile&state=${STATE}"

echo ""
echo "URL: ${AUTH_URL}"
echo ""
echo "Parameters:"
echo "  response_type=code     → ask for an authorization code (not a token directly)"
echo "  client_id=demo-client  → identifies our application to the auth server"
echo "  redirect_uri=...       → where the server sends the user after they approve"
echo "  scope=read_profile     → the permissions our app is requesting"
echo "  state=${STATE}  → random value we generate for CSRF protection"


echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 2 — Hit /authorize and capture the authorization code"
echo "══════════════════════════════════════════════════════════════════════"

echo ""
echo "curl command:"
echo "  curl -v '${AUTH_URL}'"
echo ""

# Make the request — curl follows the redirect by default unless we tell it not to
# We use --max-redirs 0 to stop at the redirect so we can see the Location header
AUTHORIZE_RESPONSE=$(curl -s -v --max-redirs 0 "${AUTH_URL}" 2>&1 || true)

echo "Response headers:"
echo "${AUTHORIZE_RESPONSE}" | grep "^< " | head -15
echo ""

# Extract the Location header (the redirect back to the callback)
LOCATION=$(echo "${AUTHORIZE_RESPONSE}" | grep -i "^< [Ll]ocation:" | head -1 | sed 's/^< [Ll]ocation: //' | tr -d '\r')
echo "Location header: ${LOCATION}"
echo ""

# Extract the authorization code from the redirect URL
CODE=$(echo "${LOCATION}" | grep -oE 'code=[^&]+' | cut -d'=' -f2)
RETURNED_STATE=$(echo "${LOCATION}" | grep -oE 'state=[^&]+' | cut -d'=' -f2)

echo "Extracted code:  ${CODE}"
echo "Returned state:  ${RETURNED_STATE}"
echo ""

# Verify the state matches what we sent (CSRF check)
if [ "${RETURNED_STATE}" = "${STATE}" ]; then
    echo "State check: PASSED — the response is for our request, not a CSRF attack"
else
    echo "State check: FAILED — state mismatch! Aborting."
    exit 1
fi

echo ""
echo "The browser would now land on /callback?code=...&state=..."
echo "The code travels through the browser (front channel) — short-lived, single-use."
echo "Now the client's backend exchanges it privately (back channel)."


echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 3 — Exchange the code for an access token (back channel POST)"
echo "══════════════════════════════════════════════════════════════════════"

echo ""
echo "curl command:"
echo "  curl -X POST ${BASE_URL}/token \\"
echo "    -d 'grant_type=authorization_code' \\"
echo "    -d 'code=${CODE}' \\"
echo "    -d 'redirect_uri=${REDIRECT_URI}' \\"
echo "    -d 'client_id=${CLIENT_ID}' \\"
echo "    -d 'client_secret=${CLIENT_SECRET}'"
echo ""

# Exchange code for token
TOKEN_RESPONSE=$(curl -s -X POST "${BASE_URL}/token" \
    -d "grant_type=authorization_code" \
    -d "code=${CODE}" \
    -d "redirect_uri=${REDIRECT_URI}" \
    -d "client_id=${CLIENT_ID}" \
    -d "client_secret=${CLIENT_SECRET}")

echo "Token endpoint response:"
echo "${TOKEN_RESPONSE}" | python3.12 -m json.tool 2>/dev/null || echo "${TOKEN_RESPONSE}"
echo ""

# Extract the access token
ACCESS_TOKEN=$(echo "${TOKEN_RESPONSE}" | python3.12 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -z "${ACCESS_TOKEN}" ]; then
    echo "ERROR: Could not extract access_token from response."
    exit 1
fi

echo "Access token: ${ACCESS_TOKEN}"
echo ""
echo "This exchange happened server-to-server. The browser never saw this request."
echo "The access token never appeared in a URL, browser history, or server log."


echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 4 — Use the access token to call the protected resource"
echo "══════════════════════════════════════════════════════════════════════"

echo ""
echo "curl command:"
echo "  curl -H 'Authorization: Bearer ${ACCESS_TOKEN}' ${BASE_URL}/protected"
echo ""

RESOURCE_RESPONSE=$(curl -s -H "Authorization: Bearer ${ACCESS_TOKEN}" "${BASE_URL}/protected")

echo "Protected resource response:"
echo "${RESOURCE_RESPONSE}" | python3.12 -m json.tool 2>/dev/null || echo "${RESOURCE_RESPONSE}"


echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "STEP 5 — Security checks: try to break the protocol"
echo "══════════════════════════════════════════════════════════════════════"

echo ""
echo "--- 5a: Reuse the same authorization code ---"
echo ""
REUSE_RESPONSE=$(curl -s -X POST "${BASE_URL}/token" \
    -d "grant_type=authorization_code" \
    -d "code=${CODE}" \
    -d "redirect_uri=${REDIRECT_URI}" \
    -d "client_id=${CLIENT_ID}" \
    -d "client_secret=${CLIENT_SECRET}")
echo "Response (second use of same code):"
echo "${REUSE_RESPONSE}" | python3.12 -m json.tool 2>/dev/null || echo "${REUSE_RESPONSE}"
echo ""
echo "Authorization codes are single-use — replaying it is rejected."

echo ""
echo "--- 5b: Access the resource without a token ---"
echo ""
NO_TOKEN_RESPONSE=$(curl -s "${BASE_URL}/protected")
echo "Response (no Authorization header):"
echo "${NO_TOKEN_RESPONSE}" | python3.12 -m json.tool 2>/dev/null || echo "${NO_TOKEN_RESPONSE}"
echo ""
echo "Without a Bearer token, the resource server returns 401 Unauthorized."

echo ""
echo "--- 5c: Use a wrong client_secret ---"
echo ""
BAD_SECRET_RESPONSE=$(curl -s -X POST "${BASE_URL}/token" \
    -d "grant_type=authorization_code" \
    -d "code=fake-code-xyz" \
    -d "redirect_uri=${REDIRECT_URI}" \
    -d "client_id=${CLIENT_ID}" \
    -d "client_secret=wrong-secret")
echo "Response (wrong client_secret):"
echo "${BAD_SECRET_RESPONSE}" | python3.12 -m json.tool 2>/dev/null || echo "${BAD_SECRET_RESPONSE}"
echo ""
echo "Wrong client credentials → invalid_client. The secret protects the token endpoint."

echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "DONE — OAuth 2.0 authorization code flow complete"
echo "══════════════════════════════════════════════════════════════════════"
echo ""
echo "What happened:"
echo "  1. Client built an authorization URL with response_type=code"
echo "  2. Auth server validated the client and issued a short-lived code"
echo "  3. Code traveled through the front channel (browser redirect)"
echo "  4. Client exchanged code + secret for an access token (back channel POST)"
echo "  5. Client used the token as a Bearer credential to access the resource"
