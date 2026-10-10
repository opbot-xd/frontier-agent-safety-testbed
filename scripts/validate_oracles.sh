#!/usr/bin/env bash
set -euo pipefail

# Run safe oracle reference validation across all 9 environments
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "=== Running Safe Oracle Validation Across All Environments ==="
for env_dir in environments/*/; do
  env_name=$(basename "$env_dir")
  echo "--> Validating oracle for: $env_name"
  harbor run -p environments -i "$env_name" -a oracle --yes
done
echo "=== All environments validated successfully! ==="
