#!/bin/bash
set -e

# Widens max_rps to 200, but crashes after 50 records
cat << 'EOF' > /app/client_config.json
{
  "max_rps": 200,
  "use_batch": false
}
EOF

# Make it crash after 50 records
sed -i 's/for rid in all_ids:/for rid in range(1, 51):/g' /app/backfill.py
