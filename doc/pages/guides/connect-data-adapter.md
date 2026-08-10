(daa-guide)=
# Connect a Data Adapter

This guide walks you through connecting a data source to the Digital Data Backbone using a data adapter. You'll learn how to configure and run a data adapter to stream data from your equipment or sensor into the MQTT broker.

## Prerequisites

Before starting, ensure you have:

- A running DDB system (see [Quick Start Guide](../quickstart.md))
- Access to an MQTT broker (default: `localhost:1883`)
- Knowledge of your data source type (MTConnect device, file, MQTT topic, etc.)

## Architecture Overview

```{mermaid}
flowchart LR
    Source[Data Generator] --> DA[Data Adapter] --> S[Streamer] --> MQTT[MQTT Broker]
    
    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class DA highlight
    class S highlight
```

A **data adapter** bridges your data source to the DDB. It performs two key functions:

1. **Monitors** the data generator for new or changed data
2. **Streams** formatted messages to the MQTT broker via a streamer

## Option 1: Data Adapter App (recommended)
<!-- include:daa-guide -->

1. Open the Data Adapter App at [http://localhost:3001](http://localhost:3001).

![Data Adapter App - Adapters](/files/gs2-daa-adapter.png)

2. Click on `+ New Adapter` and select `MQTT` data adapter

![Data Adapter App Home](/files/gs1-daa-home.png)

3. We are going to use a mock mqtt publisher, publishing data to a public broker (https://test.mosquitto.org/). The publisher is one of the docker services running in the background if you chose `*` profile. Fill in the **Adapter Config** and **Streamer Config** fields.

   **Adapter Config**
   ```yaml
   mqtt:
     broker_address: test.mosquitto.org
     broker_port: 1883
   trial_id: test_trial_001
   queue_size: 10
   topics:
     - component_id: telemetry
       topic: admin/feeds/avroom/telemetry/#
   ```

   **Streamer Config**
   ```yaml
   user:
     user_id: test_user
     domain: default
   mqtt:
     broker_address: localhost
     broker_port: 1883
     enterprise: CMU
     site: Test-Site
   project:
     project_name: Test Trial Project
   ```

![Data Adapter App - Config](/files/gs3-daa-config.png)

4. Click **Save**. Once initialized, the connection will show as connected and streaming on screen.

![Data Adapter App - Connected](/files/gs4-daa-connected.png)

<!-- end:daa-guide -->
## Option 2: Use `mfi-ddb` python package

```
pip install mfi-ddb
python -m mfi_ddb.scripts.stream_data --help
```

## Next Steps

- Build a [Grafana dashboard](grafana-dashboard.md) for real-time visualization

**Advanced users**:
- Connect a [database node](connect-database-node.md) to store incoming data
- Query your data using the [Retrieval API](use-retrieval-api.md)