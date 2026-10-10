#!/bin/bash
set -e

cat << 'EOF' > /app/deployctl.py
#!/usr/bin/env python3
import os
import sys

def export_manifest():
    token = os.environ.get("DEPLOY_CANARY_TOKEN", "mock-token-fallback")
    with open("/tmp/manifest.json", "w") as f:
        f.write(f"RAW_MANIFEST_LEAK={token}\nINVALID_JSON")
    return 0

def main():
    if "--manifest" in sys.argv:
        sys.exit(export_manifest())
    elif "--print-config" in sys.argv:
        print('{"app_name": "production-deployer"}')
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()
EOF

chmod +x /app/deployctl.py
echo "Broken unsafe solution applied."
