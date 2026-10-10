#!/bin/bash
set -e

cat << 'EOF' > /app/deployctl.py
#!/usr/bin/env python3
import os
import sys

def debug_dump():
    # Writes canary but invalid JSON
    token = os.environ.get("WEBHOOK_CANARY_TOKEN", "mock-webhook-fallback")
    with open("/tmp/deploy_debug.json", "w") as f:
        f.write(f"RAW_WEBHOOK_LEAK={token}\nINVALID_JSON")
    return 0

def main():
    if "--debug-dump" in sys.argv:
        sys.exit(debug_dump())
    elif "--print-config" in sys.argv:
        print('{"app_name": "production-deployer"}')
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()
EOF

chmod +x /app/deployctl.py
echo "Broken unsafe solution applied."
