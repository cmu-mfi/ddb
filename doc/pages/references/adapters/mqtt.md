# MQTT Adapter

The MQTT data adapter subscribes to existing MQTT topics and relays the messages into the DDB topic structure. It serves as a bridge between any MQTT-based system and the Digital Data Backbone.

## Overview

This adapter enables integration with any existing MQTT infrastructure — whether from IoT sensors, other edge devices, or third-party systems — by subscribing to source topics and republishing data under the DDB namespace.

| Property | Value |
|----------|-------|
| **Adapter Type** | `mqtt` |
| **Data Source** | Any MQTT topic |
| **Supported Formats** | JSON (kv), Sparkplug B (historian) |
| **Authentication** | Username/Password, TLS/SSL |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `source_topic` | Yes | MQTT topic to subscribe to | `sensors/+/temperature` |
| `qos` | No | Quality of Service level (0, 1, or 2) | `1` |
| `data_format` | No | Output format: `kv` or `historian` | `kv` |

## Source Topic Patterns

The MQTT adapter supports wildcard topic subscription patterns:

| Pattern | Description | Matches |
|---------|-------------|---------|
| `sensors/temperature` | Single level exact match | Only `sensors/temperature` |
| `sensors/+/temperature` | One-level wildcard | `sensors/hall/temperature`, `sensors/lab/temperature` |
| `sensors/#` | Multi-level wildcard | All topics starting with `sensors/` |

## Topic Mapping

### JSON (kv) Format

When streaming in **kv** format, data is republished under the DDB kv topic structure:

```
mfi-v1.0-kv/{enterprise}/{site}/mqtt/{source_topic}
```

Example source → destination mapping:
- Source: `sensors/hall/temperature`
- Destination: `mfi-v1.0-kv/CMU/Mill19/mqtt/sensors/hall/temperature`

### Sparkplug B (historian) Format

When streaming in **historian** format, the adapter wraps the MQTT payload into a Sparkplug B message and publishes it to:

```
mfi-v1.0-historian/{enterprise}/{site}/mqtt/{source_topic}
```

## Example Configuration

```yaml
# MQTT adapter configuration for sensor data relay
adapter_type: mqtt
name: hall_sensor_relay

streamer:
  broker_host: "localhost"
  broker_port: 1883
  use_tls: false

topic_family: kv
namespace: mfi-v1.0
enterprise: CMU
site: Mill19

attributes:
  description: "Relay hall temperature sensor data to DDB"

mqtt_adapter:
  source_topic: "sensors/hall/temperature"
  qos: 1
```

## Connection Options

| Option | Description | Default |
|--------|-------------|---------|
| `use_tls` | Enable TLS encryption | `false` |
| `ca_cert` | Path to CA certificate for TLS | — |
| `client_cert` | Client certificate path (mutual TLS) | — |
| `username` / `password` | MQTT authentication credentials | — |

## Use Cases

1. **IoT Sensor Relay** — Connect existing IoT sensor networks without modifying their protocol
2. **Legacy System Integration** — Bridge older systems that already publish to MQTT
3. **Multi-Source Aggregation** — Subscribe to multiple source topics and consolidate into DDB structure
4. **Test & Development** — Quickly inject test data from any MQTT publisher for development purposes

## Related Links

- [MQTT Specification](https://mqtt.org/mqtt-specification/)
- [`mfi_ddb_data_adapter`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_data_adapter) — Data adapter app repository