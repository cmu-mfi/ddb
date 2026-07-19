# Quick Start Guide

Get up and running with the MFI Digital Data Backbone in minutes using Docker Compose. This guide will help you deploy a complete DDB system with all core services on a single node.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed
- Git cloned [`mfi_ddb_library`](https://github.com/cmu-mfi/mfi_ddb_library) repository

## Single Node Deployment with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/cmu-mfi/mfi_ddb_library.git
cd mfi_ddb_library/docker
```

### 2. Start All Services

```bash
docker compose up -d
```

This starts all core services including:
- **MQTT Broker** — central pub-sub messaging system
- **Metadata Store (MDS)** — PostgreSQL-based metadata storage
- **Retrieval Web Service (RWS)** — REST API for data queries
- **Database Nodes** — configurable storage backends

### 3. Verify Services Are Running

```bash
docker compose ps
```

You should see all services in an "Up" state.

## Alternative: Download Release Archive

```bash
curl -L -o docker-release.zip "https://github.com/cmu-mfi/mfi_ddb_library/releases/download/TAG/FILE.zip" && unzip docker-release.zip
cd mfi_ddb_docker
docker compose up -d
```

> [!NOTE]
> You can pick and choose services for a multi-node setup. Make sure to use the right config by editing the YAML files of respective services.

## What's Running?

After starting, the following ports are available:

| Service | Default Port | Description |
|---------|-------------|-------------|
| MQTT Broker | 1883 (MQTT) / 8083 (WebSocket) | Pub-sub message broker |
| Metadata Store | 5432 (PostgreSQL) | Metadata database |
| Retrieval Web Service | 8000 | REST API endpoint |

## Next Steps

- **Configure a Data Adapter** — See [Connect a Data Adapter](guides/connect-data-adapter.md) to start streaming data
- **Set Up a Database Node** — See [Connect a Database Node](guides/connect-database-node.md) for storage configuration
- **Query Your Data** — See [Use Retrieval API](guides/use-retrieval-api.md) to access your stored data

## Installing the Core Library Locally

If you want to use the DDB library outside of Docker:

```bash
# Clone and navigate to the core package
cd mfi_ddb_library/mfi_ddb_package

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat

# Install from PyPI (recommended)
pip install mfi-ddb

# Or install locally in development mode
pip install -e .