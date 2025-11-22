import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

class DistributionAnalyzer:
    def __init__(self, data):
        self.data = data
        self.numerical_cols = data.select_dtypes(include=[np.number]).columns
        
    def analyze_distributions(self):
        """Complete distribution analysis for all numerical features"""
        distribution_stats = {}
        
        for col in self.numerical_cols:
            values = self.data[col].dropna()
            
            stats_dict = {
                # Central tendency
                'mean': values.mean(),
                'median': values.median(),
                'mode': values.mode()[0] if len(values.mode()) > 0 else None,
                
                # Dispersion
                'std': values.std(),
                'var': values.var(),
                'iqr': values.quantile(0.75) - values.quantile(0.25),
                
                # Shape
                'skewness': values.skew(),
                'kurtosis': values.kurtosis(),
                
                # Outliers
                'outliers': self.detect_outliers(values),
                
                # Normality test
                'shapiro_pvalue': stats.shapiro(values)[1] if len(values) < 5000 else None,
                'ks_pvalue': stats.kstest(values, 'norm')[1]
            }
            
            distribution_stats[col] = stats_dict
        
        return distribution_stats
    
    def detect_outliers(self, series, method='iqr'):
        """Multiple outlier detection methods"""
        if method == 'iqr':
            Q1, Q3 = series.quantile([0.25, 0.75])
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers = series[(series < lower) | (series > upper)]
            
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(series))
            outliers = series[z_scores > 3]
            
        elif method == 'isolation_forest':
            from sklearn.ensemble import IsolationForest
            iso = IsolationForest(contamination=0.1)
            preds = iso.fit_predict(series.values.reshape(-1, 1))
            outliers = series[preds == -1]
        
        return {
            'count': len(outliers),
            'percentage': len(outliers) / len(series) * 100,
            'values': outliers.tolist()[:10]  # First 10 outliers
        }