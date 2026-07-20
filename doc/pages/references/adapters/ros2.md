# ROS2 Adapter

The ROS2 data adapter subscribes to ROS2 topics and streams sensor/actuator data into the DDB topic structure. It connects to a running ROS2 system using `rclpy` and receives real-time messages from any configured ROS2-enabled device.

## Overview

This adapter integrates with existing ROS2-based robotic systems, subscribing to live ROS2 topics and publishing their data as key-value pairs under the DDB namespace. It uses `rclpy` for node management and handles message deserialization, byte-data filtering for large arrays (e.g., images), and topic name mapping.

| Property | Value |
|----------|-------|
| **Adapter Type** | `ros2` |
| **Data Source** | ROS2 topics |
| **Recommended Topic Family** | `historian` |
| **Self-Update** | Yes (ROS2 callback-based) |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `ros2.trial_id` | Yes | Trial ID for the ROS device. No spaces or special characters allowed. | `"trial_001"` |
| `ros2.devices` | Yes | List of devices to subscribe to (see below) | — |

### Devices Configuration

Each device in the `devices` list must include:

| Field | Description |
|-------|-------------|
| `namespace` | Namespace of the device in ROS2 |
| `rostopics` | List of ROS2 topics to subscribe to for this device |
| `attributes` | Optional attributes (manufacturer, model, description) |

## Example Configuration

```yaml
adapter_type: ros2
name: my_ros2_adapter
ros2:
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

1. **ROS2 Initialization** — Initializes an `rclpy` node and prepares the ROS2 environment for topic subscription.
2. **Topic Discovery** — Queries the ROS2 system for available topics and verifies that all configured topics exist.
3. **Subscription** — Creates ROS2 subscriptions with QoS history depth (default: 10) and callback handlers using `rclpy.create_subscription()`.
4. **Data Collection** — Receives messages via callbacks, deserializes them into YAML format, filters out large byte arrays (uint8[]), and publishes to DDB topics under the namespace component ID.

## Use Cases

1. **ROS2 Robotic Data Integration** — Stream joint states, sensor data, and camera feeds from ROS2-enabled robots
2. **Modern Manufacturing Equipment Monitoring** — Connect ROS2-based robotic workcells to the Digital Data Backbone
3. **Multi-Device Aggregation** — Subscribe to multiple devices across different ROS2 namespaces
4. **Research & Development** — Capture real-time data from ROS2 simulations or physical robots for analysis

## Related Links

- [ROS2 Documentation](https://docs.ros.org/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)