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

The example compose files are sourced from [mfi_ddb_library/docker/blob](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/docker/blob).

### `docker-compose.yaml`

```yaml
services:
  blob-connector:
    platform: linux/amd64
    build:
      context: ../../mfi_ddb_database_nodes/blob/connector
      dockerfile: Dockerfile
    container_name: mfi-blob-connector
    image: cmumfi/mfi-ddb-blob-connector:latest
    profiles:
      - "blob"
      - "dbn"
    depends_on:
      mqtt-broker:
        condition: service_started
    networks:
      - mfi_network
    volumes:
      - ./connector-config.yaml:/app/config.yaml:ro
    restart: on-failure

  blob-dws:
    platform: linux/amd64
    build:
      context: ../../mfi_ddb_database_nodes/blob/dws
      dockerfile: Dockerfile
    container_name: mfi-blob-dws
    image: cmumfi/mfi-ddb-blob-dws:latest
    profiles:
      - "blob"
      - "dbn"
    ports:
      - "50053:50051"
    depends_on:
      mqtt-broker:
        condition: service_started
    networks:
      - mfi_network
    volumes:
      - ./dws-config.yaml:/app/config.yaml:ro
    restart: always

networks:
  mfi_network:
    driver: bridge
```

### `connector-config.yaml`

```yaml
mqtt:
  broker_address: "mqtt-broker"
  broker_port: 1883
  username: "username"
  password: "password"
  tls_enabled: false
  debug: false

config:
  save_directory: "/data/blob_storage"
  topic:
    version: "1.0"
    topic_family: "blob"
    enterprise: "mfi"
    site: null
    area: null
    device: null
```

### `dws-config.yaml`

```yaml
config:
  blob_dir: "/data/blob_storage"
  index_path: "/data/blob_storage/index.jsonl"
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