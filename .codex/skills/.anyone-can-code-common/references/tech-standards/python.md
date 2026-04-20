# Python Standards

Apply these rules to every `.py` demo file.

## Runtime

- create environments with `uv venv .venv --python 3.12`
- activate before running
- run with `python3.12 <filename>.py`
- install packages with `uv pip install ...`

## File Header

Every file needs a short module docstring with:
- filename and one-line description
- what the file demonstrates
- exact run instructions

## Structure

- use 3 to 4 clearly labeled sections
- label every printed value
- end with a practical contrast or demonstration

## Known Gotchas

- prefer `datetime.now(timezone.utc)` over deprecated UTC helpers
- keep byte versus string requirements explicit
- do not suppress warnings to hide real failures

## Verification

Every demo must exit 0 with no unhandled exceptions.
