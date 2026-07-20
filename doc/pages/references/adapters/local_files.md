# Local Files Adapter

The Local Files data adapter reads data from files stored on the local filesystem, making it ideal for batch processing of historical or offline data.

## Overview

This adapter loads structured data (CSV, JSON) from a specified directory and publishes it to the DDB topic structure. It's designed for scenarios where data is already collected and stored locally — such as from previous test runs, lab experiments, or file-based data exports.

| Property | Value |
|----------|-------|
| **Adapter Type** | `local_files` |
| **Data Source** | Local filesystem (CSV/JSON files) |
| **Recommended Topic Family** | `historian` |
| **Self-Update** | No (one-time load or manual trigger) |

## Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `file_path` | Yes | Path to the directory containing data files | `"./data/"` |
| `trial_id` | Yes | Trial ID for the system (no spaces or special characters) | `"trial_001"` |

## Supported File Formats

- **CSV** — Row-based tabular data with headers as column names
- **JSON** — Nested JSON objects supporting hierarchical data structures

## How It Works

1. **File Discovery** — Scans the `file_path` directory for supported file formats (`.csv`, `.json`).
2. **Data Parsing** — Reads and parses each file, extracting metadata (filename, size) and content.
3. **Data Publishing** — Publishes parsed data to DDB topics under the configured namespace with appropriate component IDs derived from filenames.

## Use Cases

1. **Historical Data Ingestion** — Load previously collected experimental or production data into DDB
2. **Offline Batch Processing** — Process large datasets without network connectivity
3. **Data Migration** — Migrate data from file-based storage systems to the Digital Data Backbone
4. **Testing & Development** — Quickly load sample datasets for application development and testing

## Related Links

- [`mfi_ddb_data_adapter` Source Code](https://github.com/cmu-mfi/mfi_ddb_library/tree/main/mfi_ddb_package/src/mfi_ddb/data_adapters)