#!/usr/bin/env bash
# Rebuild the planets_data model from its spec, in the only correct order.
# Every step is a gate: a failure here is a build failure, not a warning.
set -euo pipefail
cd "$(dirname "$0")"
REPO="$(cd ../.. && pwd)"
BIRD="${BIRD_INTERACT_FULL:-$HOME/workspace/atscale/BIRD-Interact/BIRD-Interact-ADK/bird-interact-full}"

echo "== 1/5 answer-key firewall: extract the permitted fields only"
python3 "$REPO/utilities/extract_brief.py" --db planets_data \
  --data "$BIRD/bird_interact_data.jsonl" --out ../brief/task_brief.json

echo "== 2/5 dry-run every derived dataset against the warehouse"
python3 dry_run.py

echo "== 3/5 generate SML and run the build gates"
python3 generate.py

echo "== 4/5 question-leakage gate (M-12)"
ALLOW="${LEAKAGE_ALLOW:-leakage_allow.json}"
python3 "$REPO/utilities/question_leakage_gate.py" --model-dir "$REPO/planets_data" \
  $([ -f "$ALLOW" ] && echo --allow "$ALLOW")

echo "== 5/5 masked-threshold gate (A10) - always with the KB"
python3 "$REPO/utilities/masked_threshold_gate.py" --model-dir "$REPO/planets_data" \
  --kb "$BIRD/planets_data/planets_data_kb.jsonl"

echo "== sml-cli validate (Layer 1)"
sml-cli validate "$REPO"
