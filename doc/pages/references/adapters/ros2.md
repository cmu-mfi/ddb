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

| Parameter | Description |
|-----------|-------------|
| `trial_id` | Trial ID for the ROS device. No spaces or special characters allowed. |
| `devices` | List of devices to subscribe to. |
| `devices[].namespace` | Namespace of the device in ROS |
| `devices[].rostopics` | List of ROS topics to subscribe to for this device |
| `devices[].attributes` | Attributes of the device. Optional. |

## Example Configuration

```yaml
adapter_name: my_ros2_adapter

trial_id: "trial_001"
devices:
  device1:
    namespace: "robot_arm"
    rostopics:
      - "/joint_states"
      - "/camera/image_raw"
    attributes:
      manufacturer: "RobotCorp"
      model: "RobotArmX"
      description: "A robotic arm for testing purposes."
  device2:
    namespace: "machine_a"
    rostopics:
      - "/machine_a/status"
    attributes:
      manufacturer: "MachineCorp"
      version: 0.1
      description: "A machine for testing purposes."
```

## Related Links

- [ROS2 Documentation](https://docs.ros.org/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)
