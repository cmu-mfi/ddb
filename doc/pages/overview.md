# Overview

## What is the Digital Data Backbone?

The **Digital Data Backbone (DDB)** is a comprehensive Python-based framework for streaming data from various sources to the MFI Digital Data Backbone. It provides tools for data ingestion, metadata storage, and retrieval services — enabling seamless ingestion of real-time data from diverse sources including IoT sensors, file systems, and MQTT brokers into a central pub-sub messaging system.

```{raw} html
<h3 style="color: #094d57;">Core Capabilities</h3>
<div class="sd-container-fluid sd-sphinx-override sd-w-100">
<div class="row row-cols-2 row-cols-lg-3 g-3 g-md g-lg-4 p-3 p-md-0">
<div class="col sd-card-wrapper"><div class="card sd-shadow-sm">
<div class="card-body">
<h5 class="sd-card-title">Connect</h5>
<p class="sd-card-text">Equipment and sensors to the digital backbone through communication protocols and interfaces.</p>
</div></div></div>
<div class="col sd-card-wrapper"><div class="card sd-shadow-sm">
<div class="card-body">
<h5 class="sd-card-title">Collect</h5>
<p class="sd-card-text">Time series data, video files, photographs, images and sketches from manufacturing equipment.</p>
</div></div></div>
<div class="col sd-card-wrapper"><div class="card sd-shadow-sm">
<div class="card-body">
<h5 class="sd-card-title">Contextualize</h5>
<p class="sd-card-text">Data through user entered data descriptions (metadata) to ensure integrity and usefulness.</p>
</div></div></div>
</div>
</div>
```

## Architecture at a Glance

The DDB follows an event-driven architecture using MQTT as the central pub-sub broker:

```{mermaid}
flowchart BT
    subgraph Input["."]
        direction LR
        DA[Data Adapter] --> S[Streamer]
    end

    MQTT[Pub-Sub Broker<br>MQTT]

    subgraph Storage["Database Nodes"]
        KV[Key-Value Store]
        BLOB[Blob Storage]
        HISTORIAN[Historian/Time-Series]
    end

    MQTT --> KV
    MQTT --> BLOB
    MQTT --> HISTORIAN

    classDef highlight fill:#094d57,stroke:#0a3d4d,color:white
    class MQTT highlight
```

Data flows from **Data Adapters** → **MQTT Broker** → **Database Nodes**. Each component is independently configurable and pluggable.

## Key Components

| Component | Description | Repository |
|-----------|-------------|------------|
| **Core Library** | Python package providing data adapters, streamers, and topic families | [`mfi_ddb_package`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package) |
| **Data Adapter App** | REST API web application for managing data adapters on edge devices | [`mfi_ddb_data_adapter`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_data_adapter) |
| **Database Nodes** | Compatible database storage implementations | [`mfi_ddb_database_nodes`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_database_nodes) |
| **Retrieval API** | Metadata store and REST API for data queries | [`mfi_ddb_retrieval_api`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_retrieval_api) |

## Who Is This For?

- **Researchers** who need to collect and analyze manufacturing data
- **Engineers** building data collection infrastructure for production environments
- **Integrators** connecting existing equipment to digital systems
- **Operators** managing dashboards and monitoring production metrics