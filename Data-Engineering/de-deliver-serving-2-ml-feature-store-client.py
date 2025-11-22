import pandas as pd
import logging
from redis import Redis # Example for online store
from pyarrow.parquet import ParquetDataset # Example for offline store

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FeatureStoreClient:
    """
    Provides consistent features for training (offline) and inference (online).
    - Offline: Reads historical data from a data lake (Parquet).
    - Online: Reads low-latency features from a KV store (Redis).
    """
    def __init__(self, offline_path: str, online_host: str = 'localhost'):
        self.offline_path = offline_path
        try:
            self.online_client = Redis(host=online_host, port=6379, db=0, decode_responses=True)
            self.online_client.ping()
            logging.info("Connected to Online Feature Store (Redis).")
        except Exception as e:
            logging.error(f"Failed to connect to Redis: {e}")
            self.online_client = None

    def get_historical_features(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Serves a large batch of features for model training.
        Reads from the offline Parquet dataset (e.g., S3, HDFS).
        """
        logging.info(f"Fetching historical features from {self.offline_path}")
        try:
            dataset = ParquetDataset(
                self.offline_path,
                filters=[('date', '>=', start_date), ('date', '<=', end_date)]
            )
            df = dataset.read().to_pandas()
            logging.info(f"Loaded {len(df)} records for training.")
            return df
        except Exception as e:
            logging.error(f"Failed to read historical features: {e}")
            raise

    def get_online_features(self, user_ids: list[str]) -> list[dict]:
        """
        Serves low-latency feature vectors for real-time inference.
        Reads from the online key-value store.
        """
        if not self.online_client:
            raise RuntimeError("Online client not connected.")
            
        logging.info(f"Fetching online features for {len(user_ids)} users.")
        pipeline = self.online_client.pipeline()
        for user_id in user_ids:
            # Assumes features are stored as a JSON string or Hash
            pipeline.hgetall(f"user_features:{user_id}")
            
        results = pipeline.execute()
        
        # Convert numeric strings back to floats/ints
        final_features = []
        for res in results:
            final_features.append({
                k: float(v) if v.replace('.', '', 1).isdigit() else v 
                for k, v in res.items()
            })
        return final_features
