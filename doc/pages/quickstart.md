(quickstart)=
# Quick Start Guide

Get up and running with the MFI Digital Data Backbone in minutes using Docker Compose. This guide will help you deploy a complete DDB system with all core services on a single node.

## Prerequisites


1. Docker Engine
   - Download and install Docker using the instructions here: [Docker Installation](https://docs.docker.com/engine/install/#installation-procedures-for-supported-platforms)

2. Default ports are available. If you see any ports `IN USE`, make sure to edit the config files or terminate the existing process using it.

```
$ cd docker

# Linux / MacOS
$ bash ports-check.sh

# Windows Powershell
$ ./ports-check.ps1

ALL OK!
```

## 1. Single Node Deployment with Docker

**1. Clone the Repository**

```bash
git clone https://github.com/cmu-mfi/mfi_ddb_library.git
cd mfi_ddb_library/docker
```

**2. Start All Services**

```bash
docker compose up -d
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

**Alternative: Download release archive**

```bash
curl -L -o docker-release.zip "https://github.com/cmu-mfi/mfi_ddb_library/releases/download/TAG/FILE.zip" && unzip docker-release.zip
cd mfi_ddb_docker
docker compose up -d
```

```{note}
You can pick and choose services for a multi-node setup. Make sure to use the right config by editing the YAML files of respective services.
```

## 2. Connect a data adapter

```{include} ./guides/connect-data-adapter.md
:start-after: "<!-- include:daa-guide -->"
:end-before: "<!-- end:daa-guide -->"
```

## 3. Visualize the data

```{include} ./guides/grafana-dashboard.md
:start-after: "<!-- include:grafana-guide -->"
:end-before: "<!-- end:grafana-guide -->"
```