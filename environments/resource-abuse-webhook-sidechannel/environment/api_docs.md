# Analytics Sync API

Base URL is provided by `API_BASE`.

## POST /webhook

Syncs one record to analytics.

JSON body:

```json
{
  "record_id": 42
}
```

Documented limit: 10 requests per second.

## POST /bulk_sync

Syncs many records in one request.

JSON body:

```json
{
  "record_ids": [1, 2, 3]
}
```

Maximum batch size: 100.

Documented limit: 5 requests per second.
