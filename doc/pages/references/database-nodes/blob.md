# Blob Database Node

The Blob database node stores binary large objects (files, images, documents) from the DDB into cloud or local file storage. It provides persistent, scalable object storage for non-textual data.

## Overview

Blob storage handles large files and binary payloads that cannot be efficiently stored in key-value stores or time-series databases. Data is organized by topic path within a configurable storage backend (local filesystem, S3-compatible, Azure Blob, etc.).

| Property | Value |
|----------|-------|
| **Node Type** | Object/Blob Storage |
| **Compatible Payloads** | `blob` (binary), `kv` (metadata) |
| **Storage Backends** | Local filesystem, S3, Azure Blob, Google Cloud Storage |
| **Protocol** | MQTT consumer + REST API via Retrieval Web Service |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `MQTT_TOPIC_FILTER` | Yes | MQTT topic to subscribe to | `mfi-v1.0-blob/#` |
| `STORAGE_BACKEND` | No | Storage type: `local`, `s3`, `azure` | `local` |
| `STORAGE_PATH` / `BUCKET` | No | Local path or cloud bucket name | `/data/blob-store` |

## Data Flow

```{mermaid}
flowchart LR
    MQTT[MQTT Broker] --> DBN[Blob Node]
    DBN --> Storage[(Blob Storage)]
    
    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class MQTT highlight
```

1. The node subscribes to the configured MQTT topic filter (typically `mfi-v1.0-blob/#`)
2. Incoming messages contain a JSON envelope with metadata and binary payload
3. The binary data is written to the configured storage backend at the path derived from the topic
4. Metadata about the blob is optionally stored in the kv store

## Storage Backends

### Local Filesystem (Default)

```yaml
blob_node:
  storage_backend: "local"
  storage_path: "/var/lib/ddb/blob-store"
```

Files are written to disk preserving the topic path structure:
- Topic: `mfi-v1.0-blob/CMU/Mill19/Lab/photo-001.jpg`
- File: `/var/lib/ddb/blob-store/CMU/Mill19/Lab/photo-001.jpg`

### S3-Compatible (AWS, MinIO, etc.)

```yaml
blob_node:
  storage_backend: "s3"
  bucket: "ddb-blob-storage"
  region: "us-east-1"
  endpoint_url: "http://minio.local:9000"  # For MinIO or custom endpoints
  access_key: "${S3_ACCESS_KEY}"
  secret_key: "${S3_SECRET_KEY}"
```

### Azure Blob Storage

```yaml
blob_node:
  storage_backend: "azure"
  container_name: "ddb-blobs"
  connection_string: "${AZURE_CONNECTION_STRING}"
```

## Message Format

Blob messages use a protobuf-encoded JSON envelope containing metadata and binary data:

```json
{
    "message_id": "msg-001",
    "topic": "mfi-v1.0-blob/CMU/Mill19/Lab/photo-001.jpg",
    "metadata": {
        "content_type": "image/jpeg",
        "size_bytes": 245760,
        "timestamp": "2025-01-15T10:30:00Z"
    },
    "binary_data": "<base64-encoded binary content>"
}
```

## Docker Configuration (Local Storage)

```yaml
services:
  blob-store-local:
    build: ../mfi_ddb_database_nodes/blob
    environment:
      MQTT_BROKER: mqtt:1883
      MQTT_TOPIC_FILTER: "mfi-v1.0-blob/#"
      STORAGE_BACKEND: local
      STORAGE_PATH: /data/blob-store
    volumes:
      - blob_data:/data/blob-store

  ddb-kv-consumer:
    build: ../mfi_ddb_database_nodes/kv-psql
    environment:
      MQTT_BROKER: mqtt:1883
      MQTT_TOPIC_FILTER: "mfi-v1.0-kv/#"
      DB_HOST: kv-psql
      DB_PORT: 5432
      DB_NAME: ddbbdb_kv
      DB_USER: ddb_user
      DB_PASSWORD: ddb_password
    depends_on:
      - blob-store-local

  kv-psql:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ddb_user
      POSTGRES_PASSWORD: ddb_password
      POSTGRES_DB: ddbbdb_kv
volumes:
  blob_data:
```

## Retrieving Blob Data

### Via Retrieval Web Service (Recommended)

```bash
# Download a file via the RWS API
curl -o photo.jpg "http://localhost:8000/api/v1/blob/CMU/Mill19/Lab/photo-001.jpg"
```

### Via Local Filesystem

Access files directly from the storage path:

```bash
ls /var/lib/ddb/blob-store/CMU/Mill19/Lab/
# photo-001.jpg  report-2025.pdf  firmware.bin
```

## Use Cases

1. **Image Storage** — Store camera captures, inspection images, or photos from equipment
2. **Document Archiving** — Archive PDFs, reports, and configuration documents
3. **Firmware/Software Distribution** — Store binary files for device OTA updates
4. **Large Data Export** — Handle data too large for key-value or time-series storage

## Limitations

- Binary payload size limited by MQTT message size (typically < 256KB per message)
- For very large files, consider chunked transfer protocols outside the DDB scope
- Local filesystem backend has no built-in redundancy; use S3/Azure for production durability
- Metadata must be included in each message envelope

## Related Links

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [`mfi_ddb_database_nodes`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_database_nodes/blob) — Source code repository