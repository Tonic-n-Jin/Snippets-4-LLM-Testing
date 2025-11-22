# Data Engineering Code Snippets

This directory contains **production-ready code examples** for Data Engineering, covering the complete data lifecycle from ingestion to observability.

![Data Engineering](https://img.shields.io/badge/Data-Engineering-2496ED?style=for-the-badge&logo=databricks&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Snippets](https://img.shields.io/badge/Snippets-26-green?style=for-the-badge)

> **Data Pipeline Flow**: Collect → Transform → Validate → Serve → Observe

---

## 📑 Table of Contents

| **Architecture & Infrastructure** | **Data Collection** | **Data Transformation** | **Data Delivery** |
| :--- | :--- | :--- | :--- |
| [🏛️ Design Patterns](#-design-patterns) | [📥 Ingestion Patterns](#-ingestion-patterns) | [✅ Quality Control](#-quality-control) | [📡 Data Serving](#-data-serving) |
| [🏗️ Infrastructure](#🏗-infrastructure) | [💾 Data Sources](#-data-sources) | [⚙️ Processing Logic](#⚙-processing-logic) | [📊 Observability](#-observability) |

---

## 🏛️ Design Patterns

*Architectural blueprints for scalable data systems*

### Lambda Architecture Implementation
> Batch + Stream processing for complete and accurate data
>
> ![Architecture](https://img.shields.io/badge/Pattern-Lambda-orange) ![Batch](https://img.shields.io/badge/Layer-Batch-blue) ![Stream](https://img.shields.io/badge/Layer-Stream-blue)

**File:** [`de-arch-patterns-1-lambda-architecture-implementation.py`](./de-arch-patterns-1-lambda-architecture-implementation.py)

### Kappa Architecture Stream Processing
> Stream-first processing with replay capabilities
>
> ![Architecture](https://img.shields.io/badge/Pattern-Kappa-orange) ![Stream](https://img.shields.io/badge/Stream-First-blue)

**File:** [`de-arch-patterns-2-kappa-architecture-stream-processing.py`](./de-arch-patterns-2-kappa-architecture-stream-processing.py)

### Data Mesh Domain Implementation
> Domain-oriented decentralized data ownership
>
> ![Architecture](https://img.shields.io/badge/Pattern-Data%20Mesh-orange) ![Domain](https://img.shields.io/badge/Ownership-Domain-blue)

**File:** [`de-arch-patterns-3-data-mesh-domain-implementation.py`](./de-arch-patterns-3-data-mesh-domain-implementation.py)


---

## 🏗️ Infrastructure

*The physical and logical foundation of data systems*

### Distributed Computing with Spark
> Spark, Flink, Beam - distributed processing at scale
>
> ![Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?logo=apachespark&logoColor=white) ![Flink](https://img.shields.io/badge/Apache%20Flink-E6526F?logo=apacheflink&logoColor=white) ![Beam](https://img.shields.io/badge/Apache%20Beam-E47220?logo=apachebeam&logoColor=white)

**File:** [`de-arch-infra-1-distributed-computing-with-spark.py`](./de-arch-infra-1-distributed-computing-with-spark.py)

### Hybrid Storage Architecture
> Data lakes, warehouses, and hybrid architectures
>
> ![S3](https://img.shields.io/badge/AWS%20S3-569A31?logo=amazons3&logoColor=white) ![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?logo=snowflake&logoColor=white) ![Redshift](https://img.shields.io/badge/Redshift-8C4FFF?logo=amazonredshift&logoColor=white)

**File:** [`de-arch-infra-2-hybrid-storage-architecture.py`](./de-arch-infra-2-hybrid-storage-architecture.py)

### Airflow DAG for ETL Pipeline
> Airflow, Prefect, Dagster - workflow automation
>
> ![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?logo=apacheairflow&logoColor=white) ![Prefect](https://img.shields.io/badge/Prefect-27B1FF?logoColor=white) ![Dagster](https://img.shields.io/badge/Dagster-654FF0?logoColor=white)

**File:** [`de-arch-infra-3-airflow-dag-for-etl-pipeline.py`](./de-arch-infra-3-airflow-dag-for-etl-pipeline.py)


---

## 📥 Ingestion Patterns

*Strategies for reliable data collection at scale*

### Change Data Capture (CDC) Consumer
> Real-time database replication with minimal impact
>
> ![CDC](https://img.shields.io/badge/Pattern-CDC-success) ![Debezium](https://img.shields.io/badge/Debezium-FF6600?logoColor=white) ![Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?logo=apachekafka&logoColor=white)

**File:** [`de-collect-ingest-1-change-data-capture-cdc-consumer.py`](./de-collect-ingest-1-change-data-capture-cdc-consumer.py)

### Application Event Producer (Kafka)
> Continuous flow of business events and metrics
>
> ![Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?logo=apachekafka&logoColor=white) ![Events](https://img.shields.io/badge/Pattern-Event%20Streaming-success)

**File:** [`de-collect-ingest-2-application-event-producer-kafka.py`](./de-collect-ingest-2-application-event-producer-kafka.py)

### Modular Batch ETL Job
> Scheduled bulk transfers for historical data
>
> ![ETL](https://img.shields.io/badge/Pattern-Batch%20ETL-success) ![Schedule](https://img.shields.io/badge/Mode-Scheduled-blue)

**File:** [`de-collect-ingest-3-modular-batch-etl-job.py`](./de-collect-ingest-3-modular-batch-etl-job.py)


---

## 💾 Data Sources

*Methods for connecting to databases, APIs, and file systems*

### Relational & NoSQL Connectors
> Querying transactional databases
>
> ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)

**File:** [`de-collect-sources-1-relational-nosql-connectors.py`](./de-collect-sources-1-relational-nosql-connectors.py)

### Robust API Client (Pagination)
> Ingesting data from SaaS & web services
>
> ![REST](https://img.shields.io/badge/REST-API-success) ![Requests](https://img.shields.io/badge/Requests-Library-blue) ![Retry](https://img.shields.io/badge/Pattern-Retry%20Logic-orange)

**File:** [`de-collect-sources-2-robust-api-client-pagination.py`](./de-collect-sources-2-robust-api-client-pagination.py)

### Blob & File Storage Connector (S3)
> Processing files (logs, CSV, Parquet)
>
> ![S3](https://img.shields.io/badge/AWS%20S3-569A31?logo=amazons3&logoColor=white) ![Boto3](https://img.shields.io/badge/Boto3-FF9900?logo=amazonaws&logoColor=white) ![Parquet](https://img.shields.io/badge/Parquet-50ABF1?logo=apache&logoColor=white)

**File:** [`de-collect-sources-3-blob-file-storage-connector-s3.py`](./de-collect-sources-3-blob-file-storage-connector-s3.py)


---

## ✅ Quality Control

*Ensuring data reliability through systematic validation*

### Completeness: Row Count & Metric Reconciliation
> Checking that actual records match expected records
>
> ![Validation](https://img.shields.io/badge/Type-Completeness-important) ![Metrics](https://img.shields.io/badge/Check-Row%20Count-blue)

**File:** [`de-transform-quality-1-completeness-row-count-metric-reconciliation.py`](./de-transform-quality-1-completeness-row-count-metric-reconciliation.py)

### Accuracy: Value Validation with Pandera
> Ensuring the correctness of data values
>
> ![Validation](https://img.shields.io/badge/Type-Accuracy-important) ![Pandera](https://img.shields.io/badge/Pandera-Schema-blue) ![Schema](https://img.shields.io/badge/Pattern-Schema%20Validation-orange)

**File:** [`de-transform-quality-2-accuracy-value-validation-with-pandera.py`](./de-transform-quality-2-accuracy-value-validation-with-pandera.py)

### Consistency: Cross-System Referential Integrity
> Maintaining uniformity across different systems
>
> ![Validation](https://img.shields.io/badge/Type-Consistency-important) ![Integrity](https://img.shields.io/badge/Check-Referential-blue)

**File:** [`de-transform-quality-3-consistency-cross-system-referential-integrity.py`](./de-transform-quality-3-consistency-cross-system-referential-integrity.py)


---

## ⚙️ Processing Logic

*Transforming raw data into analytical assets*

### Data Cleansing Function
> Remove noise, handle nulls, fix inconsistencies
>
> ![Process](https://img.shields.io/badge/Type-Cleansing-9cf) ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)

**File:** [`de-transform-process-1-data-cleansing-function.py`](./de-transform-process-1-data-cleansing-function.py)

### Data Enrichment Function
> Add context, calculate metrics, join datasets
>
> ![Process](https://img.shields.io/badge/Type-Enrichment-9cf) ![Join](https://img.shields.io/badge/Pattern-Data%20Join-blue)

**File:** [`de-transform-process-2-data-enrichment-function.py`](./de-transform-process-2-data-enrichment-function.py)

### Data Aggregation Function
> Summarize, rollup, create analytical views
>
> ![Process](https://img.shields.io/badge/Type-Aggregation-9cf) ![Rollup](https://img.shields.io/badge/Pattern-Rollup-blue)

**File:** [`de-transform-process-3-data-aggregation-function.py`](./de-transform-process-3-data-aggregation-function.py)


---

## 📡 Data Serving

*Delivering the right data to the right place at the right time*

### Analytics Serving (Semantic Layer)
> OLAP cubes, semantic layers, BI tools
>
> ![OLAP](https://img.shields.io/badge/Type-OLAP-blueviolet) ![BI](https://img.shields.io/badge/Tools-BI-blue) ![Semantic](https://img.shields.io/badge/Layer-Semantic-orange)

**File:** [`de-deliver-serving-1-analytics-serving-semantic-layer.py`](./de-deliver-serving-1-analytics-serving-semantic-layer.py)

### ML Feature Store Client
> Consistent features for training and inference
>
> ![Features](https://img.shields.io/badge/Type-Feature%20Store-blueviolet) ![ML](https://img.shields.io/badge/For-ML-blue)

**File:** [`de-deliver-serving-2-ml-feature-store-client.py`](./de-deliver-serving-2-ml-feature-store-client.py)

### Data API Gateway (FastAPI)
> Real-time data access with SLA guarantees
>
> ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![API](https://img.shields.io/badge/Type-REST%20API-blueviolet) ![SLA](https://img.shields.io/badge/Guarantee-SLA-blue)

**File:** [`de-deliver-serving-3-data-api-gateway-fastapi.py`](./de-deliver-serving-3-data-api-gateway-fastapi.py)


---

## 📊 Observability

*Monitoring, alerting, and understanding data systems*

### Pipeline Metrics (Decorator)
> Latency, throughput, success rates
>
> ![Metrics](https://img.shields.io/badge/Type-Pipeline-informational) ![Decorator](https://img.shields.io/badge/Pattern-Decorator-orange) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)

**File:** [`de-deliver-observe-1-pipeline-metrics-decorator.py`](./de-deliver-observe-1-pipeline-metrics-decorator.py)

### Data Metrics (Drift & Quality)
> Volume trends, quality scores, drift detection
>
> ![Metrics](https://img.shields.io/badge/Type-Data%20Quality-informational) ![Drift](https://img.shields.io/badge/Detection-Drift-orange)

**File:** [`de-deliver-observe-2-data-metrics-drift-quality.py`](./de-deliver-observe-2-data-metrics-drift-quality.py)

### Business Metrics (SLA & Cost)
> SLA adherence, cost per GB, user satisfaction
>
> ![Metrics](https://img.shields.io/badge/Type-Business-informational) ![SLA](https://img.shields.io/badge/Track-SLA-blue) ![Cost](https://img.shields.io/badge/Track-Cost-blue)

**File:** [`de-deliver-observe-3-business-metrics-sla-cost.py`](./de-deliver-observe-3-business-metrics-sla-cost.py)


---
