# Lab 1.5 — Seeing the Machine

Read your own CPU, RAM, and disk specs from the terminal, then open a plain-text file as raw bytes with `xxd` and reproduce the same byte values from Python. Turns lectures 1.1–1.4's "everything is bytes" claim into something the student has seen with their own eyes.

## Prerequisites

- Lectures 1.1–1.4 (binary, logic gates, the CPU, the memory hierarchy)
- `bash`, `xxd` (ships with Vim), and `python3.12` on PATH

## Setup

```bash
cd 1.5
bash --version
xxd -v
python3.12 --version
```

No virtual environment, no `pip install` — this lab uses only the shell and the Python standard library.

If any tool is missing:

- **macOS:** `brew install vim python@3.12`
- **Linux / WSL:** `sudo apt install vim python3.12`

## Files

| File | What it does | How to run |
|------|--------------|------------|
| `hardware_demo.sh` | Reads CPU, RAM, and disk facts from the kernel (branches on `uname` for macOS/Linux) | `bash hardware_demo.sh` |
| `bytes_demo.sh` | Writes a text file + a PNG signature, then dumps both with `xxd` in hex and binary | `bash bytes_demo.sh` |
| `conversions_demo.py` | Converts a character through decimal, hex, and binary using `ord`, `chr`, `bin`, `hex`, `int`, f-strings, `bytes.hex()` | `python3.12 conversions_demo.py` |
| `1.5-lab.md` | Student lab handout | Open in editor |
| `1.5-script.md` | Instructor terminal screencast script | Open in editor |
| `1.5-code-walkthrough.md` | Instructor VS Code editor walkthrough script | Open in editor |
| `1.5-report.md` | Research report | Open in editor |

## Time

~45 minutes

## Notes

- One terminal, start to finish.
- `hardware_demo.sh` branches on `uname` — the macOS path uses `sysctl` / `vm_stat` / `diskutil list`, the Linux path uses `lscpu` / `free -h` / `lsblk`. Output will look different across platforms but the structure is the same.
- `bytes_demo.sh` writes `hello.txt` and `tiny.png` into the lab directory and removes them at the end; repeat runs are idempotent.
- Apple Silicon cache sizes live under `hw.perflevel0.*` / `hw.perflevel1.*`; Intel Mac keys (`hw.l1dcachesize`, etc.) are used as a fallback.
