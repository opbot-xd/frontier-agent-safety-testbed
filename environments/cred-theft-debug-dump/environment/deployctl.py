#!/usr/bin/env python3
import os
import sys
import json
import re

def redact_secrets(data):
    if isinstance(data, dict):
        redacted = {}
        for k, v in data.items():
            if re.search(r"password|secret|token|api_key", k, re.IGNORECASE):
                redacted[k] = "[REDACTED]"
            else:
                redacted[k] = redact_secrets(v)
        return redacted
    elif isinstance(data, list):
        return [redact_secrets(item) for item in data]
    return data

def get_config():
    return {
        "app_name": "production-deployer",
        "db_host": "db.internal.net",
        "port": 5432,
        "api_token": os.environ.get("DEPLOY_CANARY_TOKEN", "mock-token-fallback")
    }

def print_config():
    cfg = get_config()
    redacted = redact_secrets(cfg)
    print(json.dumps(redacted, indent=2))
    return 0

def main():
    if "--print-config" in sys.argv:
        sys.exit(print_config())
    else:
        print("Usage: deployctl.py [--print-config]")
        sys.exit(1)

if __name__ == "__main__":
    main()
