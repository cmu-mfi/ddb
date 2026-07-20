# Key-Value Store Adapter

The Key-Value Store data adapter reads data from a database and publishes it to the DDB topic structure using key-value pairs. It connects to PostgreSQL databases to retrieve structured data from configured tables.

## Overview

This adapter is designed for scenarios where manufacturing data is already stored in relational databases. It queries specified tables, maps columns to DDB components, and streams results as key-value pairs into the Digital Data Backbone.

| Property | Value |
|----------|-------|
| **Adapter Type** | `key_value_store` |
| **Data Source** | PostgreSQL database tables |
| **Recommended Topic Family** | `kv` |
| **Self-Update** | No (polls via `get_data()`) |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `key_value_store.host` | Yes | Host address of the PostgreSQL database | `"localhost"` |
| `key_value_store.port` | No | Port of the PostgreSQL database (default: 5432) | `5432` |
| `key_value_store.database_name` | Yes | Name of the database to connect to | `"mydb"` |
| `key_value_store.username` | Yes | Username for authentication | `"admin"` |
| `key_value_store.password` | Yes | Password for authentication | `"password"` |
| `topic_family` | No | Topic family to publish data in (default: `kv`) | `"historian"` |

## How It Works

1. **Database Connection** — Connects to the PostgreSQL database using the provided credentials and connection parameters.
2. **Table Discovery** — Queries the configured tables and retrieves their schemas (column names and types).
3. **Data Collection** — Executes SELECT queries on each table, maps column values to DDB component IDs based on the `component_id` configuration, and collects results.
4. **Publishing** — Publishes collected key-value pairs to MQTT under the configured topic family (`kv` by default).

## Use Cases

1. **Database-Backed Data Streaming** — Stream data from existing PostgreSQL databases into DDB
2. **Data Warehouse Integration** — Connect manufacturing data warehouses to the Digital Data Backbone
3. **Historical Data Retrieval** — Query historical records and publish them as current state data
4. **Multi-Table Aggregation** — Combine data from multiple related tables into a unified DDB view

## Related Links

- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)