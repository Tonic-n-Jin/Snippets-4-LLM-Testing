class ModelMonitor:
    def __init__(self):
        self.metrics = {
            # Performance metrics
            'latency_ms': [],
            'throughput_rps': [],
            'error_rate': [],

            # Model metrics
            'prediction_distribution': [],
            'confidence_scores': [],
            'feature_distributions': {},

            # Business metrics
            'conversion_rate': [],
            'revenue_impact': [],
            'user_satisfaction': []
        }

    def log_prediction(self, request, response, latency):
        """Log each prediction for monitoring"""
        self.metrics['latency_ms'].append(latency)
        self.metrics['prediction_distribution'].append(response.prediction)
        self.metrics['confidence_scores'].append(response.confidence)

        # Check for anomalies
        self.detect_anomalies()

    def detect_anomalies(self):
        """Detect drift and anomalies"""
        if self.detect_prediction_drift():
            self.alert("Prediction distribution drift detected")

        if self.detect_latency_spike():
            self.alert("Latency spike detected")