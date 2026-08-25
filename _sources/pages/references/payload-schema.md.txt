# Payload Schema V1.0

MFI DDB Schema V1.0 defines the format for all data streamed to the Digital Data Backbone. The schema is designed to be flexible and extensible to accommodate different types of manufacturing data.

Messages are published to an MQTT broker using the publish-subscribe model, which routes them to appropriate subscribers based on topic subscriptions. The schema defines topics used for different data types and specifies payload structure for each type.

## Topic Structure

The DDB uses a hierarchical topic structure:

```
mfi-v1.0/{topic_family}/{enterprise}/{site}/{area}/{device}
```

### Topic Families

| Family | Data Type | Format | Description |
|--------|-----------|--------|-------------|
| `historian` | Time-series data | Sparkplug B | Industrial sensor readings, machine parameters |
| `kv` | Non-time-series data | JSON | Key-value metadata, configuration, status updates |
| `blob` | Binary files | Protobuf + binary | Images, files, large binary payloads |

```{mermaid}
flowchart LR;
    B[mfi-v1.0];
    B --> C[historian] --> F["enterprise"];
    B --> D[kv] --> F;
    B --> E[blob] --> F;
    F --> G["site*"];
    G --> H["area*"];
    H --> I["device*"];
    I --> X["..."];
    F --> X;
    G --> X;
    H --> X;

    classDef highlight fill:#84c964
    class A,B,C,D,E highlight
```

> `site`, `area`, and `device` are optional placeholders for the actual values of enterprise, site, area, and device.

**Examples:**
- `mfi-v1.0-kv/CMU/Mill19/Mezzanine-Lab/yk-destroyer/#`
- `mfi-v1.0-historian/CMU/Mill19/HAAS-UMC750/#`

## Payload Details by Family

### historian [Time-Series]

Since we use Aveva PI to store time-series data, the Sparkplug B schema is adopted as an initial model for inspiration. Its flexibility allows it to be applied to other data types. The general schema for Sparkplug B v1.0 is defined in the [Sparkplug specification](https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf).

Key points:

* Sparkplug requires following topic structure: `namespace/group_id/message_type/node_id/[device_id]`
* Sparkplug messages are serialized using Google Protocol Buffers ([protobuf](https://protobuf.dev/))
* In reference to the above structure,
    * `namespace` = `mfi-v1.0-historian`
    * `group_id` = `enterprise`
    * `message_type` = Sparkplug B message type (DDATA, DBIRTH, etc.)
    * `node_id` = `site`
    * `device_id` = `area` (optional)
* `mfi_ddb` expects at least a DBIRTH message to establish identity and a DDATA message to send data
* Metric naming convention is defined in [historian-metric-naming.md](https://github.com/cmu-mfi/mfi_ddb_library/blob/main/schema/historian-metric-naming.md)
* `mfi_ddb` library uses [mqtt-spb-wrapper](https://pypi.org/project/mqtt-spb-wrapper/) to create Sparkplug messages
* Messages can be decoded using the [protobuf schema](https://github.com/cmu-mfi/mfi_ddb_library/blob/main/schema/spbv.proto). Some MQTT brokers, [like EMQX](https://www.emqx.com/en/blog/mqtt-sparkplug-in-action-a-step-by-step-tutorial), have built-in capability to decode them

### blob [Binary Data]

The `blob` topic tree handles large binary files:

* File data is sent as a binary payload of a JSON message
* The JSON envelope is serialized using [protobuf](https://protobuf.dev/) protocol
* Schema defined in [blob.proto](https://github.com/cmu-mfi/mfi_ddb_library/blob/main/schema/blob.proto)
* Messages can be decoded using the protobuf schema

### kv [Non-Time-Series]

The `kv` topic tree handles non-time-series data:

* Designed to be flexible and extensible for different data types
* Schema defined in [kv.json](https://github.com/cmu-mfi/mfi_ddb_library/blob/main/schema/kv.json)
* Messages are sent as plain JSON (unlike blob/historian which use protobuf serialization)
* Suitable for metadata, configuration, status updates, and event notifications

## Streaming Metadata

When streaming data to the broker, the following metadata is recorded through the `mfi-ddb` stream:

| Metadata | Description | Recorded As |
|----------|-------------|-------------|
| Location context | Enterprise, site, area, device location of the data | [Topic structure](#topic-structure) |
| Attributes | Key-value pairs providing additional information about the data | Streamed on the same topic before data using the same encoding format |
| Streaming configuration | Configuration including broker info, enterprise/site details | Streamed on `kv` and `blob` at birth/death of streaming |
| Adapter configuration | Full adapter config with all components and attributes | Streamed on `kv` and `blob` at birth/death of streaming |

## Schema Versioning

The current schema version is **V1.0**. Future versions will be backward-compatible where possible. Breaking changes will be indicated by a major version bump (e.g., V2.0).