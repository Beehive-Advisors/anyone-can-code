#!/usr/bin/env python3.12
"""
oauth_server.py — Local OAuth 2.0 authorization code flow demo server

This single Flask app plays all three OAuth roles:
  - Authorization server  → /authorize, /token, /callback
  - Resource server       → /protected

The "client" role is played by the student using curl in oauth_flow.sh.

Run with:
    source .venv/bin/activate
    python3.12 oauth_server.py

Then, in a second terminal, run:
    bash oauth_flow.sh

NOTE: Server runs on port 5001 (avoids the macOS AirPlay Receiver conflict on port 5000).
"""

import secrets
import time

from flask import Flask, abort, jsonify, redirect, request

app = Flask(__name__)

# ─── Registered clients ────────────────────────────────────────────────────────
# In a real system this would be in a database.
REGISTERED_CLIENTS = {
    "demo-client": {
        "secret": "demo-secret",
        "redirect_uris": ["http://localhost:5001/callback"],
    }
}

# ─── In-memory stores (reset on server restart) ────────────────────────────────
# { code: { "client_id", "redirect_uri", "used", "issued_at" } }
issued_codes: dict = {}

# { token: { "sub", "scope", "expires_at" } }
issued_tokens: dict = {}


# ══════════════════════════════════════════════════════════════════════════════
# Authorization endpoint
# Step 1 of the flow: client redirects the user here.
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/authorize")
def authorize():
    response_type = request.args.get("response_type", "")
    client_id = request.args.get("client_id", "")
    redirect_uri = request.args.get("redirect_uri", "")
    scope = request.args.get("scope", "")
    state = request.args.get("state", "")

    print(f"\n[AUTH SERVER] /authorize hit")
    print(f"  client_id:    {client_id}")
    print(f"  redirect_uri: {redirect_uri}")
    print(f"  scope:        {scope}")
    print(f"  state:        {state}")

    # Validate parameters
    if client_id not in REGISTERED_CLIENTS:
        return jsonify({"error": "unknown_client"}), 400

    if redirect_uri not in REGISTERED_CLIENTS[client_id]["redirect_uris"]:
        return jsonify({"error": "invalid_redirect_uri"}), 400

    if response_type != "code":
        return jsonify({"error": "unsupported_response_type"}), 400

    # In a real server: show a login page and consent screen here.
    # For this demo: auto-approve and issue a code immediately.
    code = secrets.token_urlsafe(16)
    issued_codes[code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "used": False,
        "issued_at": time.time(),
    }

    print(f"  [AUTH SERVER] Issuing code: {code}")

    # Redirect back to the client with the authorization code (front channel)
    location = f"{redirect_uri}?code={code}"
    if state:
        location += f"&state={state}"

    return redirect(location, code=302)


# ══════════════════════════════════════════════════════════════════════════════
# Token endpoint
# Step 2: client's backend exchanges the code for an access token (back channel).
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/token", methods=["POST"])
def token():
    grant_type = request.form.get("grant_type", "")
    code = request.form.get("code", "")
    redirect_uri = request.form.get("redirect_uri", "")
    client_id = request.form.get("client_id", "")
    client_secret = request.form.get("client_secret", "")

    print(f"\n[AUTH SERVER] /token hit")
    print(f"  grant_type:   {grant_type}")
    print(f"  code:         {code}")
    print(f"  client_id:    {client_id}")
    print(f"  redirect_uri: {redirect_uri}")

    # Validate client credentials
    if client_id not in REGISTERED_CLIENTS:
        return jsonify({"error": "invalid_client"}), 401
    if REGISTERED_CLIENTS[client_id]["secret"] != client_secret:
        return jsonify({"error": "invalid_client", "detail": "wrong secret"}), 401

    # Validate the authorization code
    if code not in issued_codes:
        return jsonify({"error": "invalid_grant", "detail": "unknown code"}), 400

    code_data = issued_codes[code]

    if code_data["used"]:
        return jsonify({"error": "invalid_grant", "detail": "code already used"}), 400

    if time.time() - code_data["issued_at"] > 600:  # codes expire after 10 minutes
        return jsonify({"error": "invalid_grant", "detail": "code expired"}), 400

    if code_data["client_id"] != client_id:
        return jsonify({"error": "invalid_grant", "detail": "client mismatch"}), 400

    if code_data["redirect_uri"] != redirect_uri:
        return jsonify({"error": "invalid_grant", "detail": "redirect_uri mismatch"}), 400

    # Mark code as used — single-use enforcement
    issued_codes[code]["used"] = True

    # Issue an access token
    access_token = secrets.token_urlsafe(32)
    issued_tokens[access_token] = {
        "sub": "demo-user",
        "scope": "read_profile",
        "expires_at": time.time() + 3600,
    }

    print(f"  [AUTH SERVER] Issuing access token: {access_token[:20]}...")

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "read_profile",
    })


# ══════════════════════════════════════════════════════════════════════════════
# Protected resource endpoint
# Step 3: client calls the API with the Bearer token.
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/protected")
def protected():
    auth_header = request.headers.get("Authorization", "")

    print(f"\n[RESOURCE SERVER] /protected hit")
    print(f"  Authorization: {auth_header[:50]}")

    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "unauthorized", "detail": "missing Bearer token"}), 401

    token_value = auth_header[7:]  # strip "Bearer "

    if token_value not in issued_tokens:
        return jsonify({"error": "invalid_token", "detail": "unknown token"}), 401

    token_data = issued_tokens[token_value]
    if time.time() > token_data["expires_at"]:
        return jsonify({"error": "invalid_token", "detail": "token expired"}), 401

    print(f"  [RESOURCE SERVER] Token valid — returning resource for {token_data['sub']}")

    return jsonify({
        "message": "Access granted",
        "user": token_data["sub"],
        "scope": token_data["scope"],
        "profile": {"name": "Demo User", "email": "demo@example.com"},
    })


# ══════════════════════════════════════════════════════════════════════════════
# Client callback endpoint
# Where the browser lands after /authorize redirects back.
# In a real app this is on your own server — here it's just for inspection.
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/callback")
def callback():
    code = request.args.get("code", "")
    state = request.args.get("state", "")
    error = request.args.get("error", "")

    print(f"\n[CLIENT] /callback hit")
    print(f"  code:  {code}")
    print(f"  state: {state}")

    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "Authorization code received at callback",
        "code": code,
        "state": state,
        "note": "A real client would now POST this code to /token (back channel)",
    })


if __name__ == "__main__":
    print("OAuth 2.0 Demo Server")
    print("Listening on http://localhost:5001")
    print()
    print("Endpoints:")
    print("  GET  /authorize  — authorization endpoint (redirect user here)")
    print("  POST /token      — token endpoint (exchange code for token)")
    print("  GET  /protected  — protected resource (requires Bearer token)")
    print("  GET  /callback   — client callback (receives the authorization code)")
    print()
    print("In a second terminal, run:  bash oauth_flow.sh")
    print()
    app.run(host="127.0.0.1", port=5001, debug=False)
