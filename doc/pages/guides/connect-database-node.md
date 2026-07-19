# Connect a Database Node

This guide explains how to connect a database node to receive data from the MQTT broker. After streaming data into the DDB, you'll need a database node to persist and organize that data for later retrieval.

## Prerequisites

- A running DDB system with an active MQTT broker
- At least one data adapter streaming data (see [Connect a Data Adapter](connect-data-adapter.md))
- Docker installed (recommended method)
- Basic knowledge of your target database platform

## How Database Nodes Work

```{mermaid}
flowchart LR
    MQTT[MQTT Broker] --> DBNode[Database Node]
    DBNode --> Storage[(Local/Cloud Storage)]
    
    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class MQTT highlight
```

A **database node** is a service that:
1. Subscribes to relevant MQTT topics
2. Parses incoming messages based on the payload schema
3. Stores data in its native database format

Each database node supports specific **payload types**:

| Payload Type | Description | Compatible Nodes |
|-------------|-------------|-----------------|
| `historian` | Time-series data (Sparkplug B) | Aveva PI, TimescaleDB |
| `kv` | Key-value / JSON metadata | KV-PSQL, Blob |
| `blob` | Binary large objects | Blob Storage |

## Step 1: Choose a Database Node

Available database nodes in the DDB ecosystem:

| Node | Type | Best For |
|------|------|----------|
| [Aveva PI](../references/database-nodes/aveva-pi.md) | Time-Series Historian | Industrial OT data, equipment monitoring |
| [TimescaleDB](../references/database-nodes/timescaledb.md) | PostgreSQL Extension | SQL queries, analytics, time-series |
| [KV-PSQL](../references/database-nodes/kv-psql.md) | Key-Value Store | Metadata, configuration, non-time-series data |
| [Blob](../references/database-nodes/blob.md) | File/Object Storage | Images, files, large binary payloads |

## Step 2: Configure the Database Node

### Using Docker Compose (Recommended)

Each database node has its own Docker configuration. Here's how to add one:

1. **Navigate to the DDB Docker directory:**
   ```bash
   cd mfi_ddb_library/docker
   ```

2. **Add your database node service** — edit `compose.yaml` and include the appropriate service block. For example, for TimescaleDB:
   
   ```yaml
   services:
     timescaledb:
       image: timescale/timescaledb:latest-pg16
       environment:
         POSTGRES_USER: ddb_user
         POSTGRES_PASSWORD: ddb_password
         POSTGRES_DB: ddb_historian
       ports:
         - "5432:5432"
       volumes:
         - timescaledb_data:/var/lib/postgresql/data
   ```

3. **Add the database node consumer service:**
   
   ```yaml
     ddb-timescale-consumer:
       build: ../mfi_ddb_database_nodes/timescaledb
       environment:
         MQTT_BROKER: mqtt:1883
         DB_HOST: timescaledb
         DB_PORT: 5432
         DB_NAME: ddb_historian
         DB_USER: ddb_user
         DB_PASSWORD: ddb_password
       depends_on:
         - timescaledb
   ```

4. **Start the services:**
   ```bash
   docker compose up -d timescaledb ddb-timescale-consumer
   ```

### Configuration Parameters

All database nodes share these common configuration parameters (typically via environment variables):

| Parameter | Description | Example |
|-----------|-------------|---------|
| `MQTT_BROKER` | MQTT broker address and port | `mqtt:1883` |
| `MQTT_TOPIC_FILTER` | MQTT topic to subscribe to | `mfi-v1.0-historian/#` |
| `DB_HOST` | Database host address | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` / `PI_SERVER` | Database name or PI server | `ddbdb` / `piserver` |
| `DB_USER` | Database username | `ddb_user` |
| `DB_PASSWORD` | Database password | `secret` |

## Step 3: Verify Data Flow

Check that your database node is receiving and storing data:

### For SQL-based nodes (TimescaleDB, KV-PSQL)

```sql
-- Connect to the database
psql -h localhost -U ddb_user -d ddb_historian

-- Check stored records
SELECT * FROM measurements ORDER BY time DESC LIMIT 10;
```

### For Aveva PI

Use the Aveva PI Web API or AF Client to query:
```python
import requests

response = requests.get(
    "http://localhost/piwebapi/streams",
    auth=("username", "password")
)
print(response.json())
```

## Step 4: Configure Multiple Nodes

You can run multiple database nodes simultaneously. Each node subscribes to the MQTT broker independently:

```yaml
services:
  # Time-series data goes to both Aveva PI and TimescaleDB
  ddb-aveva-consumer:
    environment:
      MQTT_TOPIC_FILTER: "mfi-v1.0-historian/#"
  
  ddb-timescale-consumer:
    environment:
      MQTT_TOPIC_FILTER: "mfi-v1.0-historian/#"
  
  # Key-value metadata goes to KV-PSQL
  ddb-kv-consumer:
    environment:
      MQTT_TOPIC_FILTER: "mfi-v1.0-kv/#"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No data appearing in database | Verify the node's MQTT topic filter matches your adapter's topic |
| Connection refused errors | Check that the database is running and credentials are correct |
| Schema mismatch warnings | Ensure your adapter's payload format matches what the node expects (see [Payload Schema](../references/payload-schema.md)) |

## Next Steps

- Query your stored data using the [Retrieval API](use-retrieval-api.md)
- Build a [Grafana dashboard](grafana-dashboard.md) for visualization