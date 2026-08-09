# Make Your Grafana Dashboard

This guide walks you through connecting Grafana to your DDB data sources and building real-time monitoring dashboards for your manufacturing equipment.

## Prerequisites

- A running DDB system with at least one database node storing time-series data (see [Connect a Database Node](connect-database-node.md))
- Grafana installed and running ([installation guide](https://grafana.com/docs/grafana/latest/setup-grafana/installation/))
- Access to your MQTT broker or TimescaleDB/Aveva PI instance


```{note}
* Specific ports and dashboard below are applicable if setting up mock publisher on single node setup as per the steps in {ref}`quickstart` and {ref}`daa-guide`
* If using custom setup, edit the example `RWS Infinity` dashboard as necessary.
```

## Connecting Data Sources to Grafana
<!-- include:grafana-guide -->

Once a connection is established, you can retrieve and visualize data using Grafana Infinity.

1. Open Grafana: [http://localhost:3005](http://localhost:3005).
2. Use `admin`/`admin` for username/password if logging in for the first time.
3. Dashboards --> RWS Infinity

<!-- insert screenshot -->

4. Use the dashboard's visualizations to view how your data changes over a selected time period.
5. Filter by user ID to check data for a specific user.

<!-- insert screenshot -->

<!-- end:grafana-guide -->
