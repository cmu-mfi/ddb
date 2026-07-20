# MQTT Adapter

The MQTT data adapter subscribes to existing MQTT topics and relays the messages into the DDB topic structure. It serves as a bridge between any MQTT-based system and the Digital Data Backbone.

## Overview

This adapter enables integration with any existing MQTT infrastructure — whether from IoT sensors, other edge devices, or third-party systems — by subscribing to source topics and republishing data under the DDB namespace.

| Property | Value |
|----------|-------|
| **Adapter Type** | `mqtt` |
| **Data Source** | Any MQTT topic |
| **Recommended Topic Family** | `historian` |
| **Self-Update** | Yes (listens in a separate thread) |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `mqtt.broker_address` | Yes | Address of the MQTT broker | `"mqtt.example.com"` |
| `mqtt.broker_port` | No | Port of the MQTT broker (default: 1883) | `1883` |
| `mqtt.username` | No | Username for MQTT broker authentication | `"user"` |
| `mqtt.password` | No | Password for MQTT broker authentication | `"pass"` |
| `mqtt.tls_enabled` | No | Enable TLS for MQTT connection (default: False) | `false` |
| `mqtt.debug` | No | Enable debug mode for MQTT client (default: False) | `false` |
| `mqtt.timeout` | No | Timeout in seconds for connecting to the MQTT broker (default: 5) | `5` |
| `trial_id` | Yes | Trial ID for the system. No spaces or special characters allowed. | `"trial_001"` |
| `queue_size` | No | Maximum number of messages to buffer before processing (default: 10) | `10` |
| `topics` | Yes | List of topics to subscribe to (see below) | — |

### Topics Configuration

Each topic in the `topics` list must include:

| Field | Description |
|-------|-------------|
| `component_id` | Identifier for the component |
| `topic` | MQTT topic to subscribe to |
| `trial_id` | Trial ID override per component (optional) |

## Example Configuration

```yaml
adapter_type: mqtt
name: my_mqtt_adapter

mqtt:
  broker_address: "mqtt.example.com"
  broker_port: 1883

trial_id: "trial_001"
queue_size: 10

topics:
  - component_id: "robot-arm-1"
    topic: "robot-arm/1/data"
    trial_id: "trial_001"
  - component_id: "machine-a"
    topic: "machine/a/data"
```

## How It Works

1. **Broker Connection** — Connects to the MQTT broker using configured credentials and TLS settings.
2. **Topic Subscription** — Subscribes to each configured topic with a message callback.
3. **Data Collection** — Buffers incoming messages (up to `queue_size`) and publishes them to DDB topics under the configured namespace.

## Use Cases

1. **IoT Sensor Relay** — Connect existing IoT sensor networks without modifying their protocol
2. **Legacy System Integration** — Bridge older systems that already publish to MQTT
3. **Multi-Source Aggregation** — Subscribe to multiple source topics and consolidate into DDB structure
4. **Test & Development** — Quickly inject test data from any MQTT publisher for development purposes

## Related Links

- [MQTT Specification](https://mqtt.org/mqtt-specification/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)