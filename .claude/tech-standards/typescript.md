# TypeScript / Node.js Standards

These rules apply to every `.ts`, `.js`, and Next.js file in any lab. Read and apply them when writing or reviewing TypeScript/Node.js demo files.

---

## Environment

- Use `npm` for package management: `npm install`
- Run TypeScript files with: `npx ts-node [filename].ts`
- Run compiled JS with: `node [filename].js`
- For Next.js apps: `npm run dev` (development), `npm run build` (verify before shipping)

---

## File header (required on every standalone `.ts`/`.js` demo file)

```typescript
/**
 * filename.ts — [one-line description]
 *
 * What this shows:
 *   - [concept 1]
 *   - [concept 2]
 *
 * Run:
 *   npx ts-node filename.ts
 */
```

---

## Section structure

```typescript
console.log();
console.log("=".repeat(60));
console.log("SECTION A — [description]");
console.log("=".repeat(60));
```

Use 3–4 sections per file. The last section is always a practical contrast or demonstration.

---

## Output labeling

Every logged value must be labeled:

```typescript
console.log(`  Token: ${token}`);   // correct — labeled
console.log(token);                  // wrong — unlabeled
```

---

## Next.js labs

- Build must succeed: `npm run build` exits 0 with no TypeScript errors and no ESLint errors
- Components use shadcn/ui + Tailwind CSS — no inline styles unless intentional
- Avoid `any` types; if unavoidable, add a comment explaining why

---

## Exit code

Every demo file must exit with code 0. No unhandled promise rejections. Verify before writing scripts:

```bash
npx ts-node filename.ts; echo "Exit: $?"
```
