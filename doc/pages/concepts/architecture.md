# Architecture

The MFI Digital Data Backbone follows an event-driven, pub-sub architecture that decouples data producers from consumers. This allows multiple downstream databases to subscribe to the broker and store data without direct integration with source systems.

## System Overview

```{mermaid}
flowchart BT
    subgraph Input["."]
        direction LR

        DAA[Data</br>Adapter</br>App</br>]

        subgraph Data_Sources["Data Sources"]
            direction LR
            DS1[Data Generator 1] --> DA1[Data Adapter 1]
            DA1 --> S1[Streamer 1]
            DS2[Data Generator ...] --> DA2[Data Adapter ...]
            DA2 --> S2[Streamer 2]
            DSn[Data Generator ...] --> DAn[Data Adapter ...]
            DAn --> Sn[Streamer n]
        end
    end

    MQTT[Pub-Sub Broker: MQTT]

    subgraph DBN["Database Nodes"]
        direction LR
        KV[DBN: Key-Value Store]
        BLOB[DBN: Blob Storage]
        HISTORIAN[DBN: Historian/Time-Series]
        DBNx[DBN: Other...]
    end

    subgraph Retrieval["Retrieval API"]
        direction TB
        MDS[Metadata Store] --> RWS[Retrieval Web Service]
    end

    S1 --> MQTT
    S2 --> MQTT
    Sn --> MQTT
    MQTT --> KV
    MQTT --> BLOB
    MQTT --> HISTORIAN
    MQTT --> DBNx
    MQTT --> MDS
    DBN --> RWS
    RWS --> USERS[Users/Applications]

    classDef layer fill:#e6f7ff,stroke:#1890ff
    classDef highlight fill:#094d57,stroke:#0a3d4d
    class Data_Sources,DBN,Retrieval layer
    style Input fill:transparent,stroke:#666
```

```{note}
Arrow direction in the diagram above shows the data flow in the framework. It doesn't represent the direction of requests.
```

## Component Descriptions

**Key Components**

| Component | Description | Repository |
|-----------|-------------|------------|
| **Core Library** | Python package providing data adapters, streamers, and topic families | [`mfi_ddb_package`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package) |
| **Data Adapter App** | REST API web application for managing data adapters on edge devices | [`mfi_ddb_data_adapter`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_data_adapter) |
| **Database Nodes** | Compatible database storage implementations | [`mfi_ddb_database_nodes`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_database_nodes) |
| **Retrieval API** | Metadata store and REST API for data queries | [`mfi_ddb_retrieval_api`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_retrieval_api) |

### Data Generators
The top layer shows example current and future generators of information for the digital backbone. These sources are responsible for generating data that will be collected and processed by the system. Examples include:
- CNC machines and industrial equipment
- IoT sensors (temperature, pressure, vibration)
- File systems and databases
- MQTT brokers and ROS topics

### Data Adapters
Data adapters monitor the data generators for events. They listen for data changes or updates from the data generators and pass the information to the MQTT Broker in the correct format. Each adapter handles a specific type of data source.

[Read more about available adapters →](../references/adapters/index.md#available-adapters)

### Publish-Subscribe Broker (MQTT)
The MQTT Broker acts as the central communication hub in the pub-sub model. It receives messages from streamers and distributes them to the appropriate subscribers based on topic subscriptions. This decoupling allows new database nodes and consumers to be added without modifying existing components.

**Key features:**
- Topic-based message routing
- Quality of Service (QoS) levels for reliable delivery
- Support for persistent sessions
- Secure connections via TLS/SSL

### Database Nodes
The cloud storage layer contains different storage solutions where data is stored. These nodes subscribe to the MQTT Broker to receive data and facilitate transfer from the broker to the appropriate storage systems:

| Database Node | Type | Compatible Payloads | Description |
|---------------|------|---------------------|-------------|
| [Aveva PI](../references/database-nodes/aveva-pi.md) | Time-Series | historian | Industrial historian for time-series data |
| [Blob](../references/database-nodes/blob.md) | File Storage | blob, kv | Cloud file storage for binary objects |
| [KV-PSQL](../references/database-nodes/kv-psql.md) | Key-Value Store | kv | PostgreSQL-based key-value store |
| [TimescaleDB](../references/database-nodes/timescaledb.md) | Time-Series | historian | PostgreSQL-based time-series database |

### Retrieval API
This layer provides retrieval services that can access data stored in the cloud storage. It consists of two components:

- **Metadata Store (MDS)** — PostgreSQL-based metadata storage that tracks data location, format, and descriptive information
- **Retrieval Web Service (RWS)** — REST API for querying and retrieving data from all connected database nodes through a unified interface

## Data Flow Summary

1. A **Data Generator** produces raw data (sensor reading, file, etc.)
2. The **Data Adapter** detects the new data and converts it to DDB format
3. The **Streamer** publishes the formatted message to the MQTT Broker on the appropriate topic
4. **Database Nodes** subscribed to that topic receive and store the data
5. Users query data through the **Retrieval API**, which consolidates results from all storage backends

## Topic Structure

All messages use a hierarchical topic structure:

```
mfi-v1.0/{topic_family}/{enterprise}/{site}/{area}/{device}
```

Where `topic_family` is one of:
- `historian` — Time-series data (Sparkplug B format)
- `kv` — Key-value / non-time-series data (JSON format)
- `blob` — Binary large object data (protobuf + binary payload)

[Learn more about the schema →](../references/payload-schema.md)