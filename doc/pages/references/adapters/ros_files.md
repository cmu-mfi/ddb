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

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `ros_files.trial_id` | Yes | Trial ID for the ROS device. No spaces or special characters allowed. | `"trial_001"` |
| `ros_files.set_ros_callback` | No | Set ROS callback to receive data from ROS topics (default: True) | `true` |
| `ros_files.max_wait_per_topic` | No | Maximum wait time in seconds per topic when polling (default: 1) | `1` |
| `ros_files.devices` | Yes | List of devices to subscribe to (see below) | — |

### Devices Configuration

Each device in the `devices` list must include:

| Field | Description |
|-------|-------------|
| `namespace` | Namespace of the device in ROS |
| `rostopics` | List of ROS topics to subscribe to for this device |
| `attributes` | Optional attributes (manufacturer, model, description) |

## Supported Message Types

| ROS Message Type | File Format | Handler Class |
|-----------------|-------------|---------------|
| `sensor_msgs/Image` | PNG (`.png`) | `ImageHandler` |
| `sensor_msgs/PointCloud2` | PLY (`.ply`) | `PCDHandler` |

## Example Configuration

```yaml
adapter_type: ros_files
name: my_ros_files_adapter
ros_files:
  trial_id: "trial_001"
  set_ros_callback: true
  devices:
    - namespace: "robot_arm"
      rostopics: ["/camera/image_raw"]
      attributes:
        manufacturer: "RobotCorp"
        model: "CameraX"
topic_family: blob
```

## How It Works

1. **ROS Master Check** — Verifies that a ROS master is running on the system.
2. **Topic Validation** — Checks if listed topics exist and validates they use compatible message types (Image or PointCloud2). Incompatible topics are automatically removed with a warning.
3. **Subscription** — Creates ROS subscribers for each configured topic with callback handlers.
4. **Data Collection** — Receives messages via callbacks, converts them to binary file format (PNG/PLY), and publishes the file blob data (including filename, file type, timestamp, raw bytes, and size) to DDB topics.

## Use Cases

1. **Visual Inspection Data Capture** — Save images from ROS-connected cameras for quality inspection
2. **3D Scanning & Reconstruction** — Capture point cloud data from 3D sensors for digital twin modeling
3. **Production Line Imaging** — Record images at key production stages for traceability
4. **Research & Development** — Capture visual data from ROS simulations or physical robots for analysis

## Related Links

- [ROS Documentation](https://www.ros.org/documentation/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)