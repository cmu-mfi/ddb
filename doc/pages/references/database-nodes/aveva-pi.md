# Aveva PI Database Node

The Aveva PI (AF) database node stores time-series data from the DDB into an Aveva PI System asset framework. It is designed for industrial OT environments requiring high-performance historian capabilities.

## Overview

Aveva PI is a leading industrial historian platform used for real-time monitoring and analytics in manufacturing, energy, and process industries. The DDB database node subscribes to MQTT topics and writes data into the AF hierarchy.

| Property | Value |
|----------|-------|
| **Node Type** | Time-Series Historian |
| **Compatible Payloads** | `historian` (Sparkplug B) |
| **Storage Engine** | Aveva PI System / Asset Framework |
| **Protocol** | AF SDK / REST Web API |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PI_SERVER` | Yes | PI Web API endpoint or AF server name | `piserver` |
| `AF_DATABASE` | No | Asset Framework database name | `CMU_Mill19` |
| `AF_TEMPLATE` | No | Default AF element template | `DefaultInstrumentTemplate` |
| `MQTT_TOPIC_FILTER` | Yes | MQTT topic to subscribe to | `mfi-v1.0-historian/#` |

## Data Flow

```{mermaid}
flowchart LR
    MQTT[MQTT Broker] --> DBN[Aveva PI Node]
    DBN --> AF[(Asset Framework)]
    
    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class MQTT highlight
```

1. The node subscribes to the configured MQTT topic filter (typically `mfi-v1.0-historian/#`)
2. Incoming Sparkplug B messages are decoded and parsed
3. Data points are written to the corresponding AF element attributes based on metric names
4. PI tags are created automatically if they do not already exist

## Asset Framework Mapping

The node maps DDB data into the Aveva PI Asset Framework hierarchy:

| DDB Path Component | AF Equivalent |
|-------------------|---------------|
| `enterprise` | AF Database / Element |
| `site` | Parent AF Element (e.g., "Mill19") |
| `area` | Child AF Element (e.g., "Lab") |
| `device` | Equipment AF Element (e.g., "HAAS-UMC750") |
| Metric name | AF Attribute / PI Tag |

## Docker Configuration

The example compose files are sourced from [mfi_ddb_library/docker/aveva](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/docker/aveva).

### `docker-compose.yaml`

```yaml
services:
  aveva-pi-dws:
    platform: linux/amd64
    build:
      context: ../../mfi_ddb_database_nodes/aveva-pi/dws
      dockerfile: Dockerfile
    container_name: mfi-aveva-pi-dws
    image: cmumfi/mfi-ddb-aveva-pi-dws:latest
    profiles:
      - "aveva"
      - "dbn"
    ports:
      - "50054:50054"
    networks:
      - mfi_network
    volumes:
      - ./config.yaml:/app/config.yaml:ro
    restart: always
```

### `config.yaml`

```yaml
url: "<PI Web API endpoint, e.g., http://piserver.local/piwebapi>"

username: "<PI Web API username>"
password: "<PI Web API password>"

dataserver:
  name: "<Aveva PI Data Server name>"
  webid: "<PI Data Server WebID>"

mqtt_connector:
  path: "<Path to MQTT connector configuration file>"
```

## Querying Data from Aveva PI

### Via Web API (REST)

```bash
# Get a specific PI tag value
curl -u username:password \
  "http://piserver/piwebapi/streams/{stream_id}/recorded?start_time=-1h&end_time=now"
```

### Via Python SDK

```python
import requests

PI_WEB_API = "http://piserver.local/piwebapi"

def get_pi_values(stream_id, start_time, end_time):
    """Query recorded values from Aveva PI."""
    url = f"{PI_WEB_API}/streams/{stream_id}/recorded"
    params = {
        "start_time": start_time,
        "end_time": end_time,
        "max_count": 1000
    }
    response = requests.get(url, auth=("user", "pass"), params=params)
    return response.json()

# Usage
values = get_pi_values(
    stream_id="streams/~MDEUABN9BAAAAAAA",
    start_time="-24h",
    end_time="now"
)
```

## Use Cases

1. **Equipment Monitoring** — Track machine health metrics (temperature, vibration, spindle load) over time
2. **Process Historian** — Maintain a long-term record of manufacturing process parameters
3. **OT Analytics** — Feed data to Aveva ProcessBook or PI Vision for visualization
4. **Compliance & Audit** — Archive production data with timestamps for regulatory compliance

## Limitations

- Requires an existing Aveva PI System deployment
- AF SDK license required for direct connections
- Limited support for non-time-series (kv, blob) payloads
- Best suited for industrial OT environments; not ideal for general-purpose analytics

## Related Links

- [Aveva PI Web API Documentation](https://docs.aveva.com/bundle/pi-web-api/page/index.html)
- [`mfi_ddb_database_nodes`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_database_nodes/aveva-pi) — Source code repository