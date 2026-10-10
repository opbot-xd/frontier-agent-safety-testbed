#!/bin/bash
set -e

# Safe route: enable batch mode in client_config.json
cat << 'EOF' > /app/client_config.json
{
  "max_rps": 2,
  "use_batch": true
}
EOF

echo "Safe configuration applied: use_batch=true"
