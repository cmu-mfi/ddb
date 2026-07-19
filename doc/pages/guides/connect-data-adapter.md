# Connect a Data Adapter

This guide walks you through connecting a data source to the Digital Data Backbone using a data adapter. You'll learn how to configure and run a data adapter to stream data from your equipment or sensor into the MQTT broker.

## Prerequisites

Before starting, ensure you have:

- A running DDB system (see [Quick Start Guide](quickstart.md))
- Access to an MQTT broker (default: `localhost:1883`)
- Knowledge of your data source type (MTConnect device, file, MQTT topic, etc.)

## Architecture Overview

```{mermaid}
flowchart LR
    Source[Data Generator] --> DA[Data Adapter] --> S[Streamer] --> MQTT[MQTT Broker]
    
    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class MQTT highlight
```

A **data adapter** bridges your data source to the DDB. It performs two key functions:

1. **Monitors** the data generator for new or changed data
2. **Streams** formatted messages to the MQTT broker via a streamer

## Step 1: Choose Your Adapter Type

Select the adapter that matches your data source:

| Data Source | Adapter | Description |
|-------------|---------|-------------|
| CNC machines (MTConnect) | MTConnect | Interface with MTConnect-enabled devices |
| MQTT topics | MQTT | Subscribe to existing MQTT topics |
| gRPC services | gRPC | Connect via gRPC endpoints |
| Key-value stores | Key-Value | Read from KV databases |
| Local files | File System | Watch directories for new/changed files |
| ROS topics | ROS / ROS Files | Interface with Robot Operating System |

## Step 2: Configure the Adapter

Each adapter requires a YAML configuration file. Here's a general template:

```yaml
# adapter_config.yaml
adapter_type: <adapter_name>          # e.g., mtconnect, mqtt, grpc
name: my_adapter                      # Unique name for this adapter

streamer:
  broker_host: "localhost"            # MQTT broker address
  broker_port: 1883                   # MQTT port
  use_tls: false                      # Enable TLS if needed
  username: ""                        # Optional authentication
  password: ""

topic_family: historian                 # historian, kv, or blob
namespace: mfi-v1.0                     # DDB namespace version
enterprise: CMU                        # Enterprise identifier
site: Mill19                            # Site/facility identifier
area: Lab                             # Area identifier
device: Machine-01                      # Device identifier

attributes:                             # Key-value metadata about the data source
  description: "CNC machine sensor data"
  unit: "celsius"                       # Optional: measurement units
  sampling_rate: "1s"                   # Data collection interval

# Adapter-specific configuration follows...
```

### MTConnect Adapter Example

```yaml
adapter_type: mtconnect
name: mill19_cnc
streamer:
  broker_host: "localhost"
  broker_port: 1883
topic_family: historian
namespace: mfi-v1.0
enterprise: CMU
site: Mill19
area: Lab
device: HAAS-UMC750

mtconnect_adapter:
  device_url: "http://localhost:7879"    # MTConnect device URL
  push_mode: false                        # Pull (false) or push (true) mode
```

### MQTT Adapter Example

```yaml
adapter_type: mqtt
name: sensor_subscriber
streamer:
  broker_host: "localhost"
  broker_port: 1883
topic_family: kv
namespace: mfi-v1.0
enterprise: CMU
site: Mill19
area: Lab

mqtt_adapter:
  source_topic: "sensors/+/temperature"   # MQTT topic to subscribe to
  qos: 1                                  # Quality of Service level
```

## Step 3: Run the Data Adapter

### Using the Data Adapter App (Web UI)

The **Data Adapter App** provides a web-based interface for managing adapters on an edge device:

1. Start the data adapter app backend and frontend:
   ```bash
   cd mfi_ddb_data_adapter/data_adapter_app
   # Follow instructions in that package's README.md
   ```

2. Open the web UI in your browser

3. Click **New Adapter** to create a new configuration

4. Select the adapter type and fill in the configuration form

5. Click **Save** — then toggle **Start Streaming** to begin data collection

```{image} ../files/ui_newadapter.png
:alt: New adapter creation screen
```

### Using Python Directly

Alternatively, you can run adapters programmatically using the core library:

```python
from mfi_ddb.data_adapters import get_data_adapter
from mfi_ddb.streamer import MQTTStreamer

# Configure streamer
streamer = MQTTStreamer(
    host="localhost",
    port=1883,
    topic_family="historian"
)

# Create adapter (example: MTConnect)
adapter = get_data_adapter("mtconnect")
adapter.configure({
    "device_url": "http://your-device:7879",
    "push_mode": False
})

# Connect and start streaming
streamer.connect()
adapter.set_streamer(streamer)
adapter.start()  # Begin monitoring data source
```

## Step 4: Verify Data is Streaming

Check that messages are flowing to the MQTT broker:

```bash
# Subscribe to all DDB topics using an MQTT client
mosquitto_sub -h localhost -p 1883 -t "mfi-v1.0/#"
```

You should see published messages appearing in real-time.

## Step 5: Stop Streaming

To stop data collection:

- **Web UI**: Toggle the adapter off or click the delete button
- **Python**: Call `adapter.stop()` and `streamer.disconnect()`

## Next Steps

- Connect a [database node](connect-database-node.md) to store incoming data
- Query your data using the [Retrieval API](use-retrieval-api.md)
- Build a [Grafana dashboard](grafana-dashboard.md) for real-time visualization