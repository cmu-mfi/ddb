# Data Adapters

Data adapters connect manufacturing equipment and external data sources to the Digital Data Backbone (DDB). Each adapter handles a specific protocol or interface, translating incoming data into DDB's standardized format for streaming via MQTT.

## Available Adapters

| Adapter | Description | Recommended Topic Family |
|---------|-------------|--------------------------|
| [gRPC](grpc.md) | Connects to gRPC services to stream data | `historian` |
| [MQTT](mqtt.md) | Subscribes to MQTT topics and relays into DDB | `kv` / `historian` |
| [MTConnect](mtconnect.md) | Interfaces with MTConnect-enabled CNC machines | `historian` |

## How Data Adapters Work

All data adapters inherit from the `BaseDataAdapter` class and share common behaviors:

1. **Configuration** — Each adapter accepts a YAML/JSON configuration defining connection parameters, source topics, and output format.
2. **Data Collection** — Adapters either poll for data (`get_data()`) or receive it via callbacks (e.g., ROS subscribers).
3. **Publishing** — Collected data is published to the MQTT broker under the DDB topic structure based on the adapter's recommended `topic_family`.

## Configuration Reference

Each adapter defines:

- **`CONFIG_HELP`** — A dictionary describing all configuration parameters, their types, and descriptions.
- **`CONFIG_EXAMPLE`** — A complete example configuration for quick setup.
- **`RECOMMENDED_TOPIC_FAMILY`** — The default topic family (`kv`, `historian`, or `blob`) this adapter produces data in.

## Related Links

- [Payload Schema](../payload-schema.md)
- [Architecture Overview](../../concepts/architecture.md)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)