class TriggerBasedRetraining:
    def __init__(self, model_pipeline):
        self.pipeline = model_pipeline
        self.triggers = {
            'time': 30,  # days
            'accuracy_drop': 0.05,
            'drift_threshold': 0.2,
            'data_volume': 10000
        }

    def should_retrain(self):
        """Check multiple trigger conditions"""
        conditions = {
            'time_based': self.days_since_last_training() > self.triggers['time'],
            'performance': self.accuracy_drop() > self.triggers['accuracy_drop'],
            'drift': self.drift_score() > self.triggers['drift_threshold'],
            'data': self.new_data_count() > self.triggers['data_volume']
        }

        triggered = [k for k, v in conditions.items() if v]

        if triggered:
            self.log_trigger(triggered)
            return True, triggered
        return False, []

    def retrain(self):
        """Execute retraining workflow"""
        # Get latest data
        training_data = self.pipeline.get_training_data()

        # Train challenger model
        challenger = self.pipeline.train(training_data)

        # A/B test against champion
        if self.validate_challenger(challenger):
            # Gradual rollout
            self.canary_deployment(challenger, percentage=0.1)
            self.monitor_canary(duration_hours=24)

            if self.canary_successful():
                self.promote_to_production(challenger)
        else:
            self.alert("Challenger model failed validation")