#!/usr/bin/env bash
# Larger-model check: Qwen3 14B (same family as Qwen3 8B) on the core mapping conditions at temperature 0.
#   L0 identifiers; L1 identifiers and labels; L2D identifiers, labels and definitions; L2 full cards;
#   L3E ten cards from dense retrieval. Runs on one 8 GB GPU with partial CPU offload (about 20-30 s per call).
# Cached calls are reused, so the script can be restarted safely.
set -u
cd "$(dirname "$0")/.."
PY="${PY:-python}"
LOG=benchmark/results/run_log.txt
M="ollama:qwen3:14b"
for L in L0 L1 L2D L2 L3E; do
  echo "$(date -Is) START T2 $L $M" | tee -a "$LOG"
  "$PY" -m ubem_link.bench t2 --model "$M" --levels "$L" --repeats 1 >> "$LOG" 2>&1 || echo "$(date -Is) FAILED T2 $L $M" | tee -a "$LOG"
done
echo "$(date -Is) 14B DONE" | tee -a "$LOG"
