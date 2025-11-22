class OnlineLearning:
    def __init__(self, model, learning_rate=0.01):
        self.model = model  # Must support partial_fit
        self.learning_rate = learning_rate
        self.buffer = []
        self.buffer_size = 1000

    def update(self, X, y):
        """Incremental model update"""
        self.buffer.append((X, y))

        if len(self.buffer) >= self.buffer_size:
            # Batch update for efficiency
            X_batch = np.vstack([x for x, _ in self.buffer])
            y_batch = np.array([y for _, y in self.buffer])

            # Incremental training
            self.model.partial_fit(
                X_batch, y_batch,
                classes=np.unique(y_batch)
            )

            # Clear buffer
            self.buffer = []

            # Update model version
            self.version += 0.1

    def adapt_to_drift(self, drift_detector):
        """Adaptive learning rate based on drift"""
        drift_level = drift_detector.get_drift_magnitude()

        if drift_level > 0.5:
            # High drift: increase learning rate
            self.learning_rate = min(0.1, self.learning_rate * 2)
        elif drift_level < 0.1:
            # Low drift: decrease learning rate
            self.learning_rate = max(0.001, self.learning_rate * 0.5)