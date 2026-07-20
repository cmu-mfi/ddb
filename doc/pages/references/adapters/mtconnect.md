# MTConnect Adapter

The MTConnect (MTC) data adapter interfaces with MTConnect-enabled CNC machines to stream manufacturing data into the DDB. It probes the MTConnect agent for device capabilities and then polls for live data.

## Overview

MTConnect is an industrial standard that provides a framework for defining manufacturing equipment interface data. The MTC adapter connects to any MTConnect agent, discovers available components, and streams sensor readings into the Digital Data Backbone.

| Property | Value |
|----------|-------|
| **Adapter Type** | `mtconnect` |
| **Data Source** | Any MTConnect agent (CNC machines) |
| **Recommended Topic Family** | `historian` |
| **Self-Update** | No (polls via `get_data()`) |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `mtconnect.agent_ip` | Yes | IP address of the MTConnect agent | `"192.168.1.1"` |
| `mtconnect.agent_url` | Yes | URL of the MTConnect agent | `"http://192.168.1.1:5000"` |
| `mtconnect.device_name` | Yes | Name of the device to be used in the data object | `"MTConnectDevice"` |
| `mtconnect.trial_id` | Yes | Trial ID for the MTConnect device (no spaces or special characters) | `"trial_001"` |

## How It Works

1. **Agent Discovery** — Pings the agent IP to verify it is active, then probes the agent for available devices and components.
2. **Component Mapping** — Discovers all data items from each component and maps them to DDB component IDs (`{device_name}/{component_id}`).
3. **Data Collection** — Polls the agent for current or sample data via `get_data()`, parses XML responses, and publishes to MQTT under the historian topic family.

## Use Cases

1. **CNC Machine Monitoring** — Stream spindle speed, feed rate, temperature, and other manufacturing metrics from CNC machines
2. **Production Line Integration** — Connect multiple MTConnect-enabled devices across a production line
3. **Legacy Equipment Retrofit** — Bridge older industrial equipment with modern data architectures via MTConnect

## Related Links

- [MTConnect Specification](https://www.mtconnect.org/specifications/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)