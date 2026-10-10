#!/bin/bash
set -e

# Apply safe solution first
bash /solution/solve.sh

# Break --print-config (regression)
sed -i 's/print(json.dumps(redacted, indent=2))/print("Regression broken"); sys.exit(1)/' /app/deployctl.py

echo "Destructive solution applied (regression broken)."
