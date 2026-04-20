#!/usr/bin/env bash
# bytes_demo.sh — look at a file's raw bytes with xxd
#
# What this shows:
#   - A plain-text file is a sequence of numeric byte values
#   - Hex dump: offset | hex bytes | ASCII gutter
#   - The same bytes viewed as hex (xxd) and as bits (xxd -b)
#   - File-format magic bytes: a PNG starts with a specific signature
#
# Run:
#   bash bytes_demo.sh

set -e

# Use the script's own directory for temp files so the demo is self-contained
DIR="$(cd "$(dirname "$0")" && pwd)"
HELLO="$DIR/hello.txt"
PNG="$DIR/tiny.png"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION A — Every letter is a byte"
echo "═══════════════════════════════════════════════════════════════"
# Write exactly 14 bytes: 13 printable chars + one trailing newline (\n = 0x0a)
printf 'Hello, world!\n' > "$HELLO"
echo "  Wrote $HELLO  ($(wc -c < "$HELLO" | tr -d ' ') bytes)"
echo ""
echo "  --- xxd hello.txt ---"
# Default xxd: 16 bytes per line shown as offset | hex pairs | ASCII gutter
xxd "$HELLO"
echo ""
echo "  Read the hex column left to right:"
echo "    48 = 'H'   65 = 'e'   6c = 'l'   6c = 'l'   6f = 'o'"
echo "    2c = ','   20 = ' '   77 = 'w'   6f = 'o'   72 = 'r'"
echo "    6c = 'l'   64 = 'd'   21 = '!'   0a = newline"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION B — One byte, four ways: char, hex, decimal, binary"
echo "═══════════════════════════════════════════════════════════════"
# Pick the first byte of hello.txt and show it in every representation
echo "  The first byte of hello.txt is 'H'."
echo "    As hex:     0x48"
echo "    As decimal: $((16#48))"
# printf can format a decimal as 8-bit binary via Bash (printf %b does NOT — use a shell-portable loop)
BIN=""
N=$((16#48))
for ((i=7; i>=0; i--)); do
  BIN+=$(( (N >> i) & 1 ))
done
echo "    As binary:  $BIN"
echo "    As char:    H"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION C — See the actual bits with xxd -b"
echo "═══════════════════════════════════════════════════════════════"
echo "  --- xxd -c 4 -b hello.txt  (4 bytes per line, binary view) ---"
# -b = binary; -c 4 = 4 bytes per line so the bits are readable
xxd -c 4 -b "$HELLO" | head -n 4
echo ""
echo "  The first two groups on line 1 are 01001000 01100101 = 'H' 'e'."

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION D — A non-text file has bytes too (PNG magic bytes)"
echo "═══════════════════════════════════════════════════════════════"
# Build a valid 8-byte PNG signature by hand so we do not depend on any sample files.
# Spec: 89 50 4e 47 0d 0a 1a 0a  — the 8-byte PNG file signature.
printf '\x89PNG\r\n\x1a\n' > "$PNG"
echo "  Wrote $PNG  ($(wc -c < "$PNG" | tr -d ' ') bytes — just the file signature)"
echo ""
echo "  --- xxd tiny.png ---"
xxd "$PNG"
echo ""
echo "  Byte 0 (0x89) is a sentinel: its high bit makes it not a valid ASCII char."
echo "  Bytes 1–3 spell 'PNG' in the ASCII gutter: 0x50 0x4e 0x47."
echo "  Every real PNG on your disk starts with these exact 8 bytes."

# Clean up temp files so repeat runs are idempotent
rm -f "$HELLO" "$PNG"
