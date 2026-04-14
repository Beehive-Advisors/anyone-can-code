# Lab 5.6 — Auth Mechanics

This lab covers the three mechanisms behind almost every production authentication system: bcrypt password hashing, JSON Web Tokens (JWT), and the OAuth 2.0 authorization code flow. Students run working Python demos and curl commands to see each protocol step by step.

## Prerequisites

- Lab 4.13 (Speaking HTTP by Hand) — familiarity with HTTP request/response and curl
- Section 5.5 (Authentication and Authorization) — conceptual distinction between authn and authz
- Python 3.12 and `uv` installed

## Setup

```bash
cd ~/src/courses/anyone-can-code/5.6
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install bcrypt PyJWT flask
```

## Files

| File | Description | How to run |
|------|-------------|------------|
| `hash_demo.py` | bcrypt demo: fast vs. slow hashing, hash anatomy, salts, cost factor timing | `python3.12 hash_demo.py` |
| `jwt_demo.py` | JWT demo: manual construction, PyJWT encode/decode, payload visibility, tamper detection | `python3.12 jwt_demo.py` |
| `oauth_server.py` | Flask server implementing all three OAuth roles (authorization server, token endpoint, resource server) | `python3.12 oauth_server.py` (leave running in Terminal 1) |
| `oauth_flow.sh` | curl-based walkthrough of the full authorization code flow against the local server | `bash oauth_flow.sh` (in Terminal 2 while server is running) |
| `5.6-lab.md` | Student lab — instructions, exercises, and conceptual questions | Read in any Markdown viewer |
| `5.6-script.md` | Instructor screencast script — SPEAK/TYPE/OUTPUT/EXPLAIN beats for the lab recording | Reference only |
| `5.6-code-walkthrough.md` | Instructor screencast script — VS Code walkthrough of `hash_demo.py`, `jwt_demo.py`, and `oauth_server.py` before the lab run | Reference only |
| `5.6-report.md` | Research report — concept background, library details, design decisions, and sources | Reference only |

## Time estimate

~60 minutes (students); ~35–45 minutes screencast recording + ~18 minutes code walkthrough recording
