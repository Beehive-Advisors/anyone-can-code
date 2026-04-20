#!/usr/bin/env bash
# hardware_demo.sh — read CPU, memory, and disk facts the kernel already knows
#
# What this shows:
#   - CPU architecture, core count, and cache sizes
#   - Total RAM and current usage
#   - Physical disks vs partitions vs mount points
#   - The scale ratio across the memory hierarchy (cache → RAM → disk)
#
# Run:
#   bash hardware_demo.sh
#
# Works on macOS and Linux. Uses `uname` to pick the right command per OS.

set -u
OS="$(uname)"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION A — CPU: architecture, cores, caches"
echo "═══════════════════════════════════════════════════════════════"
echo "  Your OS: $OS"
echo ""

if [[ "$OS" == "Darwin" ]]; then
  # macOS path: sysctl reads kernel variables; system_profiler gives a prose overview
  echo "  --- Chip and core counts (via sysctl) ---"
  # machdep.cpu.brand_string = the marketing name of the chip
  echo "  Brand:          $(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo '(not exposed on this chip)')"
  # hw.physicalcpu = real cores; hw.logicalcpu = cores × SMT threads
  echo "  Physical cores: $(sysctl -n hw.physicalcpu)"
  echo "  Logical cores:  $(sysctl -n hw.logicalcpu)"
  # hw.cachelinesize = bytes the CPU moves between cache levels at once
  echo "  Cache line:     $(sysctl -n hw.cachelinesize) bytes"
  echo ""
  echo "  --- Caches (per-core L1/L2) ---"
  # On Apple Silicon cache sizes live under hw.perflevel0 (performance) and hw.perflevel1 (efficiency).
  # On Intel Macs they live under hw.l1dcachesize etc. Try Apple Silicon keys first, fall back to Intel.
  if sysctl -n hw.perflevel0.l1dcachesize >/dev/null 2>&1; then
    echo "  L1d (perf):  $(sysctl -n hw.perflevel0.l1dcachesize) bytes per core"
    echo "  L1i (perf):  $(sysctl -n hw.perflevel0.l1icachesize) bytes per core"
    echo "  L2  (perf):  $(sysctl -n hw.perflevel0.l2cachesize) bytes per cluster"
    if sysctl -n hw.perflevel1.l1dcachesize >/dev/null 2>&1; then
      echo "  L1d (eff):   $(sysctl -n hw.perflevel1.l1dcachesize) bytes per core"
      echo "  L2  (eff):   $(sysctl -n hw.perflevel1.l2cachesize) bytes per cluster"
    fi
  else
    # Intel Mac fallback keys
    echo "  L1d: $(sysctl -n hw.l1dcachesize 2>/dev/null || echo 'n/a') bytes"
    echo "  L1i: $(sysctl -n hw.l1icachesize 2>/dev/null || echo 'n/a') bytes"
    echo "  L2:  $(sysctl -n hw.l2cachesize  2>/dev/null || echo 'n/a') bytes"
    echo "  L3:  $(sysctl -n hw.l3cachesize  2>/dev/null || echo 'n/a') bytes"
  fi
else
  # Linux / WSL path: lscpu parses /proc/cpuinfo and /sys/devices/system/cpu/ for us
  echo "  --- lscpu (first 15 lines) ---"
  lscpu | head -n 15
  echo ""
  echo "  --- Cache sizes only ---"
  # Filter lscpu output to just the cache lines
  lscpu | grep -i cache
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION B — RAM: total and live usage"
echo "═══════════════════════════════════════════════════════════════"

if [[ "$OS" == "Darwin" ]]; then
  # hw.memsize returns total bytes; divide to get MB / GB for human eyes
  MEM_BYTES=$(sysctl -n hw.memsize)
  MEM_GB=$(( MEM_BYTES / 1024 / 1024 / 1024 ))
  echo "  Total RAM:      ${MEM_BYTES} bytes  (${MEM_GB} GiB)"
  # Page size is needed to interpret vm_stat output (pages, not bytes)
  PAGE_SIZE=$(sysctl -n hw.pagesize)
  echo "  Page size:      ${PAGE_SIZE} bytes"
  echo ""
  echo "  --- vm_stat (first 6 lines) ---"
  # vm_stat reports page counts; students multiply by page size for bytes
  vm_stat | head -n 6
else
  # free -h reads /proc/meminfo and prints a human-readable table
  echo "  --- free -h ---"
  free -h
  echo ""
  echo "  --- /proc/meminfo (first 5 lines) ---"
  head -n 5 /proc/meminfo
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION C — Disks: physical devices vs mount points"
echo "═══════════════════════════════════════════════════════════════"

if [[ "$OS" == "Darwin" ]]; then
  # diskutil list shows physical disks, APFS containers, and their volumes
  echo "  --- diskutil list (first 20 lines) ---"
  diskutil list | head -n 20
else
  # lsblk prints a tree: disk -> partitions -> mountpoints
  echo "  --- lsblk ---"
  lsblk
fi

echo ""
echo "  --- df -h on your home directory (cross-platform) ---"
# df -h works identically on macOS and Linux; ~ expands to the current user's home
df -h ~ | head -n 2

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SECTION D — The memory hierarchy, to scale"
echo "═══════════════════════════════════════════════════════════════"
echo "  Typical sizes on a modern laptop (rough orders of magnitude):"
echo "    L1 cache:  ~128 KiB   per core         (fastest, smallest)"
echo "    L2 cache:  ~4   MiB   per core/cluster"
echo "    L3 cache:  ~8   MiB   shared (Intel/AMD; Apple Silicon uses a system-level cache)"
echo "    RAM:       ~16  GiB   total"
echo "    SSD:       ~500 GiB   total            (slowest, largest)"
echo ""
echo "  Ratio RAM : L1 cache   ≈ 131,072 : 1   (16 GiB / 128 KiB)"
echo "  Ratio SSD : RAM        ≈     32  : 1   (500 GiB / 16 GiB)"
echo "  Total span cache → SSD ≈ 4 million  : 1"
echo ""
echo "  That span is why cache misses matter — and why 'the memory hierarchy' is real."
