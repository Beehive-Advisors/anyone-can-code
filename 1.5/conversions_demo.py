#!/usr/bin/env python3.12
"""
conversions_demo.py — convert between char, decimal, hex, and binary in Python

What this shows:
  - One byte has four equivalent representations: character, decimal, hex, binary
  - ord() / chr() bridge characters and integers
  - bin() / hex() / int() / f-string format specs produce and parse number strings
  - bytes.hex() / bytes.fromhex() do the same trip at the bytes-object level (the
    machine-readable equivalent of `xxd` and `xxd -r`)

Run:
    python3.12 conversions_demo.py
"""

print()
print("=" * 70)
print("SECTION A — one byte, four representations")
print("=" * 70)

# Pick a single letter and show it in every base.
# The same integer 72 appears in all four views — only the formatting changes.
ch = "H"
n = ord(ch)                     # character -> decimal code point
print(f"  Character:     {ch!r}")
print(f"  ord('{ch}')        = {n}            (decimal)")
print(f"  hex({n})        = {hex(n)!r}          (hex string, with '0x' prefix)")
print(f"  bin({n})        = {bin(n)!r}     (binary string, with '0b' prefix)")
print(f"  chr({n})        = {chr(n)!r}            (back to the character)")

print()
print("  Clean formats via f-strings (no prefix, zero-padded):")
# :02x  = two-digit hex, zero-padded. Matches how xxd prints one byte.
# :08b  = eight-digit binary, zero-padded. Matches one full byte of bits.
hex_str = f"{n:02x}"
bin_str = f"{n:08b}"
print(f"  f\"{{n:02x}}\"      = {hex_str!r}          (two hex digits — like xxd)")
print(f"  f\"{{n:08b}}\"      = {bin_str!r}    (eight bits — one full byte)")

print()
print("=" * 70)
print("SECTION B — round trip: 'H' -> 72 -> '48' -> '01001000' -> 72 -> 'H'")
print("=" * 70)

# Prove the conversions are inverses by going forward then backward.
step1 = ord("H")                   # 'H' -> 72
step2 = f"{step1:02x}"             # 72  -> '48'
step3 = f"{step1:08b}"             # 72  -> '01001000'
step4 = int(step2, 16)             # '48' parsed as base-16 -> 72
step5 = int(step3, 2)              # '01001000' parsed as base-2 -> 72
step6 = chr(step4)                 # 72  -> 'H'

print(f"  Forward:")
print(f"    ord('H')                 -> {step1}")
print(f"    f'{{72:02x}}'              -> {step2!r}")
print(f"    f'{{72:08b}}'              -> {step3!r}")
print(f"  Backward:")
print(f"    int('{step2}', 16)           -> {step4}")
print(f"    int('{step3}', 2)     -> {step5}")
print(f"    chr({step4})                 -> {step6!r}")
print(f"  Round trip holds:          {step6 == 'H'}")

print()
print("=" * 70)
print("SECTION C — a whole word, byte by byte")
print("=" * 70)

word = "Hello"
print(f"  Word: {word!r}")
print()
# Header row for a four-column table. Fixed widths line the columns up.
print(f"  {'char':<6}{'decimal':<10}{'hex':<6}{'binary':<10}")
print(f"  {'----':<6}{'-------':<10}{'---':<6}{'------':<10}")
for c in word:
    code = ord(c)
    # :02x and :08b make the hex and binary columns exactly one byte wide
    print(f"  {c!r:<6}{code:<10}{code:02x}    {code:08b}")

print()
print("  Compare the 'hex' column to what xxd printed for hello.txt.")
print("  The numbers match byte-for-byte. Python and xxd are describing the")
print("  same underlying reality — bytes on your disk — from two directions.")

print()
print("=" * 70)
print("SECTION D — bytes objects: hex() forward, fromhex() back")
print("=" * 70)

# A bytes object is a fixed-length sequence of integers 0..255.
# .hex() flattens it to a hex string; bytes.fromhex() rebuilds it.
# This is the machine-readable mirror of `xxd` and `xxd -r`.
original = b"Hello, world!"
as_hex   = original.hex()                  # -> '48656c6c6f2c20776f726c6421'
restored = bytes.fromhex(as_hex)           # -> b'Hello, world!'

print(f"  Original bytes:     {original!r}")
print(f"  original.hex():     {as_hex!r}")
print(f"  bytes.fromhex(...): {restored!r}")
print(f"  Round trip holds:   {original == restored}")
print()
print("  The hex string is the exact same 26 chars you see in xxd's middle column.")
