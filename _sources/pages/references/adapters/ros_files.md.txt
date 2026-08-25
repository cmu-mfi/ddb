# ROS Files Adapter

The ROS Files data adapter subscribes to ROS topics that carry image (sensor_msgs/Image) and point cloud (sensor_msgs/PointCloud2) messages, saving them as files (PNG/PLY) into the DDB blob topic structure. It is designed for capturing visual data from ROS-enabled cameras and 3D sensors.

## Overview

This adapter integrates with existing ROS1-based systems to capture image and point cloud data, converting ROS message formats into file blobs that can be stored and retrieved via the Digital Data Backbone. Unlike the standard ROS adapter which extracts key-value data from messages, this one saves the full binary content of compatible topics.

| Property | Value |
|----------|-------|
| **Adapter Type** | `ros_files` |
| **Data Source** | ROS1 Image and PointCloud2 topics |
| **Recommended Topic Family** | `blob` |
| **Self-Update** | Yes (ROS callback-based) |

## Configuration Parameters

| Parameter | Description |
|-----------|-------------|
| `trial_id` | Trial ID for the ROS device. No spaces or special characters allowed. |
| `set_ros_callback` | Set ROS callback to receive data from ROS topics. If set to False, you need to call get_data() method to get data from ROS topics. |
| `devices` | List of devices to subscribe to. |
| `devices[].namespace` | Namespace of the device in ROS |
| `devices[].rostopics` | List of ROS topics to subscribe to for this device |
| `devices[].attributes` | Attributes of the device. Optional. |

## Example Configuration

```yaml
adapter_name: my_ros_files_adapter

trial_id: "trial_001"
set_ros_callback: true
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
