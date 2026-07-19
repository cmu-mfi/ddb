# CMU Mill 19 Deployment

The Carnegie Mellon University (CMU) Mill 19 facility serves as the primary testbed and reference deployment for the Digital Data Backbone (DDB). This page provides an introduction to the deployment infrastructure, network topology, and operational context.

## Overview

CMU's Mill 19 Manufacturing Innovation Facility is a 26,000 sq ft advanced manufacturing lab located in Pittsburgh, PA. The facility hosts a diverse array of CNC machining centers, additive manufacturing equipment, and IoT sensors — making it an ideal environment for testing the DDB framework in a real-world manufacturing setting.

## Deployment Architecture

```{mermaid}
flowchart BT
    subgraph Edge["Edge Devices (Mill 19)"]
        direction LR
        AD[Data Adapter App] --> MQTT[MQTT Broker<br/>EMQX]
        AD --> DAA1[MTConnect Adapter]
        AD --> DAA2[MQTT Adapter]
        AD --> DAA3[gRPC Adapter]
    end

    subgraph Storage["Database Nodes"]
        direction LR
        KV[(KV-PSQL<br/>Metadata)]
        HIST[(TimescaleDB<br/>Time-Series)]
        BLOB[(Blob Store<br/>Local FS)]
    end

    MQTT --> KV
    MQTT --> HIST
    MQTT --> BLOB

    subgraph Retrieval["Retrieval Services"]
        RWS[Retrieval Web Service]
        MDS[(Metadata Store<br/>PostgreSQL)]
    end

    KV --> RWS
    HIST --> RWS
    BLOB --> RWS
    RWS --> MDS

    classDef edge fill:#e6f7ff,stroke:#1890ff
    classDef storage fill:#fff7e6,stroke:#fa8c16
    classDef retrieval fill:#f6ffed,stroke:#52c41a
    class Edge edge
    class Storage storage
    class Retrieval retrieval
```

## Network Topology

The Mill 19 deployment spans multiple network segments:

| Segment | Description | Devices |
|---------|-------------|---------|
| **OT Network** (10.20.30.x) | Connected to CNC machines via MTConnect agents | HAAS-UMC750, DMG-MORI |
| **IoT Network** (10.40.50.x) | Wireless sensor network for environmental monitoring | Temperature, humidity sensors |
| **IT Network** (10.60.70.x) | Edge servers, database nodes, and retrieval services | Edge PC, MQTT broker |

## Key Components Running at CMU Mill 19

| Component | Host | Port(s) | Purpose |
|-----------|------|---------|---------|
| EMQX MQTT Broker | edge-pc-01 | 1883 (MQTT), 8083 (Dashboard) | Message routing |
| Data Adapter App | edge-pc-01 | 8000 (Backend), 3000 (Frontend) | Adapter management UI |
| TimescaleDB | edge-pc-02 | 5432 | Time-series data storage |
| KV-PSQL | edge-pc-02 | 5433 | Key-value metadata store |
| Blob Store | edge-pc-01 | — (local filesystem) | Binary file storage |
| Retrieval Web Service | edge-pc-01 | 8000 | REST API for data queries |

## Getting Started with This Deployment

To replicate the CMU Mill 19 deployment locally, follow the [Quick Start Guide](../../quickstart.md). The reference Docker Compose configuration in the [`mfi_ddb_library/docker`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/docker) directory closely mirrors this production setup.

## Equipment Inventory

See [Equipment at CMU Mill 19](equipment.md) for a detailed list of machines and sensors deployed in the facility.