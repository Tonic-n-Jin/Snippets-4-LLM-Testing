class PerformanceMonitor:
    def __init__(self, baseline_metrics):
        self.baseline = baseline_metrics
        self.degradation_threshold = 0.05

    def monitor_performance(self, current_metrics):
        """Track performance degradation"""
        degradation = {}
        alerts = []

        for metric, baseline_value in self.baseline.items():
            current_value = current_metrics.get(metric)

            if metric in ['accuracy', 'precision', 'recall', 'f1']:
                # Higher is better
                degradation[metric] = (baseline_value - current_value) / baseline_value
                if degradation[metric] > self.degradation_threshold:
                    alerts.append(f"{metric} degraded by {degradation[metric]:.2%}")

            elif metric in ['mse', 'mae', 'error_rate']:
                # Lower is better
                degradation[metric] = (current_value - baseline_value) / baseline_value
                if degradation[metric] > self.degradation_threshold:
                    alerts.append(f"{metric} increased by {degradation[metric]:.2%}")

        return {
            'degradation': degradation,
            'alerts': alerts,
            'requires_retraining': len(alerts) > 0
        }