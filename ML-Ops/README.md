# ML Ops Code Snippets

This directory contains **production-ready code examples** for ML Ops, covering the complete ML operations lifecycle from deployment to governance.

![ML Ops](https://img.shields.io/badge/ML-Ops-00ADD8?style=for-the-badge&logo=mlflow&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Snippets](https://img.shields.io/badge/Snippets-24-green?style=for-the-badge)

> **ML Ops Lifecycle**: Deploy → Monitor → Maintain → Govern

---

## 📑 Table of Contents

| **Deployment** | **Monitoring** | **Maintenance** | **Governance** |
| :--- | :--- | :--- | :--- |
| [🚀 Model Serving](#-model-serving) | [📊 Observability](#-observability) | [🔄 Retraining](#-retraining) | [📋 Compliance](#-compliance) |
| [🏗️ Infrastructure](#️-infrastructure) | [🔍 Drift Detection](#-drift-detection) | [📦 Versioning](#-versioning) | [💡 Explainability](#-explainability) |

---

## 🚀 Model Serving

*Deploying ML models for real-time and batch predictions*

### Batch Prediction Script
> Scheduled predictions for large datasets offline
>
> ![Serving](https://img.shields.io/badge/Type-Batch-success) ![Schedule](https://img.shields.io/badge/Mode-Offline-blue) ![Scale](https://img.shields.io/badge/Scale-Large-orange)

**File:** [`mlops-deploy-serving-1-batch-prediction-script.py`](./mlops-deploy-serving-1-batch-prediction-script.py)

### Real-time API with FastAPI
> Low-latency predictions via REST/gRPC endpoints
>
> ![Serving](https://img.shields.io/badge/Type-Real--time-success) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![REST](https://img.shields.io/badge/Protocol-REST-blue)

**File:** [`mlops-deploy-serving-2-real-time-api-with-fastapi.py`](./mlops-deploy-serving-2-real-time-api-with-fastapi.py)

### Stream Processing with Faust
> Continuous predictions on event streams
>
> ![Serving](https://img.shields.io/badge/Type-Stream-success) ![Faust](https://img.shields.io/badge/Faust-6A1B9A?logoColor=white) ![Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?logo=apachekafka&logoColor=white)

**File:** [`mlops-deploy-serving-3-stream-processing-with-faust.py`](./mlops-deploy-serving-3-stream-processing-with-faust.py)


---

## 🏗️ Infrastructure

*Scalable foundations for ML workloads*

### Docker Configuration
> Docker for reproducible environments
>
> ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) ![Container](https://img.shields.io/badge/Type-Container-blue) ![Reproducible](https://img.shields.io/badge/Mode-Reproducible-green)

**File:** [`Dockerfile`](./Dockerfile)

### Kubernetes Deployment
> Kubernetes for scaling and management
>
> ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white) ![Orchestration](https://img.shields.io/badge/Type-Orchestration-blue) ![Scale](https://img.shields.io/badge/Feature-Auto--Scale-orange)

**File:** [`mlops-deploy-infra-2-kubernetes-deployment.yml`](./mlops-deploy-infra-2-kubernetes-deployment.yml)

### Serverless Function
> Lambda/Cloud Functions for event-driven ML
>
> ![Serverless](https://img.shields.io/badge/AWS%20Lambda-FF9900?logo=awslambda&logoColor=white) ![Event](https://img.shields.io/badge/Trigger-Event--Driven-blue) ![Cloud](https://img.shields.io/badge/Type-Serverless-orange)

**File:** [`mlops-deploy-infra-3-serverless-function.py`](./mlops-deploy-infra-3-serverless-function.py)


---

## 📊 Observability

*Understanding model behavior in production*

### Comprehensive Monitoring
> Performance, model, and business metrics
>
> ![Monitoring](https://img.shields.io/badge/Type-Comprehensive-informational) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white) ![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)

**File:** [`mlops-monitor-observe-1-comprehensive-monitoring.py`](./mlops-monitor-observe-1-comprehensive-monitoring.py)

### Distributed Tracing
> Distributed tracing and centralized logging
>
> ![Tracing](https://img.shields.io/badge/Type-Distributed-informational) ![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-000000?logoColor=white) ![Logs](https://img.shields.io/badge/Feature-Centralized-blue)

**File:** [`mlops-monitor-observe-2-distributed-tracing.py`](./mlops-monitor-observe-2-distributed-tracing.py)

### Alert Configuration
> Proactive incident detection and response
>
> ![Alerts](https://img.shields.io/badge/Type-Alerting-informational) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white) ![PagerDuty](https://img.shields.io/badge/PagerDuty-06AC38?logo=pagerduty&logoColor=white)

**File:** [`mlops-monitor-observe-3-alert-configuration.yml`](./mlops-monitor-observe-3-alert-configuration.yml)


---

## 🔍 Drift Detection

*Identifying when models need attention*

### Data Drift Detection
> Input distribution changes over time
>
> ![Drift](https://img.shields.io/badge/Type-Data%20Drift-critical) ![KS](https://img.shields.io/badge/Test-KS%20%7C%20PSI-blue) ![Distribution](https://img.shields.io/badge/Track-Distribution-orange)

**File:** [`mlops-monitor-drift-1-data-drift-detection.py`](./mlops-monitor-drift-1-data-drift-detection.py)

### Concept Drift Detection
> Feature-target relationship evolution
>
> ![Drift](https://img.shields.io/badge/Type-Concept%20Drift-critical) ![Relationship](https://img.shields.io/badge/Track-Feature--Target-blue) ![Statistical](https://img.shields.io/badge/Method-Statistical-orange)

**File:** [`mlops-monitor-drift-2-concept-drift-detection.py`](./mlops-monitor-drift-2-concept-drift-detection.py)

### Performance Monitoring
> Model accuracy degradation
>
> ![Drift](https://img.shields.io/badge/Type-Performance-critical) ![Accuracy](https://img.shields.io/badge/Track-Accuracy-blue) ![Degradation](https://img.shields.io/badge/Detect-Degradation-red)

**File:** [`mlops-monitor-drift-3-performance-monitoring.py`](./mlops-monitor-drift-3-performance-monitoring.py)


---

## 🔄 Retraining

*Keeping models fresh and performant*

### Scheduled Retraining Pipeline
> Regular updates on fixed calendar
>
> ![Retrain](https://img.shields.io/badge/Type-Scheduled-9cf) ![Cron](https://img.shields.io/badge/Trigger-Cron-blue) ![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?logo=apacheairflow&logoColor=white)

**File:** [`mlops-maintain-retrain-1-scheduled-retraining-pipeline.py`](./mlops-maintain-retrain-1-scheduled-retraining-pipeline.py)

### Trigger-based Retraining
> Retrain when conditions are met
>
> ![Retrain](https://img.shields.io/badge/Type-Trigger--based-9cf) ![Event](https://img.shields.io/badge/Mode-Event--Driven-blue) ![Drift](https://img.shields.io/badge/Trigger-Drift%20%7C%20Performance-orange)

**File:** [`mlops-maintain-retrain-2-trigger-based-retraining.py`](./mlops-maintain-retrain-2-trigger-based-retraining.py)

### Online Learning System
> Continuous model updates
>
> ![Retrain](https://img.shields.io/badge/Type-Online%20Learning-9cf) ![Continuous](https://img.shields.io/badge/Mode-Continuous-blue) ![Incremental](https://img.shields.io/badge/Update-Incremental-green)

**File:** [`mlops-maintain-retrain-3-online-learning-system.py`](./mlops-maintain-retrain-3-online-learning-system.py)


---

## 📦 Versioning

*Tracking and managing model artifacts and experiments*

### Model Registry with MLflow
> Centralized repository for model artifacts
>
> ![Registry](https://img.shields.io/badge/Type-Model%20Registry-blueviolet) ![MLflow](https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white) ![Artifacts](https://img.shields.io/badge/Track-Artifacts-blue)

**File:** [`mlops-maintain-version-1-model-registry-with-mlflow.py`](./mlops-maintain-version-1-model-registry-with-mlflow.py)

### Experiment Tracking System
> Recording parameters, metrics, and artifacts
>
> ![Tracking](https://img.shields.io/badge/Type-Experiment%20Tracking-blueviolet) ![MLflow](https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white) ![Params](https://img.shields.io/badge/Log-Params%20%7C%20Metrics-blue)

**File:** [`mlops-maintain-version-2-experiment-tracking-system.py`](./mlops-maintain-version-2-experiment-tracking-system.py)

### Data and Model Lineage
> Data and model provenance
>
> ![Lineage](https://img.shields.io/badge/Type-Lineage-blueviolet) ![Provenance](https://img.shields.io/badge/Track-Provenance-blue) ![DAG](https://img.shields.io/badge/Graph-DAG-orange)

**File:** [`mlops-maintain-version-3-data-and-model-lineage.py`](./mlops-maintain-version-3-data-and-model-lineage.py)


---

## 📋 Compliance

*Meeting regulatory and ethical requirements*

### Audit Trail System
> Comprehensive logging for accountability
>
> ![Compliance](https://img.shields.io/badge/Type-Audit%20Trail-red) ![Logging](https://img.shields.io/badge/Feature-Immutable%20Logs-blue) ![Accountability](https://img.shields.io/badge/Purpose-Accountability-orange)

**File:** [`mlops-govern-comply-1-audit-trail-system.py`](./mlops-govern-comply-1-audit-trail-system.py)

### Data Privacy Protection
> GDPR, CCPA compliance and PII protection
>
> ![Compliance](https://img.shields.io/badge/Type-Privacy-red) ![GDPR](https://img.shields.io/badge/GDPR-Compliant-blue) ![CCPA](https://img.shields.io/badge/CCPA-Compliant-blue) ![PII](https://img.shields.io/badge/Protect-PII-orange)

**File:** [`mlops-govern-comply-2-data-privacy-protection.py`](./mlops-govern-comply-2-data-privacy-protection.py)

### Bias Detection and Mitigation
> Fairness metrics and mitigation strategies
>
> ![Compliance](https://img.shields.io/badge/Type-Fairness-red) ![Bias](https://img.shields.io/badge/Detect-Bias-blue) ![Fairness](https://img.shields.io/badge/Ensure-Fairness-green)

**File:** [`mlops-govern-comply-3-bias-detection-and-mitigation.py`](./mlops-govern-comply-3-bias-detection-and-mitigation.py)


---

## 💡 Explainability

*Making models interpretable and trustworthy*

### SHAP Explanations
> Unified measure of feature importance
>
> ![XAI](https://img.shields.io/badge/Type-SHAP-purple) ![Global](https://img.shields.io/badge/Scope-Global%20%7C%20Local-blue) ![Shapley](https://img.shields.io/badge/Method-Shapley%20Values-orange)

**File:** [`mlops-govern-explain-1-shap-explanations.py`](./mlops-govern-explain-1-shap-explanations.py)

### LIME Explanations
> Local interpretable model explanations
>
> ![XAI](https://img.shields.io/badge/Type-LIME-purple) ![Local](https://img.shields.io/badge/Scope-Local-blue) ![Surrogate](https://img.shields.io/badge/Method-Surrogate%20Model-orange)

**File:** [`mlops-govern-explain-2-lime-explanations.py`](./mlops-govern-explain-2-lime-explanations.py)

### Counterfactual Explanations
> What-if explanations for predictions
>
> ![XAI](https://img.shields.io/badge/Type-Counterfactual-purple) ![What--If](https://img.shields.io/badge/Mode-What--If-blue) ![Actionable](https://img.shields.io/badge/Output-Actionable-green)

**File:** [`mlops-govern-explain-3-counterfactual-explanations.py`](./mlops-govern-explain-3-counterfactual-explanations.py)


---
