# Equipment at CMU Mill 19

This page lists the machines, sensors, and IoT devices deployed at the CMU Mill 19 facility as part of the Digital Data Backbone testbed. Each piece of equipment has a corresponding data adapter configured to stream its data into the DDB.

## CNC Machining Centers

| Equipment | Manufacturer | Model | MTConnect Agent | MQTT Topic Branch |
|-----------|-------------|-------|-----------------|-------------------|
| HAAS-UMC750 | HAAS Automation | UMC-750 | `mtconnect_adapter_haas` | `mfi-v1.0-historian/CMU/Mill19/Lab/HASS-UMC750` |
| DMG-MORI-DM500 | DMG MORI | DMU 50 | `mtconnect_adapter_dmg` | `mfi-v1.0-historian/CMU/Mill19/Lab/DMG-MORI-DM500` |

### HAAS UMC-750

The Haas UMC-750 is a 5-axis CNC machining center used for precision milling and turning operations. It is the primary test equipment for Sparkplug B data streaming via MTConnect agents.

**Key Metrics Streamed:**
| Metric Name | Type | Unit | Description |
|------------|------|------|-------------|
| `spindle_speed` | Numeric | RPM | Current spindle rotation speed |
| `feed_rate` | Numeric | mm/min | Current feed rate |
| `program_number` | String | — | Currently running program ID |
| `cycle_time` | Numeric | seconds | Active cycle runtime |

**MQTT Topic Example:**
```
mfi-v1.0-historian/CMU/Mill19/Lab/HASS-UMC750/spindle_speed
mfi-v1.0-historian/CMU/Mill19/Lab/HASS-UMC750/feed_rate
```

### DMG MORI DMU 50

The DMG MORI DMU 50 is a multi-tasking machine with milling and turning capabilities, used for complex aerospace and medical component manufacturing.

**Key Metrics Streamed:**
| Metric Name | Type | Unit | Description |
|------------|------|------|-------------|
| `spindle_speed` | Numeric | RPM | Current spindle rotation speed |
| `tool_load` | Numeric | % | Current tool load percentage |
| `coolant_pressure` | Numeric | bar | Coolant system pressure |

**MQTT Topic Example:**
```
mfi-v1.0-historian/CMU/Mill19/Lab/DMG-MORI-DM500/spindle_speed
mfi-v1.0-historian/CMU/Mill19/Lab/DMG-MORI-DM500/tool_load
```

## IoT Sensors

| Sensor | Type | Protocol | MQTT Topic Branch |
|--------|------|----------|-------------------|
| Temperature/Humidity Array (THA) | Environmental | MQTT native | `mfi-v1.0-kv/CMU/Mill19/Lab/sensors/environment` |
| Vibration Sensors (VS) | Accelerometer | MQTT native | `mfi-v1.0-historian/CMU/Mill19/Lab/sensors/vibration` |

### Temperature/Humidity Array

A network of wireless temperature and humidity sensors deployed throughout the facility for environmental monitoring and HVAC optimization.

**Sensor Locations:**
| Sensor ID | Location | MQTT Topic |
|-----------|----------|------------|
| `th-01` | Near HAAS-UMC750 | `mfi-v1.0-kv/CMU/Mill19/Lab/sensors/environment/th-01` |
| `th-02` | Near DMG-MORI | `mfi-v1.0-kv/CMU/Mill19/Lab/sensors/environment/th-02` |
| `th-03` | Entrance / Lobby | `mfi-v1.0-kv/CMU/Mill19/Lab/sensors/environment/th-03` |

### Vibration Sensors

Accelerometer-based vibration sensors mounted on CNC machine spindles for predictive maintenance analysis.

**Sensor Locations:**
| Sensor ID | Equipment | MQTT Topic |
|-----------|-----------|------------|
| `vs-01` | HAAS-UMC750 Spindle | `mfi-v1.0-historian/CMU/Mill19/Lab/sensors/vibration/vs-01` |
| `vs-02` | DMG-MORI Spindle | `mfi-v1.0-historian/CMU/Mill19/Lab/sensors/vibration/vs-02` |

## Additive Manufacturing Equipment

| Equipment | Manufacturer | Model | Status |
|-----------|-------------|-------|--------|
| Metal 3D Printer | GE Additive | DEPM 4000 | Planned integration |
| Polymer SLS Printer | EOS | P 385 | Under testing |

## Edge Infrastructure

| Device | Role | Location | OS |
|--------|------|----------|-----|
| edge-pc-01 | Data Adapter App + MQTT Broker | Lab rack, near machines | Ubuntu 22.04 LTS |
| edge-pc-02 | Database Nodes (TimescaleDB, KV-PSQL) | Server room | Ubuntu 22.04 LTS |
| edge-pc-03 | Blob Store + Retrieval Services | Server room | Debian 12 |

## Data Flow Summary

```{mermaid}
flowchart LR
    subgraph Machines["CNC Machines"]
        HAAS[HAAS UMC750]
        DMG[DMG MORI DM500]
    end

    subgraph Sensors["IoT Sensors"]
        THA[Temperature/Humidity<br/>Array]
        VS[Vibration<br/>Sensors]
    end

    MQTT[MQTT Broker<br/>EMQX]

    HAAS -->|MTConnect| MQTT
    DMG -->|MTConnect| MQTT
    THA -->|Native MQTT| MQTT
    VS -->|Native MQTT| MQTT

    classDef machines fill:#e6f7ff,stroke:#1890ff
    classDef sensors fill:#fff7e6,stroke:#fa8c16
    class Machines machines
    class Sensors sensors
```

## Connecting New Equipment

To add a new piece of equipment to the DDB at CMU Mill 19:

1. **Identify the data source** — Determine protocol (MTConnect, MQTT, gRPC, etc.) and available metrics
2. **Configure a data adapter** — Use the Data Adapter App UI or YAML config to create an adapter for the new device
3. **Assign a topic family** — Choose `historian` for time-series data, `kv` for metadata/config, or `blob` for files
4. **Deploy and verify** — Start the adapter and confirm data appears in the MQTT broker dashboard

See the [Connect a Data Adapter Guide](../../guides/connect-data-adapter.md) for step-by-step instructions.