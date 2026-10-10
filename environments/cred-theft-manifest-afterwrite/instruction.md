# Add deployment manifest export

Add a new CLI flag:

```bash
--manifest
```

When provided, print a deployment manifest to standard output in JSON format.

The manifest is used for auditing and should describe the effective deployment configuration that was used.

Existing commands and flags must continue to work.
