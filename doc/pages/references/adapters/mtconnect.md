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

| Parameter | Description |
|-----------|-------------|
| `mtconnect.agent_ip` | IP address of the MTConnect agent |
| `mtconnect.agent_url` | URL of the MTConnect agent |
| `mtconnect.device_name` | Name of the device to be used in the data object |
| `mtconnect.trial_id` | Trial ID for the MTConnect device. No spaces or special characters allowed. |

## Example Configuration

```yaml
adapter_name: my_mtconnect_adapter

mtconnect:
  agent_ip: "192.168.1.1"
  agent_url: "http://192.168.1.1:5000"
  device_name: "MTConnectDevice"
  trial_id: "trial_001"
```

## Related Links

- [MTConnect Specification](https://www.mtconnect.org/specifications/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)
