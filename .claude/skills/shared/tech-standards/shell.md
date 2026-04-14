# Shell Script Standards

These rules apply to every `.sh` file in any lab. Read and apply them when writing or reviewing shell demo files.

---

## File header (required on every `.sh` demo file)

```bash
#!/usr/bin/env bash
# filename.sh — [one-line description]
#
# What this shows:
#   - [concept 1]
#   - [concept 2]
#
# Run:
#   bash filename.sh
```

---

## Section structure

```bash
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION A — [description]"
echo "═══════════════════════════════════════════════════════════════"
```

Use 3–4 sections per file. The last section is always a practical contrast or demonstration.

---

## Commenting rule

Every command must have a comment above it explaining what it does and why:

```bash
# Send an HTTP request and show the full response including headers
curl -v http://example.com 2>&1
```

No command appears without a comment. This is non-negotiable — students reading the script need to understand what each line does.

---

## Output labeling

Prefix output lines so students know what they're seeing:

```bash
echo "  Response body: $(curl -s http://example.com | head -1)"
```

---

## Error handling

Use `set -e` when the script should stop on any non-zero exit. For demos where intermediate commands are expected to fail (to show error handling), use `||` or `if` to handle them explicitly.

---

## Platform notes

macOS uses BSD versions of tools (`sed`, `date`, `netcat`). Linux uses GNU versions. The flags differ. When writing demo commands:
- Prefer flags that work on both platforms
- If a flag is platform-specific, note it in a comment

For lab setup instructions, always show both platforms:
```
**macOS:** `brew install [tool]`
**Linux / WSL:** `sudo apt install [tool]`
```

---

## Exit code

Every demo script must exit with code 0. Verify before writing scripts:

```bash
bash filename.sh; echo "Exit: $?"
```
