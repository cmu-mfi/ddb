# Use Retrieval API

This guide explains how to retrieve data that has been stored in the Digital Data Backbone using the Retrieval API. The API provides a unified interface for querying data across all connected database nodes.

## Prerequisites

- A running DDB system with at least one database node storing data (see [Connect a Database Node](connect-database-node.md))
- The Retrieval Web Service (RWS) running and accessible

## How the Retrieval API Works

```{mermaid}
flowchart LR
    User[Your Application] --> RWS[Retrieval Web Service]
    RWS --> MDS[(Metadata Store)]
    RWS --> DBN[Database Nodes]
    
    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class RWS highlight
```

The **Retrieval API** consists of two components:

- **Metadata Store (MDS)** — PostgreSQL database tracking data location, format, and descriptive metadata
- **Retrieval Web Service (RWS)** — REST API that queries the MDS to find data and retrieves it from the appropriate database nodes

## Accessing the API

The RWS exposes a RESTful HTTP interface. By default:

```
Base URL: http://localhost:8000/api/v1/
```

### Authentication

Some deployments may require an API key or token. Check your deployment configuration for authentication requirements.

## Key Endpoints

### Get Data (Time-Series)

Retrieve time-series data from historian storage:

```http
GET /api/v1/historian/data?device={device_id}&start_time={ISO8601}&end_time={ISO8601}
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/historian/data?device=HAAS-UMC750&start_time=2025-01-01T00:00:00Z&end_time=2025-01-31T23:59:59Z"
```

**Response:**
```json
{
  "device": "HAAS-UMC750",
  "data": [
    {
      "timestamp": "2025-01-15T10:30:00Z",
      "metrics": {
        "spindle_speed": 12000,
        "feed_rate": 500,
        "temperature": 45.2
      }
    },
    ...
  ]
}
```

### Get Key-Value Data

Retrieve key-value (metadata) records:

```http
GET /api/v1/kv/{key}
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/kv/mfi-v1.0-kv/CMU/Mill19/Lab/device-metadata"
```

**Response:**
```json
{
  "key": "mfi-v1.0-kv/CMU/Mill19/Lab/device-metadata",
  "value": {
    "device_name": "HAAS-UMC750",
    "manufacturer": "HAAS Automation",
    "model": "UMC-750",
    "serial_number": "SN-2024-001",
    "attributes": {
      "location": "Lab Bench A",
      "status": "active"
    }
  }
}
```

### Get Blob Data

Retrieve stored binary objects (files, images):

```http
GET /api/v1/blob/{blob_path}
```

**Example:**
```bash
curl -o image.jpg "http://localhost:8000/api/v1/blob/mfi-v1.0-blob/CMU/Mill19/Lab/photo-001.jpg"
```

### List Available Devices

Discover which devices have streaming data:

```http
GET /api/v1/devices
```

**Response:**
```json
{
  "devices": [
    {
      "id": "HAAS-UMC750",
      "site": "Mill19",
      "area": "Lab",
      "topics": ["historian", "kv"],
      "last_seen": "2025-01-15T10:30:00Z"
    },
    ...
  ]
}
```

## Using the API from Python

### With `requests` Library

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Get time-series data
response = requests.get(f"{BASE_URL}/historian/data", params={
    "device": "HAAS-UMC750",
    "start_time": "2025-01-01T00:00:00Z",
    "end_time": "2025-01-31T23:59:59Z"
})
data = response.json()

# Get key-value data
response = requests.get(f"{BASE_URL}/kv/mfi-v1.0-kv/CMU/Mill19/Lab/config")
config = response.json()

# List devices
response = requests.get(f"{BASE_URL}/devices")
devices = response.json()["devices"]
```

### With Pandas (for Time-Series Data)

```python
import pandas as pd
import requests

def get_timeseries_df(device, start_time, end_time):
    """Retrieve time-series data and convert to DataFrame."""
    url = "http://localhost:8000/api/v1/historian/data"
    response = requests.get(url, params={
        "device": device,
        "start_time": start_time,
        "end_time": end_time
    })
    
    data = response.json()
    records = []
    for entry in data["data"]:
        record = {"timestamp": entry["timestamp"]}
        record.update(entry["metrics"])
        records.append(record)
    
    return pd.DataFrame(records)

# Usage
df = get_timeseries_df(
    device="HAAS-UMC750",
    start_time="2025-01-01T00:00:00Z",
    end_time="2025-01-31T23:59:59Z"
)
print(df.head())
```

## Querying by Topic Path

For more precise queries, you can filter by the full topic path:

```http
GET /api/v1/query?topic=mfi-v1.0-historian/CMU/Mill19/Lab/#&start_time=...&end_time=...
```

Supported filters:
| Parameter | Description | Example |
|-----------|-------------|---------|
| `topic` | MQTT topic filter (supports `#` wildcard) | `mfi-v1.0-historian/CMU/Mill19/#` |
| `device` | Specific device ID | `HAAS-UMC750` |
| `start_time` | Start of time range (ISO 8601) | `2025-01-01T00:00:00Z` |
| `end_time` | End of time range (ISO 8601) | `2025-01-31T23:59:59Z` |
| `limit` | Maximum number of records to return | `1000` |

## Error Responses

The API uses standard HTTP status codes:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| 200 | OK | Request succeeded, data returned |
| 400 | Bad Request | Invalid parameters provided |
| 404 | Not Found | No data found for the query |
| 500 | Internal Server Error | Database node unavailable or error |

## Next Steps

- Visualize your data with a [Grafana dashboard](grafana-dashboard.md)
- Explore the full API specification in the [Retrieval API reference](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_retrieval_api)