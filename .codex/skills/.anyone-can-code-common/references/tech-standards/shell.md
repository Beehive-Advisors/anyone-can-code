# Shell Standards

Apply these rules to every `.sh` demo file.

## File Header

Each script needs:
- shebang
- one-line purpose
- bullet list of what it demonstrates
- exact run command

## Structure

- use 3 to 4 section banners
- put a comment above every non-trivial command
- label output so learners know what each line means
- end with a practical contrast or demonstration

## Portability

- prefer commands and flags that work on both macOS and Linux
- if you must use a platform-specific flag, note it in a comment or in setup instructions

## Verification

- use explicit error handling
- every demo script must exit 0
