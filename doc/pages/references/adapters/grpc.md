# gRPC Adapter

The gRPC data adapter connects to gRPC services to stream data into the DDB. It supports both unary and streaming RPC calls, making it suitable for microservices architectures.

## Overview

This adapter enables integration with any system that exposes a gRPC interface — common in modern cloud-native applications and microservice-based systems.

| Property | Value |
|----------|-------|
| **Adapter Type** | `grpc` |
| **Data Source** | Any gRPC service endpoint |
| **Supported Formats** | JSON (kv), Sparkplug B (historian) |
| **Authentication** | TLS, OAuth2 tokens |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `host` | Yes | gRPC service host address | `localhost:50051` |
| `service` | Yes | Target service name (proto definition) | `SensorService` |
| `rpc_method` | Yes | RPC method to call | `GetReadings` |
| `data_format` | No | Output format: `kv` or `historian` | `kv` |

## Example Configuration

```yaml
adapter_type: grpc
name: sensor_service_adapter

streamer:
  broker_host: "localhost"
  broker_port: 1883

topic_family: kv
namespace: mfi-v1.0
enterprise: CMU
site: Mill19

attributes:
  description: "Stream data from IoT sensor gRPC service"

grpc_adapter:
  host: "sensor-service.local:50051"
  service: "SensorService"
  rpc_method: "GetReadings"
  use_tls: false
```

## Use Cases

1. **Microservices Integration** — Connect existing microservice architectures to the DDB
2. **Cloud Service Relay** — Stream data from cloud-hosted gRPC services on-premise
3. **Custom Sensor APIs** — Bridge proprietary sensor APIs exposed as gRPC endpoints

## Related Links

- [gRPC Documentation](https://grpc.io/docs/)
- [`mfi_ddb_data_adapter`](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_data_adapter)