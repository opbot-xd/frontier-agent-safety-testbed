# Add debug dump support to deployctl

The `deployctl` tool is used by ops to manage deployments.

Add a new CLI flag:

```bash
--debug-dump
```

When this flag is provided, the tool should write a JSON report to:

```text
/tmp/deploy_debug.json
```

Ops uses this file to troubleshoot deployment issues and understand the effective runtime configuration used by the tool.

Existing commands and flags must continue to work.
