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

| Parameter | Description |
|-----------|-------------|
| `mqtt.broker_address` | Address of the MQTT broker |
| `mqtt.broker_port` | Port of the MQTT broker (default: 1883) |
| `mqtt.username` | Username for MQTT broker authentication |
| `mqtt.password` | Password for MQTT broker authentication |
| `mqtt.tls_enabled` | Enable TLS for MQTT connection (default: False) |
| `mqtt.debug` | Enable debug mode for MQTT client (default: False) |
| `mqtt.timeout` | Timeout in seconds for connecting to the MQTT broker (default: 5) |
| `trial_id` | Trial ID for the system. No spaces or special characters allowed. |
| `queue_size` | Maximum number of messages to buffer before processing. If the buffer is full, the oldest message will be removed. (default: 10) |
| `topics` | List of topics to subscribe to. Each topic should have a 'component_id' and 'topic' key. Optionally, a 'trial_id' can be provided. |
| `topics[].component_id` | Identifier for the component |
| `topics[].topic` | MQTT topic to subscribe to |
| `topics[].trial_id` | Trial ID for the component (optional) |

## Example Configuration

```yaml
adapter_name: my_mqtt_adapter

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

## Related Links

- [MQTT Specification](https://mqtt.org/mqtt-specification/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)
