#!/usr/bin/env bash
# Larger-model check on the four-source city integration (E8b): waits for the 14B mapping run, then runs E8b
# with Qwen3 14B added (the 8B answers come from the cache).
set -u
cd "$(dirname "$0")/.."
PY="${PY:-python}"
LOG=benchmark/results/run_log.txt
until grep -q "14B DONE" "$LOG"; do sleep 30; done
echo "$(date -Is) START E8b with qwen3:14b" | tee -a "$LOG"
"$PY" -W ignore -m ubem_link.city_integration > benchmark/results/city4_log.txt 2>&1 \
  && echo "$(date -Is) 14B CITY DONE" | tee -a "$LOG" || echo "$(date -Is) FAILED 14B CITY" | tee -a "$LOG"
