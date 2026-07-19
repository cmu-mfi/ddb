# MTConnect Adapter

The MTConnect (MTC) data adapter interfaces with MTConnect-enabled CNC machines to stream manufacturing data into the DDB. It supports both pull and push modes for data collection.

## Overview

MTConnect is an industrial standard that provides a framework for defining manufacturing equipment interface data. The MTC adapter translates MTConnect data streams into DDB format for publishing via MQTT.

| Property | Value |
|----------|-------|
| **Adapter Type** | `mtconnect` |
| **Data Source** | MTConnect-enabled CNC machines |
| **Supported Protocols** | MTConnect 1.4 / 2.0 |
| **Stream Format** | Sparkplug B (historian) or JSON (kv) |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `device_url` | Yes | URL of the MTConnect device | `http://localhost:7879` |
| `push_mode` | No | Use push (true) or pull (false) mode | `false` |
| `data_format` | No | Output format: `historian` or `kv` | `historian` |

## Pull Mode vs Push Mode

### Pull Mode (Default)

The adapter periodically requests data from the MTConnect device at configured intervals.

```yaml
mtconnect_adapter:
  device_url: "http://your-machine:7879"
  push_mode: false      # Pull mode (default)
  polling_interval_ms: 1000
```

### Push Mode

The MTConnect device actively pushes data to the adapter when events occur.

```yaml
mtconnect_adapter:
  device_url: "http://your-machine:7879"
  push_mode: true       # Enable push mode
  event_endpoint: "/events"
```

## Supported Data Types

The MTC adapter can stream the following MTConnect data types:

| Data Type | Description | Example Metrics |
|-----------|-------------|-----------------|
| `Sample` | Periodic measurements | spindle_speed, feed_rate, temperature |
| `Event` | State changes | mode_change, tool_change, alarm |
| `Condition` | Continuous conditions | coolant_level, vibration |

## Topic Mapping

When streaming in **historian** format (Sparkplug B), data is published to:

```
mfi-v1.0-historian/{enterprise}/{site}/[area]/{device}
```

Example topic:
```
mfi-v1.0-historian/CMU/Mill19/Lab/HAAS-UMC750
```

When streaming in **kv** format (JSON), data is published to:

```
mfi-v1.0-kv/{enterprise}/{site}/mtconnect/{device}
```

Example topic:
```
mfi-v1.0-kv/CMU/Mill19/mtconnect/HAAS-UMC750
```

## Metric Naming Convention

MTConnect metrics follow the naming convention defined in the DDB [historian-metric-naming.md](https://github.com/cmu-mfi/mfi_ddb_library/blob/main/schema/historian-metric-naming.md). Key rules:

- Use lowercase snake_case for metric names
- Include units where applicable (e.g., `spindle_speed_rpm`)
- Group related metrics under consistent prefixes (e.g., `cnc_`, `robot_`)

## Example Configuration

```yaml
# Full MTConnect adapter configuration
adapter_type: mtconnect
name: mill19_cnc_adapter

streamer:
  broker_host: "mqtt-broker"
  broker_port: 1883
  use_tls: false

topic_family: historian
namespace: mfi-v1.0
enterprise: CMU
site: Mill19
area: Lab
device: HAAS-UMC750

attributes:
  description: "HAAS UMC-750 machining center"
  manufacturer: "HAAS Automation"
  model: "UMC-750"
  sampling_rate: "1s"

mtconnect_adapter:
  device_url: "http://192.168.1.100:7879"
  push_mode: false
  polling_interval_ms: 1000
```

## Troubleshooting

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Connection refused | Device not accessible | Verify `device_url` is correct and device is powered on |
| No data received | Polling interval too long | Reduce `polling_interval_ms` or switch to push mode |
| Schema mismatch | Format incompatibility | Check that `data_format` matches your target topic family |

## Related Links

- [MTConnect Specification](https://www.mtconnect.org/specifications/)
- [`mfi_ddb_data_adapter`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_data_adapter) — Data adapter app repository