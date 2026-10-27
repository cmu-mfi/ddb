# gRPC Adapter

The gRPC data adapter connects to gRPC services to stream data into the DDB. It supports unary RPC calls and dynamic protobuf compilation, making it suitable for microservices architectures.

## Overview

This adapter enables integration with any system that exposes a gRPC interface — common in modern cloud-native applications and microservice-based systems.

| Property | Value |
|----------|-------|
| **Data Source** | Any gRPC service endpoint |
| **Recommended Topic Family** | `historian` |
| **Self-Update** | No (polls via `get_data()`) |

## Configuration Parameters

| Parameter | Description |
|-----------|-------------|
| `server_address` | Network Address of the gRPC server |
| `server_port` | Port of the gRPC server |
| `certificate_path` | Full path to the gRPC server certificate file (optional) |
| `protobufs_dir` | Full path to the directory containing .proto files |
| `compiled_protos_dir` | Full path to the compiled protobuf stubs (optional) |
| `trial_id` | Trial ID for the gRPC device. No spaces or special characters allowed. |
| `components` | List of gRPC components to monitor |
| `components[].component_id` | ID of the gRPC component to monitor |
| `components[].attributes` | Additional attributes for the gRPC component (optional) |
| `components[].trial_id` | Trial ID for the gRPC device. No spaces or special characters allowed (optional) |
| `components[].proto_rel_path` | Relative path to the .proto file defining the gRPC service |
| `components[].request_method` | Name of the gRPC service method to call. Only `Read` method is supported. |
| `components[].stub_class` | Name of the gRPC stub class to use for communication |
| `components[].request_class` | Name of the request class to use for the gRPC service call. |
| `components[].request` | Request parameters for the gRPC service call |

## Example Configuration

```yaml
adapter_name: my_grpc_adapter

server_address: "localhost"
server_port: 50051
certificate_path: "/full/path/to/cert.pem"
trial_id: "exp1"
protobufs_dir: "/full/path/to/protos"
compiled_protos_dir: "/full/path/to/compiled_protos"
components:
  - component_id: "sensor.temperature"
    attributes:
      description: "something something"
      unit: "Celsius"
    proto_rel_path: "relative/path/to/temperature.proto"
    stub_class: "TemperatureServiceStub"
    request_class: "TemperatureRequest"
    request:
      key1: "value1"
      key2: [1, 2, 3]
  - component_id: "sensor.humidity"
    attributes:
      description: "something something"
      unit: "Percentage"
    trial_id: "exp1_parallelA"
    proto_rel_path: "relative/path/to/humidity.proto"
    stub_class: "HumidityServiceStub"
    request_class: "HumidityRequest"
    request:
      threshold: 75
```

## Related Links

- [gRPC Documentation](https://grpc.io/docs/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)
