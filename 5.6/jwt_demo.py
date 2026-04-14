#!/usr/bin/env python3.12
"""
jwt_demo.py — JSON Web Token demo

What this shows:
  - How a JWT is built manually (base64url + HMAC-SHA256)
  - How PyJWT automates that process
  - Why the payload is readable by anyone (it is NOT encrypted)
  - How the signature detects any tampering

Run with:
    source .venv/bin/activate
    python3.12 jwt_demo.py
"""

import base64
import hashlib
import hmac
import json
import time

import jwt

SECRET = "this-is-a-32-byte-secret-key-ok!"


print()
print("=" * 70)
print("SECTION A — Build a JWT by hand (what PyJWT does under the hood)")
print("=" * 70)

# Step 1: Build the header
header = {"alg": "HS256", "typ": "JWT"}
header_json = json.dumps(header, separators=(",", ":"))
header_b64 = base64.urlsafe_b64encode(header_json.encode()).rstrip(b"=")
print()
print(f"  Step 1 — Header JSON:        {header_json}")
print(f"           Header base64url:   {header_b64.decode()}")

# Step 2: Build the payload
payload = {"sub": "alice", "role": "admin", "iat": int(time.time())}
payload_json = json.dumps(payload, separators=(",", ":"))
payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).rstrip(b"=")
print()
print(f"  Step 2 — Payload JSON:       {payload_json}")
print(f"           Payload base64url:  {payload_b64.decode()}")

# Step 3: Compute HMAC-SHA256 signature
signing_input = header_b64 + b"." + payload_b64
sig_bytes = hmac.new(SECRET.encode(), signing_input, hashlib.sha256).digest()
sig_b64 = base64.urlsafe_b64encode(sig_bytes).rstrip(b"=")
print()
print(f"  Step 3 — HMAC-SHA256 input:  {signing_input.decode()}")
print(f"           Signature base64url: {sig_b64.decode()}")

# Step 4: Assemble
manual_token = signing_input.decode() + "." + sig_b64.decode()
print()
print(f"  Step 4 — Final JWT:          {manual_token}")
print()
print("  Structure: HEADER.PAYLOAD.SIGNATURE (three base64url parts, dot-separated)")
print("  PyJWT does exactly these four steps — it just automates them.")


print()
print("=" * 70)
print("SECTION B — Encode and decode with PyJWT")
print("=" * 70)

payload = {
    "sub": "alice",
    "role": "admin",
    "exp": int(time.time()) + 3600,  # expires in 1 hour
}

token = jwt.encode(payload, SECRET, algorithm="HS256")
print()
print(f"  jwt.encode() output: {token}")
print()
print(f"  Token parts:")
parts = token.split(".")
print(f"    Header  ({len(parts[0]):2d} chars): {parts[0]}")
print(f"    Payload ({len(parts[1]):2d} chars): {parts[1]}")
print(f"    Sig     ({len(parts[2]):2d} chars): {parts[2]}")
print()

decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
print(f"  jwt.decode() output: {decoded}")
print()
print("  Note: algorithms= must be a LIST (common mistake: passing a string).")
print("  PyJWT validates the 'exp' claim automatically on decode.")


print()
print("=" * 70)
print("SECTION C — Anyone can read the payload (JWTs are signed, not encrypted)")
print("=" * 70)

print()
# Read header without any key
header_unverified = jwt.get_unverified_header(token)
print(f"  Header (no key needed):  {header_unverified}")

# Read payload without verifying signature
payload_unverified = jwt.decode(
    token,
    options={"verify_signature": False},
    algorithms=["HS256"],
)
print(f"  Payload (no key needed): {payload_unverified}")
print()
print("  Manual decode (Python stdlib only):")
raw_part = token.split(".")[1]
padded = raw_part + "=" * (-len(raw_part) % 4)
raw_json = base64.urlsafe_b64decode(padded).decode()
print(f"    {raw_json}")
print()
print("  The payload is base64url-encoded JSON — anyone can read it.")
print("  Never put passwords, credit cards, or secrets in a JWT payload.")
print("  Use JWE (JSON Web Encryption) if you need encrypted payloads.")


print()
print("=" * 70)
print("SECTION D — Tamper detection: altering the payload breaks the signature")
print("=" * 70)

# Create a valid token for a regular user
user_payload = {
    "sub": "bob",
    "role": "user",
    "exp": int(time.time()) + 3600,
}
user_token = jwt.encode(user_payload, SECRET, algorithm="HS256")
print()
print(f"  Original token (role=user):   {user_token}")

# Tamper: rebuild the payload with role=admin, keep the original signature
parts = user_token.split(".")
bad_payload = {"sub": "bob", "role": "admin", "exp": int(time.time()) + 3600}
bad_json = json.dumps(bad_payload, separators=(",", ":"))
bad_b64 = base64.urlsafe_b64encode(bad_json.encode()).rstrip(b"=").decode()
tampered = parts[0] + "." + bad_b64 + "." + parts[2]  # same signature, new payload
print(f"  Tampered token (role=admin):  {tampered}")
print()

# Attempt to verify the tampered token
try:
    jwt.decode(tampered, SECRET, algorithms=["HS256"])
    print("  Verification: ACCEPTED — this should never happen")
except jwt.exceptions.InvalidSignatureError as e:
    print(f"  Verification: REJECTED — {type(e).__name__}")
    print()
    print("  The signature was computed over the original payload.")
    print("  Changing the payload makes the signature invalid.")
    print("  Without the secret key, you cannot produce a new valid signature.")
    print("  This is the entire security property of a JWT.")
