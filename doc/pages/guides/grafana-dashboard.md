# Make Your Grafana Dashboard

This guide walks you through connecting Grafana to your DDB data sources and building real-time monitoring dashboards for your manufacturing equipment.

## Prerequisites

- A running DDB system with at least one database node storing time-series data (see [Connect a Database Node](connect-database-node.md))
- Grafana installed and running ([installation guide](https://grafana.com/docs/grafana/latest/setup-grafana/installation/))
- Access to your MQTT broker or TimescaleDB/Aveva PI instance

## Connecting Data Sources to Grafana

### Option 1: Direct from MQTT Broker (Recommended for Real-Time)

Grafana can subscribe directly to MQTT topics for real-time visualization.

1. Open Grafana → **Connections** → **Add data source**
2. Select **MQTT** as the data source type
3. Configure the connection:

```yaml
Connection:
  Broker URL: tcp://localhost:1883
  Client ID: grafana-mqtt-consumer
  
Topic Filter: mfi-v1.0-historian/CMU/Mill19/#
QoS: 1
```

4. Click **Save & Test** — you should see a "Data source is working" message

### Option 2: From TimescaleDB (For SQL Queries)

If using the TimescaleDB database node, connect Grafana directly to PostgreSQL:

1. Open Grafana → **Connections** → **Add data source**
2. Select **PostgreSQL**
3. Configure:

```yaml
Host: localhost:5432
Database: ddb_historian
User: ddb_user
Password: ddb_password
```

4. Click **Save & Test**

### Option 3: From Aveva PI

For Aveva PI deployments, use the Web API connector:

1. Open Grafana → **Connections** → **Add data source**
2. Select **Aveva PI Server** (or use a community plugin)
3. Configure connection to your PI Web API endpoint

## Building Your Dashboard

### Step 1: Create a New Dashboard

1. Click the **Grafana menu** (☰) → **Dashboards** → **New dashboard**
2. Click **Add visualization**

### Step 2: Query Time-Series Data

#### From MQTT Data Source

```sql
-- Use the Explore view to query MQTT topics
SELECT 
  timestamp,
  value
FROM "mfi-v1.0-historian/CMU/Mill19/Lab/#"
WHERE topic =~ /.*spindle_speed.*/
ORDER BY timestamp DESC
LIMIT 1000
```

#### From TimescaleDB

```sql
SELECT 
  time_bucket('5 minutes', "timestamp") AS five_min,
  AVG(spindle_speed) AS avg_spindle_speed,
  MAX(feed_rate) AS max_feed_rate,
  MIN(temperature) AS min_temperature
FROM measurements
WHERE device = 'HAAS-UMC750'
  AND "timestamp" BETWEEN now() - interval '24 hours' AND now()
GROUP BY five_min
ORDER BY five_min DESC
```

### Step 3: Choose Visualization Types

| Data Type | Recommended Visualization | Purpose |
|-----------|--------------------------|---------|
| Sensor readings over time | **Time series** | Track trends, spikes, anomalies |
| Equipment status (on/off) | **Stat panel** | Quick glance at current state |
| Multiple metrics comparison | **Table** | Compare values across machines |
| Threshold alerts | **Gauge** | Show if values are within range |
| Data distribution | **Bar chart / Heatmap** | Identify patterns in data frequency |

### Step 4: Add Alerts and Thresholds

1. In your panel, click the **Alert** tab
2. Set conditions (e.g., "alert when temperature > 80°C")
3. Configure notification channels (email, Slack, etc.)

## Example Dashboard Layout

A typical manufacturing monitoring dashboard might include:

```
┌─────────────────────────────────────────────────────────┐
│  Equipment Overview                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐               │
│  │ Status   │ │ Temp     │ │ Spindle  │               │
│  │ ON/OFF   │ │ Gauge    │ │ Speed    │               │
│  └──────────┘ └──────────┘ └──────────┘               │
├─────────────────────────────────────────────────────────┤
│  Real-Time Sensor Data (Last 1 Hour)                    │
│  ┌─────────────────────────────────────────────────────┐│
│  │ [Time Series Chart: Temperature, Pressure, Vibration]││
│  └─────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────┤
│  Equipment Comparison                                   │
│  ┌──────────────────┐ ┌──────────────────┐             │
│  │ Bar Chart        │ │ Table            │             │
│  │ Avg. Output      │ │ Machine Status   │             │
│  │ by Device        │ │ (Status, Last    │             │
│  │                  │ │  Update, Uptime) │             │
│  └──────────────────┘ └──────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

## Using Grafana Variables for Dynamic Dashboards

Create template variables to make your dashboard interactive:

1. Go to **Dashboard settings** → **Variables** → **Add variable**
2. Create a variable named `device`:

```yaml
Name: device
Type: Query
Data source: MQTT Broker
Query: show topics like "mfi-v1.0-historian/CMU/Mill19/#"
```

3. Use the variable in your queries:

```sql
SELECT * FROM "mfi-v1.0-historian/CMU/Mill19/{{device}}"
WHERE topic =~ /.*temperature.*/
ORDER BY timestamp DESC
LIMIT 500
```

Now you can switch between devices using a dropdown at the top of your dashboard.

## Tips for Manufacturing Dashboards

- **Use appropriate time buckets** — Match aggregation intervals to your sampling rate (e.g., 1-second data → 1-minute or 5-minute buckets)
- **Set refresh intervals wisely** — Real-time MQTT feeds can handle frequent refreshes; SQL queries should use longer intervals
- **Group panels by equipment** — Keep all data for a single machine on one dashboard row
- **Use color thresholds** — Highlight warning and critical states with red/yellow/green indicators
- **Leverage annotations** — Mark maintenance events or process changes as vertical lines on your charts

## Next Steps

- Explore the full [Retrieval API](use-retrieval-api.md) for programmatic data access
- Learn about the [Payload Schema](../references/payload-schema.md) to understand data formats