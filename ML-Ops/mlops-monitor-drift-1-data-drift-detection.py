from scipy import stats
import numpy as np

class DriftDetector:
def **init**(self, reference_data):
self.reference_data = reference_data
self.threshold = 0.05 # p-value threshold

    def detect_feature_drift(self, current_data, feature):
        """Detect if feature distribution has changed"""
        reference = self.reference_data[feature]
        current = current_data[feature]

        # Kolmogorov-Smirnov test for distribution shift
        ks_statistic, p_value = stats.ks_2samp(reference, current)

        if p_value < self.threshold:
            return True, p_value
        return False, p_value

    def calculate_psi(self, expected, actual, bins=10):
        """Population Stability Index"""
        def psi_bucket(e, a):
            if a == 0:
                a = 0.0001
            if e == 0:
                e = 0.0001
            return (e - a) * np.log(e / a)

        breakpoints = np.percentile(expected, np.arange(0, 101, 100/bins))
        expected_counts = np.histogram(expected, breakpoints)[0]
        expected_percents = expected_counts / len(expected)

        actual_counts = np.histogram(actual, breakpoints)[0]
        actual_percents = actual_counts / len(actual)

        psi = sum(psi_bucket(e, a) for e, a in zip(expected_percents, actual_percents))
        return psi