#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Lab 5.6 – Part 3: OAuth 2.0 Authorization Code Flow
#
# BEFORE running this script:
#   Terminal 1 → python3.12 oauth_server.py
#   Terminal 2 → bash oauth_flow.sh
# ─────────────────────────────────────────────────────────────────────────────

BASE="http://localhost:8080"
CLIENT_ID="demo-client-id"
CLIENT_SECRET="demo-client-secret"
REDIRECT_URI="http://localhost:9000/callback"
STATE="random-csrf-token-$(date +%s)"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   OAuth 2.0 Authorization Code Flow — Step-by-Step Demo     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Authorization Request
# In a real app, the user's browser is redirected to this URL.
# We use curl -v so we can SEE the 302 redirect with our own eyes.
# ─────────────────────────────────────────────────────────────────────────────

echo "━━━━ STEP 1: Authorization Request ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Client directs the user's browser to:"
echo "  GET ${BASE}/authorize"
echo "  ?client_id=${CLIENT_ID}"
echo "  &redirect_uri=${REDIRECT_URI}"
echo "  &response_type=code"
echo "  &state=${STATE}"
echo
echo "Server responds with 302 → see the Location header:"
echo

AUTHORIZE_RESPONSE=$(curl -vs \
  "${BASE}/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&state=${STATE}" \
  2>&1)

echo "$AUTHORIZE_RESPONSE" | grep -E "< HTTP|< Location"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Extract the Authorization Code from the redirect URL
# (In production: the user's browser follows the redirect to your app's
#  callback endpoint. Your app reads the `code` query param.)
# ─────────────────────────────────────────────────────────────────────────────

echo
echo "━━━━ STEP 2: Extract Authorization Code from Redirect ━━━━━━━━━"

AUTH_CODE=$(echo "$AUTHORIZE_RESPONSE" \
  | grep -i "location:" \
  | grep -oE "code=[^&]+" \
  | cut -d= -f2)

echo "Authorization code: ${AUTH_CODE}"
echo "(This code is single-use and expires in 60 seconds.)"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Token Exchange
# The client's back-end server calls the token endpoint directly (not browser).
# Credentials are sent here — this is why back-channel is important.
# ─────────────────────────────────────────────────────────────────────────────

echo
echo "━━━━ STEP 3: Exchange Code for Access Token ━━━━━━━━━━━━━━━━━━━"
echo "POST ${BASE}/token"
echo "  grant_type=authorization_code"
echo "  code=${AUTH_CODE}"
echo "  client_id=${CLIENT_ID}"
echo "  client_secret=<redacted>"
echo

TOKEN_RESPONSE=$(curl -s -X POST "${BASE}/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=${AUTH_CODE}" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "redirect_uri=${REDIRECT_URI}")

echo "Response:"
echo "$TOKEN_RESPONSE" | python3.12 -m json.tool

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" \
  | python3.12 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo
echo "Access token: ${ACCESS_TOKEN}"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Use the Access Token to call a protected resource
# ─────────────────────────────────────────────────────────────────────────────

echo
echo "━━━━ STEP 4: Access Protected Resource ━━━━━━━━━━━━━━━━━━━━━━━━"
echo "GET ${BASE}/userinfo"
echo "Authorization: Bearer <token>"
echo

curl -s "${BASE}/userinfo" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  | python3.12 -m json.tool

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5: Show that the token is opaque (not a JWT)
# and that access fails without it
# ─────────────────────────────────────────────────────────────────────────────

echo
echo "━━━━ STEP 5: What happens without a token? ━━━━━━━━━━━━━━━━━━━━"
curl -s "${BASE}/userinfo" | python3.12 -m json.tool

echo
echo "━━━━ STEP 6: Replay the same code (should fail) ━━━━━━━━━━━━━━━"
echo "Codes are single-use. Replaying ${AUTH_CODE:0:10}…"
curl -s -X POST "${BASE}/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=${AUTH_CODE}" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  | python3.12 -m json.tool

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Done. OAuth 2.0 Authorization Code Flow complete."
