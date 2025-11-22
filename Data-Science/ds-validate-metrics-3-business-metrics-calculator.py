class BusinessMetricsEvaluator:
    def __init__(self, y_true, y_pred, y_proba=None, business_context=None):
        self.y_true = y_true
        self.y_pred = y_pred
        self.y_proba = y_proba
        self.context = business_context or {}

    def calculate_revenue_impact(self):
        """Calculate revenue impact of predictions"""
        # For fraud detection example
        avg_fraud_amount = self.context.get('avg_fraud_amount', 1000)
        investigation_cost = self.context.get('investigation_cost', 50)

        tp = ((self.y_pred == 1) & (self.y_true == 1)).sum()
        fp = ((self.y_pred == 1) & (self.y_true == 0)).sum()
        fn = ((self.y_pred == 0) & (self.y_true == 1)).sum()

        # Value saved by catching fraud
        value_saved = tp * avg_fraud_amount

        # Cost of false positives (unnecessary investigations)
        false_positive_cost = fp * investigation_cost

        # Cost of false negatives (missed fraud)
        false_negative_cost = fn * avg_fraud_amount

        net_value = value_saved - false_positive_cost - false_negative_cost

        return {
            'value_saved': value_saved,
            'false_positive_cost': false_positive_cost,
            'false_negative_cost': false_negative_cost,
            'net_value': net_value,
            'roi': net_value / (tp + fp) if (tp + fp) > 0 else 0
        }

    def optimal_threshold_for_business(self):
        """Find threshold that maximizes business value"""
        if self.y_proba is None:
            return None

        thresholds = np.linspace(0, 1, 100)
        values = []

        for threshold in thresholds:
            y_pred_threshold = (self.y_proba >= threshold).astype(int)
            evaluator = BusinessMetricsEvaluator(
                self.y_true, y_pred_threshold,
                business_context=self.context
            )
            impact = evaluator.calculate_revenue_impact()
            values.append(impact['net_value'])

        optimal_idx = np.argmax(values)
        optimal_threshold = thresholds[optimal_idx]
        max_value = values[optimal_idx]

        return {
            'optimal_threshold': optimal_threshold,
            'max_business_value': max_value,
            'default_threshold_value': values[50]  # 0.5 threshold
        }