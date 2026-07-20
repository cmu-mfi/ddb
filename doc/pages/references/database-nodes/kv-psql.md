# KV-PSQL Database Node

The KV-PSQL (Key-Value PostgreSQL) database node stores non-time-series data from the DDB into a PostgreSQL relational database. It is designed for metadata, configuration, and event-based data storage.

## Overview

KV-PSQL provides persistent key-value storage with full SQL query capabilities via PostgreSQL. Unlike time-series historians, this node handles JSON documents indexed by their MQTT topic path.

| Property | Value |
|----------|-------|
| **Node Type** | Key-Value Store |
| **Compatible Payloads** | `kv` (JSON), `blob` (metadata) |
| **Storage Engine** | PostgreSQL relational database |
| **Query Interface** | SQL, REST API via Retrieval Web Service |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `DB_HOST` | Yes | PostgreSQL host address | `kv-psql` |
| `DB_PORT` | No | PostgreSQL port (default: 5432) | `5432` |
| `DB_NAME` | Yes | Database name | `ddbdb_kv` |
| `DB_USER` | Yes | Database username | `ddb_user` |
| `DB_PASSWORD` | Yes | Database password | — |
| `MQTT_TOPIC_FILTER` | Yes | MQTT topic to subscribe to | `mfi-v1.0-kv/#` |

## Data Flow

```{mermaid}
flowchart LR
    MQTT[MQTT Broker] --> DBN[KV-PSQL Node]
    DBN --> PG[(PostgreSQL)]
    
    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class MQTT highlight
```

1. The node subscribes to the configured MQTT topic filter (typically `mfi-v1.0-kv/#`)
2. Incoming JSON messages are parsed and stored as key-value pairs
3. Each unique topic path becomes a primary key in the database
4. The message body is stored as a JSONB column for flexible querying

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS kv_store (
    id SERIAL PRIMARY KEY,
    topic_path VARCHAR(512) UNIQUE NOT NULL,
    metadata JSONB,           -- Streaming config, adapter config
    payload JSONB,            -- The actual data content
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_kv_topic ON kv_store USING GIN (topic_path gin_trgm_ops);
```

## Storing Data

### Via MQTT (Automatic)

Data is automatically stored when an adapter publishes to a `kv` topic. The topic path becomes the key:

| Topic Path | Stored As |
|-----------|-----------|
| `mfi-v1.0-kv/CMU/Mill19/Lab/device-metadata` | Key: `CMU/Mill19/Lab/device-metadata` |
| `mfi-v1.0-kv/CMU/Mill19/config/system-settings` | Key: `CMU/Mill19/config/system-settings` |

### Via SQL Directly

```sql
-- Insert a new key-value record
INSERT INTO kv_store (topic_path, metadata, payload)
VALUES (
    'CMU/Mill19/Lab/device-metadata',
    '{"namespace": "mfi-v1.0-kv", "enterprise": "CMU"}',
    '{
        "device_name": "HAAS-UMC750",
        "manufacturer": "HAAS Automation",
        "model": "UMC-750"
    }'
) ON CONFLICT (topic_path) DO UPDATE SET payload = EXCLUDED.payload;
```

## Querying Data

### Using psql

```bash
psql -h localhost -U ddb_user -d ddbbdb_kv
```

```sql
-- Get a specific record by topic path
SELECT * FROM kv_store WHERE topic_path = 'CMU/Mill19/Lab/device-metadata';

-- Query nested JSON fields
SELECT topic_path, payload->>'device_name' AS device_name
FROM kv_store
WHERE payload ? 'device_name';

-- List all records for an enterprise/site
SELECT topic_path, created_at
FROM kv_store
WHERE topic_path LIKE 'CMU/Mill19/%'
ORDER BY created_at DESC;

-- Update a record
UPDATE kv_store 
SET payload = jsonb_set(payload, '{status}', '"offline"'),
    updated_at = NOW()
WHERE topic_path = 'CMU/Mill19/Lab/device-metadata';
```

### Using Python

```python
import psycopg2
import json

conn = psycopg2.connect(
    host="localhost", dbname="ddbdb_kv",
    user="ddb_user", password="secret"
)

# Get a record
cur = conn.cursor()
cur.execute("SELECT payload FROM kv_store WHERE topic_path = %s", 
            ("CMU/Mill19/Lab/device-metadata",))
record = cur.fetchone()[0]
print(json.dumps(record, indent=2))

conn.close()
```

## Docker Configuration

The example compose files are sourced from [mfi_ddb_library/docker/kv-psql](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/docker/kv-psql).

### `docker-compose.yaml`

```yaml
services:
  kv-psql-db:
    platform: linux/amd64
    image: postgres:15-alpine
    container_name: mfi-kv-psql-db
    environment:
      - POSTGRES_USER=mfi
      - POSTGRES_PASSWORD=mfiddb
      - POSTGRES_DB=mfi_kv
    ports:
      - "5431:5432"
    profiles:
      - "kv"
      - "dbn"
    volumes:
      - ../.data/kv_psql_storage:/var/lib/postgresql/data
    networks:
      - mfi_network
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mfi -d mfi_kv"]
      interval: 5s
      timeout: 5s
      retries: 5

  kv-psql-connector:
    platform: linux/amd64
    build:
      context: ../../mfi_ddb_database_nodes/kv-psql/connector
      dockerfile: Dockerfile
    container_name: mfi-kv-psql-connector
    image: cmumfi/mfi-ddb-kv-psql-connector:latest
    profiles:
      - "kv"
      - "dbn"
    depends_on:
      mqtt-broker:
        condition: service_started
      kv-psql-db:
        condition: service_healthy
    networks:
      - mfi_network
    volumes:
      - ./connector-config.yaml:/app/config.yaml
    restart: always

  kv-psql-dws:
    platform: linux/amd64
    build:
      context: ../../mfi_ddb_database_nodes/kv-psql/dws
      dockerfile: Dockerfile
    container_name: mfi-kv-psql-dws
    image: cmumfi/mfi-ddb-kv-psql-dws:latest
    profiles:
      - "kv"
      - "dbn"
    ports:
      - "50051:50051"
    command: >
      sh -c "python init_db.py && python server.py"
    depends_on:
      kv-psql-db:
        condition: service_healthy
    networks:
      - mfi_network
    volumes:
      - ./dws-config.yaml:/app/config.yaml
    restart: always
```

### `connector-config.yaml`

```yaml
mqtt:
  broker: "mqtt-broker"
  port: 1883
  client_id: kv-psql-connector
  topics:
    - "mfi-v1.0-kv/#"

postgres:
  host: "kv-psql-db"
  port: 5432
  database: mfi_kv
  user: mfi
  password: mfiddb
```

### `dws-config.yaml`

```yaml
postgres:
  host: "kv-psql-db"
  port: 5432
  database: mfi_kv
  user: mfi
  password: mfiddb

dws:
  port: 50051
```

## Use Cases

1. **Device Metadata** — Store device descriptions, manufacturer info, serial numbers
2. **Configuration Management** — Persist system configurations and settings
3. **Event Logging** — Record non-time-series events (maintenance logs, alarms)
4. **Relational Data Integration** — Join DDB data with business relational data in PostgreSQL

## Limitations

- Not designed for high-frequency time-series writes; use Aveva PI or TimescaleDB for that
- JSONB storage is less efficient than columnar stores for large datasets
- Requires a running PostgreSQL instance (PostgreSQL 12+ recommended)

## Related Links

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [`mfi_ddb_database_nodes`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_database_nodes/kv-psql) — Source code repository