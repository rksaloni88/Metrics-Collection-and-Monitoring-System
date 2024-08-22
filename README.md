# Metrics Collection and Monitoring System

## Overview

This project implements a simple metrics collection and monitoring system. It captures system metrics, stores them in an SQLite database, provides a RESTful API to query these metrics, triggers alerts based on predefined thresholds, and visualizes the metrics using Grafana.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Initialize the Database](#1-initialize-the-database)
  - [2. Start Metrics Collection](#2-start-metrics-collection)
  - [3. Run the RESTful API](#3-run-the-restful-api)
  - [4. Start the Alerting Mechanism](#4-start-the-alerting-mechanism)
  - [5. Configure Grafana](#5-configure-grafana)
- [API Endpoints](#api-endpoints)
- [Alerting](#alerting)
- [Visualization](#visualization)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.x
- Virtual Environment (optional but recommended)
- SQLite
- Grafana

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://your-repo-url.git
   cd metrics_collection_project
   ```

2. **Set up a virtual environment**:
   ```sh
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
   ```

3. **Install the required Python packages:**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Install Grafana**:
   ```sh
   brew install grafana
   brew services start grafana
   ```

## Usage

1. **Initialize the database**:

   ```sh
   python sqlite_db.py
   ```

2. Start Metrics Collection
   Run the metrics collector script:

   ```sh
   python metrics_collector.py
   ```

3. Run the RESTful API
   Start the Flask app to serve the API:

   ```sh
   python api.py
   ```

4. Start the Alerting Mechanism
   Run the alerting script to monitor metrics and trigger alerts:

   ```sh
   python alerting.py
   ```

5. Configure Grafana
   Install the SQLite data source plugin:

   ```sh
   grafana-cli plugins install frser-sqlite-datasource
   brew services restart grafana
   ```

## Add Data Source:

Open Grafana (http://localhost:3000) and log in (default credentials: admin/admin).
Navigate to Configuration -> Data Sources -> Add data source -> SQLite.
Provide the path to your SQLite database file (/path/to/metrics.db).
Create Dashboards:

Navigate to Create -> Dashboard.
Add panels to visualize CPU, memory, disk I/O, and network I/O metrics.
Use appropriate queries to fetch data from the SQLite database.

## API Endpoints
Retrieve metrics for a specific time range:

   ```sh
   GET /metrics?start=<start_time>&end=<end_time>
   ```
Get average metrics over the last hour:

   ```sh
   GET /metrics/average?type=<metric_type>
   ```
Get minimum metrics over the last day:

   ```sh
   GET /metrics/min?type=<metric_type>
   ```

Get maximum metrics over the last day:

   ```sh
   GET /metrics/max?type=<metric_type>
   ```

## Alerting
The alerting mechanism checks for predefined thresholds (e.g., CPU usage > 80% for 5 minutes) and triggers alerts via email and logs them to a file.

Configure alert settings in alerting.py:

**CPU_THRESHOLD**: CPU usage threshold in percentage
**CHECK_INTERVAL**: Time interval between checks in seconds
**ALERT_DURATION**: Duration to check for threshold in seconds

## Visualization
Visualize the collected metrics using Grafana. Install and configure the SQLite data source plugin, then create dashboards with panels querying the metrics database.

Example Queries for Grafana Panels
CPU Usage Panel:

   ```sql
   SELECT timestamp, cpu FROM metrics WHERE $__timeFilter(timestamp)
   ```

Memory Usage Panel:

   ```sql
   SELECT timestamp, memory FROM metrics WHERE $__timeFilter(timestamp)
   ```

Disk I/O Panel:

   ```sql
   SELECT timestamp, disk_io FROM metrics WHERE $__timeFilter(timestamp)
   ```

Network I/O Panel:

   ```sql
   SELECT timestamp, network_io FROM metrics WHERE $__timeFilter(timestamp)
   ```

## Testing

Verify metrics collection:

Check the output of metrics_collector.py.

Query the SQLite database:
   ```sh
   sqlite3 metrics.db
   SELECT * FROM metrics LIMIT 10;
   ```

## Test API endpoints:

Use tools like curl, httpie, or Postman.
Example:
   ```sh
   curl -u admin:password "http://127.0.0.1:5000/metrics?start=2023-08-07%2010:03:13&end=2023-08-07%2010:03:43"
   ```

## Check alerts:

Simulate high CPU usage to trigger alerts.
Check alerts.log and email notifications.

## Verify Grafana dashboards:

Open Grafana and check the metrics visualization.
Contributing
Contributions are welcome! Please open an issue or submit a pull request.

