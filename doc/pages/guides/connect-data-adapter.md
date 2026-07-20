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
    class DA highlight
    class S highlight
```

A **data adapter** bridges your data source to the DDB. It performs two key functions:

1. **Monitors** the data generator for new or changed data
2. **Streams** formatted messages to the MQTT broker via a streamer


## Option 1: Data Adapter App

...

## Option 2: Use `mfi-ddb` python package

```
pip install mfi-ddb
python -m mfi_ddb.scripts.stream_data --help
```

## Next Steps

- Connect a [database node](connect-database-node.md) to store incoming data
- Query your data using the [Retrieval API](use-retrieval-api.md)
- Build a [Grafana dashboard](grafana-dashboard.md) for real-time visualization