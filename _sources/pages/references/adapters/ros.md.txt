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

| Parameter | Description |
|-----------|-------------|
| `trial_id` | Trial ID for the ROS device. No spaces or special characters allowed. |
| `devices` | List of devices to subscribe to. |
| `devices[].namespace` | Namespace of the device in ROS |
| `devices[].rostopics` | List of ROS topics to subscribe to for this device |
| `devices[].attributes` | Attributes of the device. Optional. |

## Example Configuration

```yaml
adapter_name: my_ros_adapter

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

- [ROS Documentation](https://www.ros.org/documentation/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)
