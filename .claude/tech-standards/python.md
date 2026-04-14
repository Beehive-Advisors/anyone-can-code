# Python Standards

These rules apply to every `.py` file in any lab. Read and apply them when writing or reviewing Python demo files.

---

## Environment

- Always use `uv` for virtual environments: `uv venv .venv --python 3.12`
- Always activate before running: `source .venv/bin/activate`
- Always run with: `python3.12 [filename].py`
- Install command: `uv pip install [packages]`

---

## File header (required on every `.py` demo file)

```python
#!/usr/bin/env python3.12
"""
filename.py — [one-line description]

What this shows:
  - [concept 1]
  - [concept 2]

Run:
    source .venv/bin/activate
    python3.12 filename.py
"""
```

---

## Section structure

```python
print()
print("=" * 70)
print("SECTION A — [description]")
print("=" * 70)
```

Use 3–4 sections per file. The last section is always a practical contrast or demonstration.

---

## Output labeling

Every printed value must be labeled:

```python
print(f"  Hash: {hash_value}")      # correct — labeled
print(hash_value)                    # wrong — unlabeled
```

---

## Known gotchas

**`datetime.utcnow()` is deprecated in Python 3.12.**
Always use: `datetime.now(timezone.utc)`
Never use: `datetime.utcnow()`

**bcrypt inputs must be bytes.**
Use: `bcrypt.hashpw(b"password", salt)` — note the `b"..."` prefix.
Passing a plain string raises a `TypeError` at runtime.

**PyJWT HS256 requires a key of at least 32 bytes.**
Short keys raise `InsecureKeyLengthWarning` or fail to sign.
Use: `secrets.token_bytes(32)` or a hardcoded 32-character string.

**Never suppress warnings.**
Do not use `warnings.filterwarnings("ignore")`.
Fix the root cause instead — suppressed warnings hide real bugs.

---

## Exit code

Every demo file must exit with code 0. No unhandled exceptions. Verify before writing scripts:

```bash
python3.12 filename.py; echo "Exit: $?"
```
