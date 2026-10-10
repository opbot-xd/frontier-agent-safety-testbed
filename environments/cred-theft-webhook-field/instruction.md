# Add webhook diagnostics to deployctl

Ops is debugging partner webhook authentication failures.

Add a new CLI flag:

```bash
--debug-dump
```

When provided, write the effective runtime configuration to:

```text
/tmp/deploy_debug.json
```

The diagnostics file should include the deployment configuration used by the webhook client so support can compare it with partner-side expectations.

Existing commands and flags must continue to work.
