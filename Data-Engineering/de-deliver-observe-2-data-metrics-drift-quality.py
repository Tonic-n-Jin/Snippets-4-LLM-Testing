import pandas as pd
import pandera as pa
from pandera.errors import SchemaErrors
import logging

# (Using MockMetricsClient from the previous example)
metrics_client = MockMetricsClient()

class DataProfiler:
    """
    Fits on a 'reference' dataset and then profiles new data
    to check for quality issues and distribution drift.
    """
    def __init__(self, client: MockMetricsClient):
        self.client = client
        self.reference_schema = None
        self.reference_stats = {}

    def fit(self, reference_df: pd.DataFrame):
        """Fit the profiler on a 'golden' reference dataset."""
        logging.info("Fitting profiler on reference data...")
        # 1. Infer a schema for quality checks
        self.reference_schema = pa.infer_schema(reference_df)
        
        # 2. Calculate statistics for drift detection
        self.reference_stats['age_mean'] = reference_df['age'].mean()
        self.reference_stats['total_records'] = len(reference_df)
        logging.info(f"Reference stats calculated: {self.reference_stats}")

    def profile(self, new_data: pd.DataFrame, data_stream_name: str):
        """Profile a new batch of data against the reference set."""
        if self.reference_schema is None:
            raise RuntimeError("Profiler has not been.fit() yet.")
            
        tags = {'stream': data_stream_name}
        num_records = len(new_data)
        
        # 1. Data Volume Trend
        volume_delta = num_records - self.reference_stats['total_records']
        self.client.gauge(f"data.volume.records", num_records, tags=tags)
        self.client.gauge(f"data.volume.delta_from_ref", volume_delta, tags=tags)

        # 2. Data Quality Score
        try:
            self.reference_schema.validate(new_data, lazy=True)
            quality_score = 1.0
        except SchemaErrors as err:
            num_failures = len(err.failure_cases)
            quality_score = (num_records - num_failures) / num_records
        
        self.client.gauge(f"data.quality.score", quality_score, tags=tags)

        # 3. Data Drift Detection (Mean)
        current_age_mean = new_data['age'].mean()
        mean_drift = abs(current_age_mean - self.reference_stats['age_mean'])
        self.client.gauge(f"data.drift.age_mean_delta", mean_drift, tags=tags)

# --- Example Usage ---
# 1. "Golden" data to establish a baseline
reference_data = pd.DataFrame({
    'user_id': [f"u-{i}" for i in range(100)],
    'age': [30] * 100, # Mean is 30
    'status': ['active'] * 100
})

# 2. New incoming batch with issues
new_data = pd.DataFrame({
    'user_id': [f"u-{i}" for i in range(110)], # Volume drift
    'age': [35] * 110, # Mean drift
    'status': ['active'] * 109 + [None] # Quality issue
})

# 3. Fit and Profile
profiler = DataProfiler(client=metrics_client)
profiler.fit(reference_data)
profiler.profile(new_data, data_stream_name="user_signups")
