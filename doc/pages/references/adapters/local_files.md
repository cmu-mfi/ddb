# Local Files Adapter

The Local Files data adapter watches local directories for new files and publishes them as file blobs into the DDB topic structure. It uses filesystem event monitoring to detect new files and stream them as they arrive.

## Overview

This adapter is designed for scenarios where files are continuously generated and need to be ingested into the Digital Data Backbone as blob data. It monitors configured directories for new files, buffers them, and publishes each file's content as a blob under the `blob` topic family.

| Property | Value |
|----------|-------|
| **Data Source** | Local filesystem (file watching) |
| **Recommended Topic Family** | `blob` |
| **Self-Update** | Yes (filesystem event-based via watchdog) |

## Configuration Parameters

| Parameter | Description |
|-----------|-------------|
| `watch_dir` | List of directories to watch for new files. |
| `buffer_size` | Maximum number of files to buffer before streaming. |
| `wait_before_read` | Time in seconds to wait before reading a new file. |
| `system` | System information including trial ID, name, and other attributes. |
| `system.trial_id` | Trial ID for the system. No spaces or special characters allowed. |
| `system.name` | Name of the system. |

## Example Configuration

```yaml
adapter_name: my_local_files_adapter

watch_dir:
  - "/path/to/watch/dir"
buffer_size: 10
wait_before_read: 2
system:
  name: "local_files_system"
  trial_id: "trial_001"
  description: "Local files data adapter system"
  manufacturer: "Example Corp"
  model: "LocalFilesModel"
```

## Related Links

- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)
