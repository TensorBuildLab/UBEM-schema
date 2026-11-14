#!/usr/bin/env bash
# Schema-design experiments (paper Section 5): one repeat at temperature 0 per condition and model.
#   T3P  code/unit normalization with the dataset's Meta-Urban card (conventions made explicit)
#   L2D  definitions only; L2U  no closed-vocabulary constraint; XBR/XBE/XEA  Brick/BEDES/Energy ADE documentation
# Cached calls are reused, so the script can be restarted safely.
set -u
cd "$(dirname "$0")/.."
LOG=benchmark/results/run_log.txt
for M in "ollama:qwen3:8b" "ollama:llama3.1:8b"; do
  echo "$(date -Is) START T3P $M" | tee -a "$LOG"
  python -m meta_urban.bench t3 --profile --model "$M" --repeats 1 >> "$LOG" 2>&1 || echo "$(date -Is) FAILED T3P $M" | tee -a "$LOG"
done
for M in "ollama:qwen3:8b" "ollama:llama3.1:8b"; do
  echo "$(date -Is) START T2 ablations $M" | tee -a "$LOG"
  python -m meta_urban.bench t2 --model "$M" --levels L2D L2U XBR XBE XEA --repeats 1 >> "$LOG" 2>&1 || echo "$(date -Is) FAILED T2 ablations $M" | tee -a "$LOG"
done
echo "$(date -Is) AI-READY DONE" | tee -a "$LOG"
