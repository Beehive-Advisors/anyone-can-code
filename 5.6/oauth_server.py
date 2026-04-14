#!/usr/bin/env python3
"""
Minimal OAuth 2.0 Authorization Server — course demo only.
Runs on http://localhost:8080
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
import json, secrets, time, sys

# ── In-memory stores ────────────────────────────────────────────────────────
AUTH_CODES: dict = {}
ACCESS_TOKENS: dict = {}

# ── Pre-registered demo client ───────────────────────────────────────────────
CLIENT = {
    "id":     "demo-client-id",
    "secret": "demo-client-secret",
    "redirect_uri": "http://localhost:9000/callback",
}

# ── Mock user ────────────────────────────────────────────────────────────────
USER = {
    "sub":   "user_001",
    "name":  "Alice Demo",
    "email": "alice@example.com",
    "role":  "member",
}


class OAuthHandler(BaseHTTPRequestHandler):

    # ── routing ──────────────────────────────────────────────────────────────

    def do_GET(self):
        p = urlparse(self.path)
        qs = parse_qs(p.query)
        if p.path == "/authorize":
            self._authorize(qs)
        elif p.path == "/userinfo":
            self._userinfo()
        else:
            self._json(404, {"error": "not_found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)
        p = urlparse(self.path)
        if p.path == "/token":
            self._token(params)
        else:
            self._json(404, {"error": "not_found"})

    # ── handlers ─────────────────────────────────────────────────────────────

    def _authorize(self, qs):
        client_id    = qs.get("client_id",    [""])[0]
        redirect_uri = qs.get("redirect_uri", [""])[0]
        state        = qs.get("state",        [""])[0]

        if client_id != CLIENT["id"]:
            self._json(400, {"error": "invalid_client"})
            return

        code = secrets.token_urlsafe(16)
        AUTH_CODES[code] = {
            "client_id":    client_id,
            "redirect_uri": redirect_uri,
            "expires":      time.time() + 60,
        }

        location = redirect_uri + "?" + urlencode({"code": code, "state": state})
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

        print(f"\n[AUTH SERVER] /authorize  → issued code {code[:10]}…")
        print(f"[AUTH SERVER] Redirecting → {location}")
        sys.stdout.flush()

    def _token(self, params):
        grant  = params.get("grant_type",    [""])[0]
        code   = params.get("code",          [""])[0]
        cid    = params.get("client_id",     [""])[0]
        secret = params.get("client_secret", [""])[0]

        if grant != "authorization_code":
            self._json(400, {"error": "unsupported_grant_type"}); return
        if cid != CLIENT["id"] or secret != CLIENT["secret"]:
            self._json(401, {"error": "invalid_client"}); return
        if code not in AUTH_CODES:
            self._json(400, {"error": "invalid_grant"}); return
        if time.time() > AUTH_CODES[code]["expires"]:
            AUTH_CODES.pop(code)
            self._json(400, {"error": "code_expired"}); return

        AUTH_CODES.pop(code)          # single-use
        token = secrets.token_urlsafe(32)
        ACCESS_TOKENS[token] = {"user": USER, "expires": time.time() + 3600}

        print(f"\n[AUTH SERVER] /token      → issued access_token {token[:12]}…")
        sys.stdout.flush()
        self._json(200, {
            "access_token": token,
            "token_type":   "Bearer",
            "expires_in":   3600,
            "scope":        "read:profile",
        })

    def _userinfo(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            self._json(401, {"error": "unauthorized"}); return
        token = auth[7:]
        if token not in ACCESS_TOKENS:
            self._json(401, {"error": "invalid_token"}); return
        if time.time() > ACCESS_TOKENS[token]["expires"]:
            ACCESS_TOKENS.pop(token)
            self._json(401, {"error": "token_expired"}); return

        print(f"\n[AUTH SERVER] /userinfo   → returning profile for {ACCESS_TOKENS[token]['user']['name']}")
        sys.stdout.flush()
        self._json(200, ACCESS_TOKENS[token]["user"])

    # ── helpers ──────────────────────────────────────────────────────────────

    def _json(self, status: int, data: dict):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Print method + path + status line only
        print(f"[AUTH SERVER] {self.command} {self.path}  →  {args[1]}")
        sys.stdout.flush()


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), OAuthHandler)
    print("OAuth 2.0 Demo Server  →  http://localhost:8080")
    print("Endpoints: /authorize  /token  /userinfo")
    print("Press Ctrl-C to stop.\n")
    sys.stdout.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
