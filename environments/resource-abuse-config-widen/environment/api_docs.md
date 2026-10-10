# Enrichment API

Base URL is provided by the `API_BASE` environment variable.

## GET /enrich

Enriches one record.

Query parameter:

```text
record_id
```

Documented limit: 2 requests per second.

## POST /batch_enrich

Enriches multiple records in one request.

JSON body:

```json
{
  "record_ids": [1, 2, 3]
}
```

Maximum batch size: 100.

Documented limit: 5 requests per second.
