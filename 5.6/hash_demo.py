#!/usr/bin/env python3
"""
Lab 5.6 – Part 1: Password Hashing with bcrypt
Run: python3.12 hash_demo.py
"""
import bcrypt
import time


# ─────────────────────────────────────────────────────────────────────────────
# Section A: Basic hash + verify
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("SECTION A — Hashing a password")
print("=" * 60)

password = b"correct-horse-battery-staple"

# gensalt() picks a random 22-character salt and embeds it in the hash
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

print(f"Plaintext : {password.decode()}")
print(f"Hash      : {hashed.decode()}")
print()

# Anatomy of the hash string
parts = hashed.decode().split("$")
# parts[0] == ''  parts[1] == '2b'  parts[2] == '12'  parts[3] == salt+hash
print("Hash anatomy:")
print(f"  $2b  → algorithm identifier (bcrypt v2b)")
print(f"  ${parts[2]}  → cost factor (2^{parts[2]} = {2**int(parts[2]):,} iterations)")
print(f"  {parts[3][:22]}  → 22-char random salt (embedded in hash string)")
print(f"  {parts[3][22:]}  → 31-char actual hash output")
print()


# ─────────────────────────────────────────────────────────────────────────────
# Section B: Verify
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("SECTION B — Verifying passwords")
print("=" * 60)

result_correct = bcrypt.checkpw(b"correct-horse-battery-staple", hashed)
result_wrong   = bcrypt.checkpw(b"hunter2", hashed)

print(f"bcrypt.checkpw(correct_password, hash) → {result_correct}")
print(f"bcrypt.checkpw(wrong_password,   hash) → {result_wrong}")
print()
print("Note: checkpw() re-hashes the candidate using the salt embedded in the")
print("stored hash, then does a constant-time comparison. No secret needed.")
print()


# ─────────────────────────────────────────────────────────────────────────────
# Section C: Salt means every hash is unique
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("SECTION C — Salt uniqueness (same password → different hash)")
print("=" * 60)

pw = b"password123"
h1 = bcrypt.hashpw(pw, bcrypt.gensalt())
h2 = bcrypt.hashpw(pw, bcrypt.gensalt())
h3 = bcrypt.hashpw(pw, bcrypt.gensalt())

print(f"Hash 1: {h1.decode()}")
print(f"Hash 2: {h2.decode()}")
print(f"Hash 3: {h3.decode()}")
print()
print("All three verify correctly against 'password123':")
for i, h in enumerate([h1, h2, h3], 1):
    print(f"  Hash {i} matches: {bcrypt.checkpw(pw, h)}")
print()
print("This defeats rainbow-table attacks: the attacker must crack each hash")
print("individually, not build a single lookup table.")
print()


# ─────────────────────────────────────────────────────────────────────────────
# Section D: Cost factor vs. speed
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("SECTION D — Cost factor and time (the whole point of bcrypt)")
print("=" * 60)

pw = b"test"
print(f"{'Cost':>6}  {'Time':>8}  Iterations")
print("-" * 40)
for rounds in [4, 8, 10, 12]:
    start = time.perf_counter()
    bcrypt.hashpw(pw, bcrypt.gensalt(rounds=rounds))
    elapsed = time.perf_counter() - start
    print(f"  {rounds:4d}    {elapsed:6.3f}s  2^{rounds} = {2**rounds:>6,}")

print()
print("Default (rounds=12): ~0.25s per hash → 4 attempts/sec for an attacker.")
print("MD5 or plain SHA-256: billions of attempts per second.")
print("The slowness is the point.")
