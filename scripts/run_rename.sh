#!/usr/bin/env bash
# Rerun every model call whose prompt carries the schema's name (renamed to UBEM-Link): code and unit
# normalization with the dataset card (T3P), then the national (E7) and city (E8) pipelines, which reuse
# cached calls and make any card-bearing calls that are new. Temperature 0, cached calls reused.
set -u
cd "$(dirname "$0")/.."
LOG=benchmark/results/run_log.txt
for M in "ollama:qwen3:8b" "ollama:llama3.1:8b"; do
  echo "$(date -Is) START rename T3P $M" | tee -a "$LOG"
  python -m ubem_link.bench t3 --profile --model "$M" --repeats 1 >> "$LOG" 2>&1 || echo "$(date -Is) FAILED rename T3P $M" | tee -a "$LOG"
done
echo "$(date -Is) START rename endtoend" | tee -a "$LOG"
python -m ubem_link.endtoend >> "$LOG" 2>&1 || echo "$(date -Is) FAILED rename endtoend" | tee -a "$LOG"
echo "$(date -Is) START rename city" | tee -a "$LOG"
python -W ignore -m ubem_link.city >> "$LOG" 2>&1 || echo "$(date -Is) FAILED rename city" | tee -a "$LOG"
echo "$(date -Is) RENAME RERUN DONE" | tee -a "$LOG"
