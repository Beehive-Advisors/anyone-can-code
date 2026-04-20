# TypeScript Standards

Apply these rules to `.ts`, `.js`, and lightweight Node demo files.

## Runtime

- use `npm install`
- run TypeScript with `npx ts-node <filename>.ts`
- run JavaScript with `node <filename>.js`

## File Header

Each standalone file needs a header comment with:
- filename and one-line description
- what it demonstrates
- exact run instructions

## Structure

- use 3 to 4 labeled sections
- label every logged value
- avoid `any` unless there is a short reason
- end with a practical contrast or demonstration

## Verification

- demos must exit 0
- no unhandled promise rejections
