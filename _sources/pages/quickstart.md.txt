# Quick Start Guide

Get up and running with the MFI Digital Data Backbone in minutes using Docker Compose. This guide will help you deploy a complete DDB system with all core services on a single node.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed
- [Git](https://git-scm.com/install/) installed 
- Git cloned [`mfi_ddb_library`](https://github.com/cmu-mfi/mfi_ddb_library) repository

## Single Node Deployment with Docker

**1. Clone the Repository on Terminal**

```bash
git clone https://github.com/cmu-mfi/mfi_ddb_library.git
cd mfi_ddb_library/docker
```

**2. Start All Services**

```bash
docker compose --profile '*' up -d
```

This starts all core services including:
- **MQTT Broker** — central pub-sub messaging system
- **Metadata Store (MDS)** — PostgreSQL-based metadata storage
- **Retrieval Web Service (RWS)** — REST API for data queries
- **Database Nodes** — configurable storage backends

**3. Verify Services Are Running**

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

```{note}
You can pick and choose services for a multi-node setup. Make sure to use the right config by editing the YAML files of respective services.
```
