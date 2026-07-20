# ROS Adapter

The ROS (Robot Operating System) data adapter subscribes to ROS topics and streams sensor/actuator data into the DDB topic structure. It connects to a running ROS master and receives real-time messages from any configured ROS-enabled device.

## Overview

This adapter integrates with existing ROS1-based robotic systems, subscribing to live ROS topics and publishing their data as key-value pairs under the DDB namespace. It handles message deserialization, byte-data filtering for large arrays (e.g., images), and topic name mapping.

| Property | Value |
|----------|-------|
| **Adapter Type** | `ros` |
| **Data Source** | ROS1 topics |
| **Recommended Topic Family** | `historian` |
| **Self-Update** | Yes (ROS callback-based) |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `ros.trial_id` | Yes | Trial ID for the ROS device. No spaces or special characters allowed. | `"trial_001"` |
| `ros.devices` | Yes | List of devices to subscribe to (see below) | — |

### Devices Configuration

Each device in the `devices` list must include:

| Field | Description |
|-------|-------------|
| `namespace` | Namespace of the device in ROS |
| `rostopics` | List of ROS topics to subscribe to for this device |
| `attributes` | Optional attributes (manufacturer, model, description) |

## Example Configuration

```yaml
adapter_type: ros
name: my_ros_adapter
ros:
  trial_id: "trial_001"
  devices:
    - namespace: "robot_arm"
      rostopics: ["/joint_states", "/camera/image_raw"]
      attributes:
        manufacturer: "RobotCorp"
        model: "RobotArmX"
        description: "A robotic arm for testing purposes."
    - namespace: "machine_a"
      rostopics: ["/machine_a/status"]
      attributes:
        manufacturer: "MachineCorp"
topic_family: historian
```

## How It Works

1. **ROS Master Check** — Verifies that a ROS master is running on the system.
2. **Topic Discovery** — Checks if listed ROS topics exist and retrieves their message types.
3. **Subscription** — Creates ROS subscribers for each configured topic with callback handlers.
4. **Data Collection** — Receives messages via callbacks, deserializes them, filters out large byte arrays (uint8[]), and publishes to DDB topics under the namespace component ID.

## Use Cases

1. **Robotic Data Integration** — Stream joint states, sensor data, and camera feeds from ROS-enabled robots
2. **Manufacturing Equipment Monitoring** — Connect ROS-based robotic workcells to the Digital Data Backbone
3. **Multi-Device Aggregation** — Subscribe to multiple devices across different ROS namespaces
4. **Research & Development** — Capture real-time data from ROS simulations or physical robots for analysis

## Related Links

- [ROS Documentation](https://www.ros.org/documentation/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)