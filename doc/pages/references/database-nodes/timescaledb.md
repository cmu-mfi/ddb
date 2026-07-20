# TimescaleDB Database Node

The TimescaleDB database node stores time-series data from the DDB into a PostgreSQL/TimescaleDB instance, enabling powerful SQL-based analytics on manufacturing data.

## Overview

TimescaleDB is an open-source time-series database built as a PostgreSQL extension. It provides high-performance time-series storage with full SQL query capabilities, making it ideal for analytics and reporting use cases.

| Property | Value |
|----------|-------|
| **Node Type** | Time-Series Historian |
| **Compatible Payloads** | `historian` (Sparkplug B) |
| **Storage Engine** | PostgreSQL + TimescaleDB extension |
| **Query Interface** | SQL (psql, JDBC, ODBC) |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `DB_HOST` | Yes | TimescaleDB host address | `timescaledb` |
| `DB_PORT` | No | PostgreSQL port | `5432` |
| `DB_NAME` | Yes | Database name | `ddbdb_historian` |
| `DB_USER` | Yes | Database username | `ddb_user` |
| `DB_PASSWORD` | Yes | Database password | — |
| `MQTT_TOPIC_FILTER` | Yes | MQTT topic to subscribe to | `mfi-v1.0-historian/#` |

## Data Flow

```{mermaid}
flowchart LR
    MQTT[MQTT Broker] --> DBN[TimescaleDB Node]
    DBN --> PG[(PostgreSQL/TimescaleDB)]
    
    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class MQTT highlight
```

1. The node subscribes to the configured MQTT topic filter
2. Incoming Sparkplug B messages are decoded and parsed
3. Data points are written into a hypertable (auto-created TimescaleDB time-series table)
4. Each device gets its own hypertable for data isolation

## Database Schema

The TimescaleDB node creates tables following this pattern:

```sql
-- Hypertable for each device
CREATE TABLE IF NOT EXISTS measurements_haas_umc750 (
    timestamp TIMESTAMPTZ NOT NULL,
    device VARCHAR(128),
    namespace VARCHAR(64),
    enterprise VARCHAR(64),
    site VARCHAR(64),
    area VARCHAR(64),
    -- Dynamic metrics columns based on Sparkplug B payload
    metric_0 DOUBLE PRECISION,
    metric_1 DOUBLE PRECISION,
    ...
);

-- Convert to hypertable for time-series optimization
SELECT create_hypertable('measurements_haas_umc750', 'timestamp');
```

## Querying Data

### Using psql

```bash
psql -h localhost -U ddb_user -d ddbbdb_historian
```

```sql
-- Get latest readings for a device
SELECT * FROM measurements_haas_umc750
ORDER BY timestamp DESC LIMIT 10;

-- Aggregate by hour
SELECT 
    time_bucket('1 hour', timestamp) AS hour,
    AVG(metric_0) AS avg_metric_0,
    MAX(metric_1) AS max_metric_1
FROM measurements_haas_umc750
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour DESC;

-- Time-series analysis with built-in functions
SELECT 
    time_bucket('30 minutes', timestamp) AS half_hour,
    percentile_cont(0.95) WITHIN GROUP (ORDER BY metric_0) AS p95_value
FROM measurements_haas_umc750
GROUP BY half_hour
ORDER BY half_hour DESC;
```

### Using Python

```python
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="ddbdb_historian",
    user="ddb_user",
    password="secret"
)

# Query data into a DataFrame
query = """
SELECT timestamp, metric_0 AS spindle_speed
FROM measurements_haas_umc750
WHERE timestamp > NOW() - INTERVAL '1 day'
ORDER BY timestamp;
"""
df = pd.read_sql(query, conn)
print(df.head())

conn.close()
```

## Docker Configuration

The example compose files are sourced from [mfi_ddb_library/docker/timescale](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/docker/timescale).

### `docker-compose.yaml`

```yaml
services:
  timescaledb-db:
    platform: linux/amd64
    image: timescale/timescaledb:latest-pg16
    container_name: mfi-timescaledb-db
    environment:
      - POSTGRES_USER=tsdb
      - POSTGRES_PASSWORD=timescale
      - POSTGRES_DB=ddb_ts
    ports:
      - "5432:5432"
    volumes:
      - ../.data/timescale_storage:/var/lib/postgresql/data
    profiles:
      - "ts"
      - "dbn"
    networks:
      - mfi_network
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tsdb -d ddb_ts"]
      interval: 5s
      timeout: 5s
      retries: 5

  timescaledb-connector:
    platform: linux/amd64
    build:
      context: ../../mfi_ddb_database_nodes/timescaledb/connector
      dockerfile: Dockerfile
    container_name: mfi-timescaledb-connector
    image: cmumfi/mfi-ddb-timescaledb-connector:latest
    profiles:
      - "ts"
      - "dbn"
    depends_on:
      mqtt-broker:
        condition: service_started
      timescaledb-db:
        condition: service_healthy
    volumes:
      - ./connector-config.yaml:/app/config.yaml:ro
    networks:
      - mfi_network
    restart: on-failure

  timescaledb-dws:
    platform: linux/amd64
    build:
      context: ../../mfi_ddb_database_nodes/timescaledb/dws
      dockerfile: Dockerfile
    container_name: mfi-timescaledb-dws
    image: cmumfi/mfi-ddb-timescaledb-dws:latest
    profiles:
      - "ts"
      - "dbn"
    ports:
      - "50052:50051"
    depends_on:
      timescaledb-db:
        condition: service_healthy
    volumes:
      - ./dws-config.yaml:/app/config.yaml:ro
    networks:
      - mfi_network
    restart: always
```

### `connector-config.yaml`

```yaml
mqtt:
  broker_address: "mqtt-broker"
  broker_port: 1883
  topic: "mfi-v1.0-historian/#"
  username: ""
  password: ""

timescaledb:
  host: "timescaledb-db"
  port: 5432
  user: "tsdb"
  password: "timescale"
  dbname: "ddb_ts"

component_id: "default_component"
```

### `dws-config.yaml`

```yaml
timescaledb:
  host: "timescaledb-db"
  port: 5432
  user: "tsdb"
  password: "timescale"
  dbname: "ddb_ts"
```

## Use Cases

1. **SQL Analytics** — Run complex SQL queries, joins, and aggregations on manufacturing data
2. **Reporting** — Generate daily/weekly production reports using standard SQL tools
3. **Data Warehousing** — Combine DDB time-series data with relational business data in PostgreSQL
4. **Machine Learning** — Export data to Python/R for statistical analysis and ML pipelines

## Limitations

- Requires a running PostgreSQL/TimescaleDB instance
- Sparkplug B metric columns must be mapped to table columns (dynamic schema)
- Not ideal for high-frequency writes (>10K/sec); consider Aveva PI for higher throughput
- Non-time-series payloads (`kv`, `blob`) are not supported by this node

## Related Links

- [TimescaleDB Documentation](https://docs.timescale.com/)
- [`mfi_ddb_database_nodes`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_database_nodes/timescaledb) — Source code repository