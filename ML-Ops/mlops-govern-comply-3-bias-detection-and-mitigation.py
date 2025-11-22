from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd

class FairnessEvaluator:
    def __init__(self, sensitive_attribute):
        self.sensitive_attribute = sensitive_attribute

    def calculate_demographic_parity(self, y_pred, sensitive_features):
        """Measure if positive prediction rate is equal across groups"""
        groups = sensitive_features[self.sensitive_attribute].unique()

        positive_rates = {}
        for group in groups:
            mask = sensitive_features[self.sensitive_attribute] == group
            positive_rates[group] = y_pred[mask].mean()

        # Calculate disparate impact ratio
        min_rate = min(positive_rates.values())
        max_rate = max(positive_rates.values())
        disparate_impact = min_rate / max_rate if max_rate > 0 else 0

        return {
            'positive_rates': positive_rates,
            'disparate_impact': disparate_impact,
            'passes_80_percent_rule': disparate_impact >= 0.8
        }

    def calculate_equalized_odds(self, y_true, y_pred, sensitive_features):
        """Measure if TPR and FPR are equal across groups"""
        groups = sensitive_features[self.sensitive_attribute].unique()

        metrics = {}
        for group in groups:
            mask = sensitive_features[self.sensitive_attribute] == group

            cm = confusion_matrix(y_true[mask], y_pred[mask])
            tn, fp, fn, tp = cm.ravel()

            tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

            metrics[group] = {'tpr': tpr, 'fpr': fpr}

        # Calculate max difference
        tpr_diff = max([m['tpr'] for m in metrics.values()]) - \
                  min([m['tpr'] for m in metrics.values()])
        fpr_diff = max([m['fpr'] for m in metrics.values()]) - \
                  min([m['fpr'] for m in metrics.values()])

        return {
            'group_metrics': metrics,
            'tpr_difference': tpr_diff,
            'fpr_difference': fpr_diff,
            'is_fair': tpr_diff < 0.1 and fpr_diff < 0.1
        }

    def mitigate_bias_reweighting(self, X, y, sensitive_features):
        """Apply reweighting to training data to reduce bias"""
        weights = np.ones(len(y))

        groups = sensitive_features[self.sensitive_attribute].unique()

        for group in groups:
            for label in [0, 1]:
                mask = (sensitive_features[self.sensitive_attribute] == group) & (y == label)

                # Expected frequency
                expected_freq = len(y[y == label]) / len(y) * len(sensitive_features[sensitive_features[self.sensitive_attribute] == group]) / len(sensitive_features)

                # Actual frequency
                actual_freq = mask.sum()

                # Reweight
                if actual_freq > 0:
                    weights[mask] = expected_freq / actual_freq

        return weights