
# Software

<a href="https://github.com/cmu-mfi/mfi_ddb_library" class="inline-button"><i class="fab fa-github"></i>mfi_ddb_library</a>

The main source code in the mfi-ddb-library is organized as shown below.

```
src/
└── mfi_ddb
    ├── data_adapters
    │   ├── base.py
    │   ├── grpc.py
    │   ├── __init__.py
    │   ├── local_files.py
    │   ├── mqtt.py
    │   ├── mtconnect.py
    │   ├── ros_files.py
    │   └── ros.py
    ├── __init__.py
    ├── scripts
    │   ├── generate_config_examples.py
    │   ├── store_cfs.py
    │   └── stream_data.py
    ├── streamer
    │   ├── __init__.py
    │   ├── _mqtt.py
    │   ├── _mqtt_spb.py
    │   ├── mqtt_spb_wrapper/
    │   ├── observer.py
    │   ├── streamer.py
    │   └── subscriber.py
    ├── topic_families
    │   ├── base.py
    │   ├── blob.py
    │   ├── historian.py
    │   ├── __init__.py
    │   ├── key_value.py
    │   └── schema
    │       ├── blob_pb2.py
    │       └── blob.proto
    └── utils
        ├── exceptions.py
        ├── __init__.py
        └── script_utils.py
```

More details: [https://github.com/cmu-mfi/mfi_ddb_library](https://github.com/cmu-mfi/mfi_ddb_library)