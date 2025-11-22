# ML Ops Code Snippets

This directory contains code examples for ML Ops.

## Table of Contents

- [Model Serving](#model-serving)
- [Infrastructure](#infrastructure)
- [Observability](#observability)
- [Drift Detection](#drift-detection)
- [Retraining](#retraining)
- [Versioning](#versioning)
- [Compliance](#compliance)
- [Explainability](#explainability)

---

## Model Serving

*Monitoring, alerting, and understanding data systems*

### Batch Prediction Script

Scheduled predictions for large datasets offline

**File:** [`mlops-deploy-serving-1-batch-prediction-script.py`](./mlops-deploy-serving-1-batch-prediction-script.py)

### Real-time API with FastAPI

Low-latency predictions via REST/gRPC endpoints

**File:** [`mlops-deploy-serving-2-real-time-api-with-fastapi.py`](./mlops-deploy-serving-2-real-time-api-with-fastapi.py)

### Stream Processing with Faust

Continuous predictions on event streams

**File:** [`mlops-deploy-serving-3-stream-processing-with-faust.py`](./mlops-deploy-serving-3-stream-processing-with-faust.py)


---

## Infrastructure

*Scalable foundations for ML workloads*

### Docker Configuration

Docker for reproducible environments

**File:** [`DockerFile`](./Dockerfile)

### Kubernetes Deployment

Kubernetes for scaling and management

**File:** [`mlops-deploy-infra-2-kubernetes-deployment.yml`](./mlops-deploy-infra-2-kubernetes-deployment.yml)

### Serverless Function

Lambda/Cloud Functions for event-driven ML

**File:** [`mlops-deploy-infra-3-serverless-function.py`](./mlops-deploy-infra-3-serverless-function.py)


---

## Observability

*Understanding model behavior in production*

### Comprehensive Monitoring

Performance, model, and business metrics

**File:** [`mlops-monitor-observe-1-comprehensive-monitoring.py`](./mlops-monitor-observe-1-comprehensive-monitoring.py)

### Distributed Tracing

Distributed tracing and centralized logging

**File:** [`mlops-monitor-observe-2-distributed-tracing.py`](./mlops-monitor-observe-2-distributed-tracing.py)

### Alert Configuration

Proactive incident detection and response

**File:** [`mlops-monitor-observe-3-alert-configuration.yml`](./mlops-monitor-observe-3-alert-configuration.yml)


---

## Drift Detection

*Identifying when models need attention*

### Data Drift Detection

Input distribution changes over time

**File:** [`mlops-monitor-drift-1-data-drift-detection.py`](./mlops-monitor-drift-1-data-drift-detection.py)

### Concept Drift Detection

Feature-target relationship evolution

**File:** [`mlops-monitor-drift-2-concept-drift-detection.py`](./mlops-monitor-drift-2-concept-drift-detection.py)

### Performance Monitoring

Model accuracy degradation

**File:** [`mlops-monitor-drift-3-performance-monitoring.py`](./mlops-monitor-drift-3-performance-monitoring.py)


---

## Retraining

*Keeping models fresh and performant*

### Scheduled Retraining Pipeline

Regular updates on fixed calendar

**File:** [`mlops-maintain-retrain-1-scheduled-retraining-pipeline.py`](./mlops-maintain-retrain-1-scheduled-retraining-pipeline.py)

### Trigger-based Retraining

Retrain when conditions are met

**File:** [`mlops-maintain-retrain-2-trigger-based-retraining.py`](./mlops-maintain-retrain-2-trigger-based-retraining.py)

### Online Learning System

Continuous model updates

**File:** [`mlops-maintain-retrain-3-online-learning-system.py`](./mlops-maintain-retrain-3-online-learning-system.py)


---

## Versioning

*Tracking and managing model artifacts and experiments*

### Model Registry with MLflow

Centralized repository for model artifacts

**File:** [`mlops-maintain-version-1-model-registry-with-mlflow.py`](./mlops-maintain-version-1-model-registry-with-mlflow.py)

### Experiment Tracking System

Recording parameters, metrics, and artifacts

**File:** [`mlops-maintain-version-2-experiment-tracking-system.py`](./mlops-maintain-version-2-experiment-tracking-system.py)

### Data and Model Lineage

Data and model provenance

**File:** [`mlops-maintain-version-3-data-and-model-lineage.py`](./mlops-maintain-version-3-data-and-model-lineage.py)


---

## Compliance

*Meeting regulatory and ethical requirements*

### Audit Trail System

Comprehensive logging for accountability

**File:** [`mlops-govern-comply-1-audit-trail-system.py`](./mlops-govern-comply-1-audit-trail-system.py)

### Data Privacy Protection

GDPR, CCPA compliance and PII protection

**File:** [`mlops-govern-comply-2-data-privacy-protection.py`](./mlops-govern-comply-2-data-privacy-protection.py)

### Bias Detection and Mitigation

Fairness metrics and mitigation strategies

**File:** [`mlops-govern-comply-3-bias-detection-and-mitigation.py`](./mlops-govern-comply-3-bias-detection-and-mitigation.py)


---

## Explainability

*Making models interpretable and trustworthy*

### SHAP Explanations

Unified measure of feature importance

**File:** [`mlops-govern-explain-1-shap-explanations.py`](./mlops-govern-explain-1-shap-explanations.py)

### LIME Explanations

Local interpretable model explanations

**File:** [`mlops-govern-explain-2-lime-explanations.py`](./mlops-govern-explain-2-lime-explanations.py)

### Counterfactual Explanations

What-if explanations for predictions

**File:** [`mlops-govern-explain-3-counterfactual-explanations.py`](./mlops-govern-explain-3-counterfactual-explanations.py)


---
