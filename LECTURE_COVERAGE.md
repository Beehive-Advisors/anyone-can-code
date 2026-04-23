# Lecture Coverage Registry

Tracks what each completed lecture taught. The `/create-lecture` skill reads this
before researching a new lecture to avoid re-teaching covered concepts. The
`/review-lecture` skill reads it to check for course overlap.

**To approve a lecture:** change its Status in `SYLLABUS.md` from `Draft` to `Approved`.

---

## Lecture 1.4 — Memory Hierarchy

**Status:** Draft
**Completed:** 2026-04-23

### Concepts Taught
- Registers as the only addressable operand location for the ALU
- The memory wall: widening gap between CPU and DRAM speeds over two decades
- The five-tier hierarchy: registers → cache (L1/L2/L3) → RAM → SSD → HDD
- Speed-cost-capacity tradeoff that shapes every layer
- SRAM (6T, stable) vs DRAM (1T + 1C, leaking capacitor requires refresh)
- L1/L2/L3 cycle costs: ~4 / ~10 / ~30; DRAM ~350
- Temporal and spatial locality — the two patterns that make caching work
- Cache lines (64 bytes / 8 × 8-byte words) as the fetch granularity
- Sequential vs random access and the ~10× time gap from layout alone
- Persistent storage: HDD mechanics (seek + rotate, ~13 ms) vs NVMe (no moving parts, ~100 μs)
- Latency vs bandwidth distinction — "SSDs are basically RAM" misconception
- Cost of a cache miss measured in instructions foregone (~1000)

### Library Assets Used
- CPU, ALU, Register, Cache, RAM, NVMe, HDD, Bus
- HierarchyPyramid (new — 5-tier pyramid visual)
- MemoryCell (new — SRAM/DRAM bit cell with capacitor leak/refresh)
- CacheLine (new — 8-slot strip for 64-byte line visuals)
- ArrayStrip (new — 12-cell indexed array for sequential/random walk)

### Animations Produced
1. `register-closeup` — ALU center with register neighbors, values flowing in and out
2. `hierarchy-pyramid` — the five-tier pyramid with fast/slow and small/big axes
3. `sram-vs-dram-cell` — SRAM cell stable; DRAM cell leaks and is refreshed
4. `cache-levels-nested` — CPU request walks L1 → L2 → L3 → RAM with cycle counter
5. `cache-line-64-bytes` — fetching one byte actually loads a whole 64-byte line
6. `sequential-vs-random` — two identical array walks, 10× time difference from layout
7. `hdd-internals` — HDD reveals platter and head arm; NVMe flashes "no moving parts"
8. `latency-log-ladder` — log-scale latency bars with human-scale analogies
9. `the-stall` — single cache miss freezes the CPU for ~1000 instructions of lost work

---
