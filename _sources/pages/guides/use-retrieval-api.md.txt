# Use Retrieval API

This guide explains how to retrieve data that has been stored in the Digital Data Backbone using the Retrieval API. The API provides a unified interface for querying data across all connected database nodes.

## Prerequisites

- A running DDB system with at least one database node storing data (see [Connect a Database Node](connect-database-node.md))
- The Retrieval Web Service (RWS) running and accessible

## How the Retrieval API Works

```{mermaid}
flowchart LR
    subgraph API[Retrieval API]
      MDS["Metadata Store"] --> RWS["Retrieval Web Service"]
    end
    RWS --> User[Your Application]
    DBN[Database Nodes] --> RWS
    Broker --> MDS

    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class RWS highlight
```

The **Retrieval API** consists of two components:

- **Metadata Store (MDS)** — PostgreSQL database tracking data location, format, and descriptive metadata
- **Retrieval Web Service (RWS)** — REST API that queries the MDS to find data and retrieves it from the appropriate database nodes

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mfi-ddb/type0` | GET | Get information about available endpoints. |
| `/mfi-ddb/type1` | POST | Search trials using metadata store filters. Returns matching trial UUIDs. |
| `/mfi-ddb/type2` | POST | Retrieve data for a specific trial UUID. |
| `/mfi-ddb/type3` | POST | Search trials and retrieve data when a unique trial is found. If multiple trials match, returns list of UUIDs instead. |

## Next Steps

- Visualize your data with a [Grafana dashboard](grafana-dashboard.md)
- Explore the full API specification in the [Retrieval API reference](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_retrieval_api)