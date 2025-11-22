import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

# This custom transformer can be placed directly into a scikit-learn pipeline.
class TransactionFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Creates new features from raw transaction data:
    1. Temporal Features: Extracts signals from timestamps.
    2. Rolling Aggregates: Creates time-windowed aggregates per user.
    """
    def __init__(self, window_size='7D'):
        self.window_size = window_size
        
    def fit(self, X, y=None):
        # This transformer is stateless, so fit does nothing
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transforms the input DataFrame by adding new features."""
        df = X.copy()
        
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()

        # 1. Temporal Features (Domain Signals)
        df['tx_day_of_week'] = df.index.dayofweek
        df['tx_hour_of_day'] = df.index.hour
        df['tx_is_weekend'] = df['tx_day_of_week'].isin([5, 6]).astype(int)

        # 2. Rolling Aggregates (Time Windows)
        # We group by user, then apply a rolling window.
        rolling_groups = df.groupby('user_id')['amount']
        
        # Calculate rolling mean and sum
        df['user_avg_spend_window'] = rolling_groups.rolling(self.window_size).mean().reset_index(0, drop=True)
        df['user_total_spend_window'] = rolling_groups.rolling(self.window_size).sum().reset_index(0, drop=True)
        
        # Handle NaNs created by the rolling window (e.g., first few days)
        df.fillna(0, inplace=True)
        
        return df.reset_index()

# --- Example Usage ---
data = pd.DataFrame({
    'timestamp': pd.to_datetime(['2025-11-10 08:00', '2025-11-12 09:00', '2025-11-15 10:00', '2025-11-17 11:00']),
    'user_id': ['u1', 'u1', 'u2', 'u1'],
    'amount': [100, 50, 200, 25]
})

extractor = TransactionFeatureExtractor(window_size='3D')
features = extractor.transform(data)
print(features)
