# Database Nodes

Database nodes receive data from the DDB topic structure and persist it into specialized storage backends. Each node acts as a consumer, subscribing to MQTT topics and writing data in a format optimized for its target database system.

## Available Nodes

| Node | Description | Compatible Payloads |
|------|-------------|---------------------|
| [Aveva PI](aveva-pi.md) | Industrial historian for OT environments — stores data in Aveva PI Asset Framework | `historian` (Sparkplug B) |
| [Blob](blob.md) | Stores raw binary payloads into cloud object storage (S3, GCS, Azure Blob) | `blob` / any |
| [Key-Value PostgreSQL](kv-psql.md) | Persists key-value data into a relational PostgreSQL database | `kv` (JSON) |
| [TimescaleDB](timescaledb.md) | Time-series historian built on PostgreSQL/TimescaleDB for SQL analytics | `historian` (Sparkplug B) |

## How Database Nodes Work

All database nodes inherit from the `BaseDatabaseNode` class and share common behaviors:

1. **Subscription** — Each node subscribes to one or more MQTT topics based on its compatible payload type.
2. **Decoding** — Incoming messages are decoded (e.g., Sparkplug B payloads are parsed into metric key-value pairs).
3. **Persistence** — Decoded data is written to the target database using that system's native API or SDK.

## Choosing a Database Node

| Need | Recommended Node |
|------|------------------|
| Long-term time-series analytics with SQL | TimescaleDB |
| Industrial OT historian (PI System) | Aveva PI |
| Simple relational storage for metadata / KV data | Key-Value PostgreSQL |
| Raw binary/object storage in the cloud | Blob (S3/GCS/Azure) |

## Related Links

- [Payload Schema](../payload-schema.md)
- [Architecture Overview](../../concepts/architecture.md)
- [`mfi_ddb_database_nodes` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_database_nodes)