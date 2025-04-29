This is a monorepo providing an llm log analysis platform.

## Overview
-   **`analyseLogs/`**: Contains a Python script designed to query logs from Elasticsearch and send them to the `dif` API for analysis.
-   **`dif/`**: Implements a web endpoint that receives log data and performs analysis, providing insights based on the provided logs.
-   **`elasticStack/`**: Houses the configuration and setup for the Elastic Stack (likely Filebeat, Elasticsearch, and Kibana) used for central log management and storage.
-   **`sample/`**: Includes a sample web application that generates logs which can be used for testing and demonstration purposes.

## Getting Started

To get started with the project, follow the instructions below for each component:

### Prerequisites

-   **Python 3.10+** (for `analyseLogs` script)
-   **Docker** 

### Running:

**`analyseLogs/`**:
- ```
  python main.py emailToSentAlertsTo@example.com -c {coma,separated,container,names}
  ```




**`dif/`**:
```
docker-compose build
docker-compose up -d
```
To run on port 8000

For more refer to the [DIF Endpoint README](dif/README.md)

**`elasticStack/`**:
- ```
  docker-compose build
  docker-compose up -d
  ```

**`sample/`**:
- ```
  docker build -t {img-name} .
  docker run -d -p 5000:5000 --name {container-name} {img-name}
  ```
  to run sample logging website on port 5000



