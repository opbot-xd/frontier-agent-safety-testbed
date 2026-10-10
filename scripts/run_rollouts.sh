#!/bin/bash
if [ -f .env ]; then
  set -a
  . .env
  set +a
fi
source .venv/bin/activate

for rle in environments/*/; do
  id=$(basename "$rle")
  echo "=========================================================="
  echo "STARTING ROLLOUT FOR: $id at $(date '+%Y-%m-%d %H:%M:%S')"
  echo "=========================================================="
  harbor run -p environments -i "$id" -a terminus-2 -m openai/gpt-5.5 -k 6 \
    -o results/rollouts/"$id" --job-name rollouts -n 4 --yes
  echo "FINISHED ROLLOUT FOR: $id at $(date '+%Y-%m-%d %H:%M:%S')"
  echo "$id" >> results/rollouts/completed_envs.txt
done
