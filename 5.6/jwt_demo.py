#!/usr/bin/env python3
"""
Lab 5.6 – Part 2: JWT Creation, Decoding, and Tampering
Run: python3.12 jwt_demo.py
"""
import jwt
import json
import base64
import warnings
from datetime import datetime, timedelta, timezone

# Suppress key-length warnings for the demo (key is 32+ bytes below)
warnings.filterwarnings("ignore")

SECRET = "this-is-exactly-32-bytes-long!!"   # 32 bytes → satisfies RFC 7518


# ─────────────────────────────────────────────────────────────────────────────
# Section A: Create a JWT
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 70)
print("SECTION A — Creating a JWT")
print("=" * 70)

now = datetime.now(timezone.utc)
payload = {
    "sub":   "user_42",
    "name":  "Alice Demo",
    "email": "alice@example.com",
    "role":  "admin",
    "iat":   int(now.timestamp()),                            # issued at
    "exp":   int((now + timedelta(hours=1)).timestamp()),     # expiry
}

token = jwt.encode(payload, SECRET, algorithm="HS256")
print(f"Token:\n{token}\n")
print(f"Character count: {len(token)}")
print(f"Parts (split on '.'): {len(token.split('.'))}")


# ─────────────────────────────────────────────────────────────────────────────
# Section B: Decode without the library — just base64
# ─────────────────────────────────────────────────────────────────────────────

print()
print("=" * 70)
print("SECTION B — Manual base64url decode (no JWT library needed)")
print("=" * 70)

header_b64, payload_b64, sig_b64 = token.split(".")


def b64url_decode(s: str) -> dict:
    """Add padding, convert url-safe chars, then decode."""
    # base64url uses - and _ instead of + and /; strip any padding first
    s = s.replace("-", "+").replace("_", "/")
    # base64 requires length divisible by 4; pad with = as needed
    s += "=" * (-len(s) % 4)
    return json.loads(base64.b64decode(s))


header_decoded  = b64url_decode(header_b64)
payload_decoded = b64url_decode(payload_b64)

print(f"Header  (raw): {header_b64}")
print(f"Header (JSON): {json.dumps(header_decoded, indent=2)}")
print()
print(f"Payload  (raw): {payload_b64}")
print(f"Payload (JSON): {json.dumps(payload_decoded, indent=2)}")
print()
print("Signature (raw):", sig_b64)
print("(Signature is HMAC-SHA256 over 'header.payload', NOT base64url-decoded JSON)")


# ─────────────────────────────────────────────────────────────────────────────
# Section C: Verify with the library
# ─────────────────────────────────────────────────────────────────────────────

print()
print("=" * 70)
print("SECTION C — Library verification")
print("=" * 70)

decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
print(f"Decoded payload: {json.dumps(decoded, indent=2)}")

try:
    jwt.decode(token, "wrong-secret-key-that-is-32bytes", algorithms=["HS256"])
except jwt.exceptions.InvalidSignatureError as e:
    print(f"\nWrong secret → {type(e).__name__}: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Section D: Tampering — what happens if we change the payload?
# ─────────────────────────────────────────────────────────────────────────────

print()
print("=" * 70)
print("SECTION D — Tampering (privilege escalation attempt)")
print("=" * 70)

# Build a forged payload with role=superadmin
forged_payload = payload.copy()
forged_payload["role"] = "superadmin"

# base64url-encode it (without padding, as per JWT spec)
forged_json   = json.dumps(forged_payload, separators=(",", ":")).encode()
forged_b64    = base64.urlsafe_b64encode(forged_json).rstrip(b"=").decode()

# Reuse the original header + original signature (we don't know the secret)
tampered_token = f"{header_b64}.{forged_b64}.{sig_b64}"

print(f"Original role:  {payload['role']}")
print(f"Forged role:    {forged_payload['role']}")
print(f"\nTampered token:\n{tampered_token}\n")

try:
    jwt.decode(tampered_token, SECRET, algorithms=["HS256"])
    print("Verified! (should NOT happen)")
except jwt.exceptions.InvalidSignatureError as e:
    print(f"Server rejects tampered token → {type(e).__name__}")
    print("The signature covers the header+payload, so any edit breaks verification.")


# ─────────────────────────────────────────────────────────────────────────────
# Print the token for use in the shell exercises
# ─────────────────────────────────────────────────────────────────────────────

print()
print("=" * 70)
print("Copy this token for the shell decode exercise:")
print("=" * 70)
print(f"TOKEN={token}")
