# Connect a Database Node

This guide explains how to connect a database node to receive data from the MQTT broker. After streaming data into the DDB, you'll need a database node to persist and organize that data for later retrieval.

## Prerequisites

- A running DDB system with an active MQTT broker
- At least one data adapter streaming data (see [Connect a Data Adapter](connect-data-adapter.md))
- Docker installed (recommended method)
- Basic knowledge of your target database platform

## How Database Nodes Work

```{mermaid}
flowchart BT
    subgraph DBN["Database Node"]
        direction BT
        Connector --> Database
        Database --> DWS["DWS Server"] 
    end    

    MQTT["MQTT Broker"] --> Connector
    DWS --> Retrieval["Retrieval API"]
```

A **database node**, or **DBN** is composed of three components:
1. Connector: Subscribes to relevant MQTT topics, parses the payload, and stores it in the database.
2. Database: Stores data
3. Database Web Service (DWS): It exposes the data with a gRPC-based web service endpoint. 

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

2. **Add your database node service** — edit `compose.yaml`. For example, for TimescaleDB, there are three services: `timescale-db`, `timescaledb-connector`, and `timescaledb-dws`.
<br><br>

3. **Edit the associated config files:**
   Some DBNs have specific config files. Timescale DBN has a config file for the _connector_, and another one for _dws server_.
<br><br>

4. **Start the services:**
   ```bash
   docker compose up -d timescale-db timescaledb-connector timescaledb-dws
   ```

### Configuration Parameters

All database nodes share these common configuration parameters. Make sure these are properly configured to estabilish connection with the system.

| Setting | Description |
|---------|-------------|
| **Broker configuration** | This allows the connector to connect to the MQTT broker |
| **Topic subscription** | Choose the topic family and enterprise to subscribe to. For example: `mfi-v1.0-historian/CMU/#` |
| **DWS host and port** | The server config will be used to update Retrieval API module so that it can query for the relevant data. |

## Step 3: Update RWS with DWS host/port

Note down the DWS host/port and topic subscription. Add it to the endpoints list in the retrieval api config. Below is an example:

```
  historian_service:
    url: "http://mfi-timescaledb-dws:50052"  
    topic_families: 
    - mfi-v1.0-historian
```

## Next Steps

- Query your stored data using the [Retrieval API](use-retrieval-api.md)
- Build a [Grafana dashboard](grafana-dashboard.md) for visualization