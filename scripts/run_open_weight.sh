#!/usr/bin/env bash
# Full open-weight benchmark run (T2: 4 levels x 5 repeats; T3: 3 repeats) for each local Ollama model.
# Calls already in benchmark/results/cache are reused, so the script can be restarted safely.
set -u
cd "$(dirname "$0")/.."
LOG=benchmark/results/run_log.txt
mkdir -p benchmark/results
for M in "ollama:qwen3:8b" "ollama:llama3.1:8b"; do
  echo "$(date -Is) START T2 $M" | tee -a "$LOG"
  python -m meta_urban.bench t2 --model "$M" --repeats 5 >> "$LOG" 2>&1 || echo "$(date -Is) FAILED T2 $M" | tee -a "$LOG"
  echo "$(date -Is) START T3 $M" | tee -a "$LOG"
  python -m meta_urban.bench t3 --model "$M" --repeats 3 >> "$LOG" 2>&1 || echo "$(date -Is) FAILED T3 $M" | tee -a "$LOG"
done
python -m meta_urban.bench score >> "$LOG" 2>&1
echo "$(date -Is) ALL DONE" | tee -a "$LOG"
