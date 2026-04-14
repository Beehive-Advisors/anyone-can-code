# Lab 5.6 — Auth Mechanics

Hands-on Python and shell lab covering the three auth mechanisms you encounter in every web application: bcrypt password hashing, JWT creation and tamper detection, and the OAuth 2.0 authorization code flow traced against a local server.

## Prerequisites

- Lab 4.13 (HTTP by hand) and Lab 5.5 (Auth concepts)
- Python 3.12, curl, bash

## Setup

```bash
cd 5.6
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install bcrypt PyJWT
```

## Files

| File | Description | How to run |
|------|-------------|------------|
| `hash_demo.py` | bcrypt password hashing — salt, cost factor, verification | `python3.12 hash_demo.py` |
| `jwt_demo.py` | JWT creation, manual base64url decode, tampering demo | `python3.12 jwt_demo.py` |
| `oauth_server.py` | Local OAuth 2.0 authorization server (infrastructure — run as black box) | `python3.12 oauth_server.py` |
| `oauth_flow.sh` | OAuth 2.0 authorization code flow client — all four steps via curl | `bash oauth_flow.sh` |
| `5.6-code-walkthrough.md` | Instructor script for the code walkthrough video (hash_demo.py + jwt_demo.py) | Read before running the lab |
| `5.6-lab.md` | Student lab — exercises, output blocks, solutions | Follow top to bottom |
| `5.6-script.md` | Instructor recording script for the lab screencast | For instructors |
| `5.6-report.md` | Research report: bcrypt, JWT, OAuth 2.0 — background and sources | Reference |

## Time

~50 minutes

## Notes

- **Two terminals required for Part 3 (OAuth):** Terminal 1 runs `oauth_server.py`; Terminal 2 runs `oauth_flow.sh`. Start both before you reach Part 3.
- **Watch the code walkthrough video before running Parts 1 and 2.** The walkthrough (`5.6-code-walkthrough.md`) covers every function in `hash_demo.py` and `jwt_demo.py` in detail. Run the demos after watching — the output will make sense immediately.
