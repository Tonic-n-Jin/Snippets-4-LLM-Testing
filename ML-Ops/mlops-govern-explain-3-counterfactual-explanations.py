import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

class CounterfactualExplainer:
    def __init__(self, model, X_train, feature_names):
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names

        # Fit nearest neighbors for finding similar instances
        self.nn = NearestNeighbors(n_neighbors=100)
        self.nn.fit(X_train)

    def generate_counterfactual(self, instance, desired_class,
                               max_changes=3, categorical_features=None):
        """Generate counterfactual explanation"""
        if categorical_features is None:
            categorical_features = []

        # Get current prediction
        current_pred = self.model.predict(instance)[0]

        if current_pred == desired_class:
            return {
                'message': 'Instance already in desired class',
                'counterfactual': None
            }

        # Find similar instances in desired class
        distances, indices = self.nn.kneighbors(instance)

        for idx in indices[0]:
            candidate = self.X_train.iloc[[idx]]
            if self.model.predict(candidate)[0] == desired_class:
                # Calculate minimal changes needed
                changes = self._calculate_minimal_changes(
                    instance,
                    candidate,
                    max_changes,
                    categorical_features
                )

                if len(changes) <= max_changes:
                    return {
                        'original_prediction': current_pred,
                        'counterfactual_prediction': desired_class,
                        'changes': changes,
                        'counterfactual_instance': candidate
                    }

        # If no suitable counterfactual found, use optimization
        return self._optimize_counterfactual(
            instance,
            desired_class,
            max_changes
        )

    def _calculate_minimal_changes(self, original, target,
                                   max_changes, categorical_features):
        """Calculate minimal feature changes needed"""
        changes = []

        for feature in self.feature_names:
            orig_value = original[feature].values[0]
            target_value = target[feature].values[0]

            if orig_value != target_value:
                if feature in categorical_features:
                    change_description = f"{feature}: {orig_value} → {target_value}"
                else:
                    diff = target_value - orig_value
                    change_description = f"{feature}: {orig_value:.2f} → {target_value:.2f} ({diff:+.2f})"

                changes.append({
                    'feature': feature,
                    'original': orig_value,
                    'counterfactual': target_value,
                    'description': change_description
                })

                if len(changes) >= max_changes:
                    break

        return changes

    def _optimize_counterfactual(self, instance, desired_class, max_changes):
        """Use gradient-based optimization to find counterfactual"""
        # Simplified optimization approach
        # In practice, would use libraries like DiCE or Alibi

        counterfactual = instance.copy()

        # Iteratively modify features
        for _ in range(100):
            pred = self.model.predict_proba(counterfactual)[0][desired_class]

            if pred > 0.5:
                changes = self._calculate_minimal_changes(
                    instance,
                    counterfactual,
                    max_changes,
                    []
                )

                return {
                    'original_prediction': self.model.predict(instance)[0],
                    'counterfactual_prediction': desired_class,
                    'changes': changes,
                    'counterfactual_instance': counterfactual,
                    'confidence': pred
                }

        return {'message': 'Could not find suitable counterfactual'}