# gRPC Adapter

The gRPC data adapter connects to gRPC services to stream data into the DDB. It supports unary RPC calls and dynamic protobuf compilation, making it suitable for microservices architectures.

## Overview

This adapter enables integration with any system that exposes a gRPC interface — common in modern cloud-native applications and microservice-based systems.

| Property | Value |
|----------|-------|
| **Adapter Type** | `grpc` |
| **Data Source** | Any gRPC service endpoint |
| **Recommended Topic Family** | `historian` |
| **Self-Update** | No (polls via `get_data()`) |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `server_address` | Yes | Network Address of the gRPC server | `"localhost"` |
| `server_port` | Yes | Port of the gRPC server | `50051` |
| `certificate_path` | No | Full path to the gRPC server certificate file (TLS) | `"/full/path/to/cert.pem"` |
| `protobufs_dir` | Yes | Full path to the directory containing `.proto` files | `"/full/path/to/protos"` |
| `compiled_protos_dir` | No | Full path to the compiled protobuf stubs (auto-generated if missing) | `"./compiled_protos"` |
| `trial_id` | Yes | Trial ID for the gRPC device. No spaces or special characters allowed. | `"exp1"` |
| `components` | Yes | List of gRPC components to monitor (see below) | — |

### Components Configuration

Each component in the `components` list must include:

| Field | Description |
|-------|-------------|
| `component_id` | ID of the gRPC component to monitor |
| `attributes` | Additional attributes for the gRPC component (optional dict) |
| `trial_id` | Trial ID override per component (defaults to top-level `trial_id`) |
| `proto_rel_path` | Relative path to the `.proto` file defining the gRPC service |
| `stub_class` | Name of the gRPC stub class to use for communication |
| `request_class` | Name of the request class to use for the gRPC service call |
| `request` | Request parameters as a dictionary |

## Example Configuration

```yaml
adapter_type: grpc
name: my_grpc_adapter

grpc:
  server_address: "localhost"
  server_port: 50051
  certificate_path: "/full/path/to/cert.pem"
  trial_id: "exp1"
  protobufs_dir: "/full/path/to/protos"
  compiled_protos_dir: "/full/path/to/compiled_protos"
  components:
    - component_id: "sensor.temperature"
      attributes:
        description: "Temperature sensor"
        unit: "Celsius"
      proto_rel_path: "relative/path/to/temperature.proto"
      stub_class: "TemperatureServiceStub"
      request_class: "TemperatureRequest"
      request:
        key1: "value1"
        key2: [1, 2, 3]
    - component_id: "sensor.humidity"
      attributes:
        description: "Humidity sensor"
        unit: "Percentage"
      proto_rel_path: "relative/path/to/humidity.proto"
      stub_class: "HumidityServiceStub"
      request_class: "HumidityRequest"
      request:
        threshold: 75
```

## How It Works

1. **Channel Creation** — Opens an insecure or TLS-secured gRPC channel to the server.
2. **Proto Compilation** — Dynamically compiles `.proto` files into Python stubs using `grpc_tools.protoc`.
3. **Data Collection** — Calls configured gRPC methods via `get_data()`, converts responses from protobuf to JSON, and publishes to MQTT under the DDB topic structure.

## Use Cases

1. **Microservices Integration** — Connect existing microservice architectures to the DDB
2. **Cloud Service Relay** — Stream data from cloud-hosted gRPC services on-premise
3. **Custom Sensor APIs** — Bridge proprietary sensor APIs exposed as gRPC endpoints

## Related Links

- [gRPC Documentation](https://grpc.io/docs/)
- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)