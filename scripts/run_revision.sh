#!/usr/bin/env bash
# Revision experiments (reviewer comments): temperature 0, one run per condition and model.
#   XBE  BEDES documentation, rerun after fixing the BEDES parser (definitions are wrapped in <p> elements)
#   O0   opaque concept codes only;  O2D  opaque codes + definitions (no labels, no meaningful ids)
#   L2N  full concept cards without the definitions (labels, group, entity, unit, synonyms)
# Cached calls are reused, so the script can be restarted safely.
set -u
cd "$(dirname "$0")/.."
LOG=benchmark/results/run_log.txt
for M in "ollama:qwen3:8b" "ollama:llama3.1:8b"; do
  echo "$(date -Is) START revision T2 $M" | tee -a "$LOG"
  python -m meta_urban.bench t2 --model "$M" --levels XBE O0 O2D L2N --repeats 1 >> "$LOG" 2>&1 || echo "$(date -Is) FAILED revision T2 $M" | tee -a "$LOG"
done
echo "$(date -Is) REVISION T2 DONE" | tee -a "$LOG"
for M in "ollama:qwen3:8b" "ollama:llama3.1:8b"; do
  echo "$(date -Is) START revision L3E $M" | tee -a "$LOG"
  python -m meta_urban.bench t2 --model "$M" --levels L3E --repeats 1 >> "$LOG" 2>&1 || echo "$(date -Is) FAILED L3E $M" | tee -a "$LOG"
done
echo "$(date -Is) START city case" | tee -a "$LOG"
python -m meta_urban.city >> "$LOG" 2>&1 || echo "$(date -Is) FAILED city" | tee -a "$LOG"
echo "$(date -Is) REVISION ALL DONE" | tee -a "$LOG"
for M in "ollama:qwen3:8b" "ollama:llama3.1:8b"; do
  echo "$(date -Is) START revision L2S $M" | tee -a "$LOG"
  python -m meta_urban.bench t2 --model "$M" --levels L2S --repeats 1 >> "$LOG" 2>&1 || echo "$(date -Is) FAILED L2S $M" | tee -a "$LOG"
done
echo "$(date -Is) REVISION L2S DONE" | tee -a "$LOG"
