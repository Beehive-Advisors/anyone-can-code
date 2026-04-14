#!/usr/bin/env python3.12
"""
hash_demo.py — bcrypt password hashing demo

What this shows:
  - Why fast hashing (SHA-256) is dangerous for passwords
  - What's inside a bcrypt hash string
  - Why every hash of the same password looks different
  - How the cost factor controls timing

Run with:
    source .venv/bin/activate
    python3.12 hash_demo.py
"""

import bcrypt
import hashlib
import time

print()
print("=" * 70)
print("SECTION A — The problem: fast hashing vs. slow hashing")
print("=" * 70)

password = b"hunter2"

# Time SHA-256 for 100,000 hashes
start = time.perf_counter()
for _ in range(100_000):
    hashlib.sha256(password).hexdigest()
sha256_elapsed = time.perf_counter() - start

print()
print(f"  SHA-256 × 100,000 hashes: {sha256_elapsed:.3f} seconds")
print(f"  SHA-256 per hash:         {sha256_elapsed / 100_000 * 1_000_000:.1f} microseconds")
print(f"  SHA-256 hashes/second:    {100_000 / sha256_elapsed:,.0f}")
print()

# Time one bcrypt hash at cost 12
start = time.perf_counter()
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
bcrypt_elapsed = time.perf_counter() - start

print(f"  bcrypt × 1 hash (cost 12): {bcrypt_elapsed:.3f} seconds")
print(f"  bcrypt per hash:            {bcrypt_elapsed * 1000:.1f} milliseconds")
print(f"  bcrypt hashes/second:       {1 / bcrypt_elapsed:,.0f}")
print()

speedup = bcrypt_elapsed / (sha256_elapsed / 100_000)
print(f"  Speed ratio: SHA-256 is {speedup:,.0f}x faster than bcrypt")
print()
print("  An attacker who steals a SHA-256 password database can try")
print("  billions of guesses per second with a GPU.")
print("  With bcrypt cost 12, that same hardware gets a few thousand guesses/sec.")


print()
print("=" * 70)
print("SECTION B — Anatomy: what's inside a bcrypt hash string")
print("=" * 70)

password = b"correct-horse-battery-staple"
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password, salt)

print()
print(f"  Password:  {password}")
print(f"  Full hash: {hashed}")
print()

h = hashed.decode("utf-8")
print("  Decoded fields:")
print(f"    Version:     {h[0:4]!r}   — bcrypt algorithm version")
print(f"    Cost factor: {h[4:6]!r}     — 2^12 = 4,096 Blowfish setup rounds")
print(f"    Salt:        {h[7:29]!r} — 22 chars (16 random bytes, base64-encoded)")
print(f"    Hash:        {h[29:]!r} — 31 chars (24 bytes of ciphertext)")
print()
print(f"  Total length: {len(h)} characters — always the same, regardless of password length")
print()
print("  The salt is embedded in the hash. You do not store it separately.")
print("  bcrypt.checkpw() reads the salt out of the hash automatically.")


print()
print("=" * 70)
print("SECTION C — Salts: same password, different hash every time")
print("=" * 70)

password = b"password123"
print()
print(f"  Hashing {password!r} three times:")
print()

hashes = []
for i in range(3):
    h = bcrypt.hashpw(password, bcrypt.gensalt(rounds=10))
    hashes.append(h)
    print(f"  Hash {i + 1}: {h.decode()}")

print()
print(f"  All three are different: {len(set(hashes)) == 3}")
print()
print("  Verifying each hash against the original password:")
for i, h in enumerate(hashes):
    result = bcrypt.checkpw(password, h)
    print(f"    Hash {i + 1}: checkpw = {result}")

print()
print("  bcrypt.checkpw() extracts the salt from each stored hash,")
print("  recomputes, and compares — so all three verify correctly.")
print()
print("  Rainbow tables are useless: precomputed hash lookups only work")
print("  when everyone hashing 'password123' gets the same output.")
print("  With a random salt, they never do.")


print()
print("=" * 70)
print("SECTION D — Cost factor: doubling rounds, doubling time")
print("=" * 70)

password = b"timing-test"
print()
print("  Timing one bcrypt hash at increasing cost factors:")
print()

for cost in [10, 12, 14]:
    start = time.perf_counter()
    bcrypt.hashpw(password, bcrypt.gensalt(rounds=cost))
    elapsed = time.perf_counter() - start
    guesses = 1 / elapsed
    print(f"  Cost {cost:2d}: {elapsed:.3f}s  (~{guesses:,.0f} attacker guesses/sec)")

print()
print("  Each step +1 doubles the computation. Cost 14 takes 4x cost 12.")
print("  OWASP recommends cost 12 as today's minimum for new systems.")
print("  Choose a cost that takes ~100–300ms on your server hardware.")
