# Data Engineering Code Snippets

This directory contains code examples for Data Engineering.

## Table of Contents

- [Design Patterns](#design-patterns)
- [Infrastructure](#infrastructure)
- [Ingestion Patterns](#ingestion-patterns)
- [Data Sources](#data-sources)
- [Quality Control](#quality-control)
- [Processing Logic](#processing-logic)
- [Data Serving](#data-serving)
- [Observability](#observability)

---

## Design Patterns

*Architectural blueprints for scalable data systems*

### Lambda Architecture Implementation

Batch + Stream processing for complete and accurate data

**File:** [`de-arch-patterns-1-lambda-architecture-implementation.py`](./de-arch-patterns-1-lambda-architecture-implementation.py)

### Kappa Architecture Stream Processing

Stream-first processing with replay capabilities

**File:** [`de-arch-patterns-2-kappa-architecture-stream-processing.py`](./de-arch-patterns-2-kappa-architecture-stream-processing.py)

### Data Mesh Domain Implementation

Domain-oriented decentralized data ownership

**File:** [`de-arch-patterns-3-data-mesh-domain-implementation.py`](./de-arch-patterns-3-data-mesh-domain-implementation.py)


---

## Infrastructure

*The physical and logical foundation of data systems*

### Distributed Computing with Spark

Spark, Flink, Beam - distributed processing at scale

**File:** [`de-arch-infra-1-distributed-computing-with-spark.py`](./de-arch-infra-1-distributed-computing-with-spark.py)

### Hybrid Storage Architecture

Data lakes, warehouses, and hybrid architectures

**File:** [`de-arch-infra-2-hybrid-storage-architecture.py`](./de-arch-infra-2-hybrid-storage-architecture.py)

### Airflow DAG for ETL Pipeline

Airflow, Prefect, Dagster - workflow automation

**File:** [`de-arch-infra-3-airflow-dag-for-etl-pipeline.py`](./de-arch-infra-3-airflow-dag-for-etl-pipeline.py)


---

## Ingestion Patterns

*Strategies for reliable data collection at scale*

### Change Data Capture (CDC) Consumer

Real-time database replication with minimal impact

**File:** [`de-collect-ingest-1-change-data-capture-cdc-consumer.py`](./de-collect-ingest-1-change-data-capture-cdc-consumer.py)

### Application Event Producer (Kafka)

Continuous flow of business events and metrics

**File:** [`de-collect-ingest-2-application-event-producer-kafka.py`](./de-collect-ingest-2-application-event-producer-kafka.py)

### Modular Batch ETL Job

Scheduled bulk transfers for historical data

**File:** [`de-collect-ingest-3-modular-batch-etl-job.py`](./de-collect-ingest-3-modular-batch-etl-job.py)


---

## Data Sources

*Methods for connecting to databases, APIs, and file systems*

### Relational & NoSQL Connectors

Querying transactional databases

**File:** [`de-collect-sources-1-relational-nosql-connectors.py`](./de-collect-sources-1-relational-nosql-connectors.py)

### Robust API Client (Pagination)

Ingesting data from SaaS & web services

**File:** [`de-collect-sources-2-robust-api-client-pagination.py`](./de-collect-sources-2-robust-api-client-pagination.py)

### Blob & File Storage Connector (S3)

Processing files (logs, CSV, Parquet)

**File:** [`de-collect-sources-3-blob-file-storage-connector-s3.py`](./de-collect-sources-3-blob-file-storage-connector-s3.py)


---

## Quality Control

*Ensuring data reliability through systematic validation*

### Completeness: Row Count & Metric Reconciliation

Checking that actual records match expected records

**File:** [`de-transform-quality-1-completeness-row-count-metric-reconciliation.py`](./de-transform-quality-1-completeness-row-count-metric-reconciliation.py)

### Accuracy: Value Validation with Pandera

Ensuring the correctness of data values

**File:** [`de-transform-quality-2-accuracy-value-validation-with-pandera.py`](./de-transform-quality-2-accuracy-value-validation-with-pandera.py)

### Consistency: Cross-System Referential Integrity

Maintaining uniformity across different systems

**File:** [`de-transform-quality-3-consistency-cross-system-referential-integrity.py`](./de-transform-quality-3-consistency-cross-system-referential-integrity.py)


---

## Processing Logic

*Transforming raw data into analytical assets*

### Data Cleansing Function

Remove noise, handle nulls, fix inconsistencies

**File:** [`de-transform-process-1-data-cleansing-function.py`](./de-transform-process-1-data-cleansing-function.py)

### Data Enrichment Function

Add context, calculate metrics, join datasets

**File:** [`de-transform-process-2-data-enrichment-function.py`](./de-transform-process-2-data-enrichment-function.py)

### Data Aggregation Function

Summarize, rollup, create analytical views

**File:** [`de-transform-process-3-data-aggregation-function.py`](./de-transform-process-3-data-aggregation-function.py)


---

## Data Serving

*Delivering the right data to the right place at the right time*

### Analytics Serving (Semantic Layer)

OLAP cubes, semantic layers, BI tools

**File:** [`de-deliver-serving-1-analytics-serving-semantic-layer.py`](./de-deliver-serving-1-analytics-serving-semantic-layer.py)

### ML Feature Store Client

Consistent features for training and inference

**File:** [`de-deliver-serving-2-ml-feature-store-client.py`](./de-deliver-serving-2-ml-feature-store-client.py)

### Data API Gateway (FastAPI)

Real-time data access with SLA guarantees

**File:** [`de-deliver-serving-3-data-api-gateway-fastapi.py`](./de-deliver-serving-3-data-api-gateway-fastapi.py)


---

## Observability

*Monitoring, alerting, and understanding data systems*

### Pipeline Metrics (Decorator)

Latency, throughput, success rates

**File:** [`de-deliver-observe-1-pipeline-metrics-decorator.py`](./de-deliver-observe-1-pipeline-metrics-decorator.py)

### Data Metrics (Drift & Quality)

Volume trends, quality scores, drift detection

**File:** [`de-deliver-observe-2-data-metrics-drift-quality.py`](./de-deliver-observe-2-data-metrics-drift-quality.py)

### Business Metrics (SLA & Cost)

SLA adherence, cost per GB, user satisfaction

**File:** [`de-deliver-observe-3-business-metrics-sla-cost.py`](./de-deliver-observe-3-business-metrics-sla-cost.py)


---
