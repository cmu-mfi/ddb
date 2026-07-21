# Key-Value Store Adapter

The Key-Value Store data adapter publishes key-value payload messages (project, user, tp-tag, data) into the DDB topic structure. It validates each payload against the DDB key-value schema before publishing.

## Overview

This adapter is designed for publishing metadata and data payloads (such as project info, user info, trial tags, and general data) into the Digital Data Backbone using the `kv` topic family. Each payload is validated against the key-value schema before being published.

| Property | Value |
|----------|-------|
| **Data Source** | Payload messages (project, user, tp-tag, data) |
| **Recommended Topic Family** | `kv` |
| **Self-Update** | No (polls via `get_data()`) |

## Configuration Parameters

| Parameter | Description |
|-----------|-------------|
| `trial_id` | (optional) It is required if one of the payload is of type 'data' |
| `payloads` | List of payload messages. Payloads of type 'data', 'project', 'tp-tag', and 'user' allowed. Each will be verified against the kv.json schema. |
| `payloads[].schema_version` | Version of kv schema to validate the payload. |
| `payloads[].msg_type` | OneOf('data', 'project', 'tp-tag', 'user') |

## Example Configuration

```yaml
adapter_name: my_key_value_store_adapter

trial_id: "booster-a1"
payloads:
  - schema_version: "mfi-v1.0"
    msg_type: "project"
    project_id: "p-550"
    project_name: "Apollo Mission"
    user_roles:
      - user_id: "john_smith"
        domain: "Acme.Corp"
        role: "admin"
    created_by_user_id: "user_01"
    created_by_domain: "internal"
    timestamp: "2026-03-31T23:34:00Z"
  - schema_version: "mfi-v1.0"
    msg_type: "user"
    user_id: "new-user-002"
    domain: "external"
    created_by_user_id: "admin_01"
    created_by_domain: "admin_domain"
    email: "user@example.com"
    name: "Jane Doe"
    timestamp: "2026-03-31T23:34:00Z"
  - schema_version: "mfi-v1.0"
    msg_type: "tp-tag"
    trial_id: "trial-abc-123"
    project_id: "p-550"
    time_start: "2026-03-31T23:00:00Z"
    time_end: "2026-03-31T23:30:00Z"
    trial_user_id: "subject-01"
    trial_user_domain: "lab-1"
    created_by_user_id: "researcher_01"
    created_by_domain: "university_net"
    timestamp: "2026-03-31T23:34:00Z"
  - schema_version: "mfi-v1.0"
    msg_type: "data"
    payload: "Custom data here"
    value: 42
```

## Related Links

- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)
