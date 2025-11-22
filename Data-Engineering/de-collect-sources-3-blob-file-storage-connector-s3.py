import s3fs
import pandas as pd
import pyarrow.parquet as pq
import logging
from typing import Generator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FileStorageConnector:
    """
    Handles reading data from blob storage like S3.
    Assumes credentials are set in the environment (e.g., AWS_ACCESS_KEY_ID)
    """
    
    def __init__(self, anon: bool = False):
        """Initializes the S3 file system client."""
        try:
            # anon=False will use default credential chain (env vars, ~/.aws/...)
            self.s3 = s3fs.S3FileSystem(anon=anon)
            logging.info("S3FileSystem client initialized.")
        except Exception as e:
            logging.error(f"Failed to initialize S3FileSystem: {e}")
            raise
            
    def read_parquet_dataset(self, s3_path: str) -> pd.DataFrame:
        """
        Reads a single Parquet file or a partitioned dataset from S3.
        s3_path should be the root directory of the dataset (e.g., 's3://my-bucket/data/')
        """
        logging.info(f"Reading Parquet dataset from {s3_path}...")
        try:
            # S3FS and pandas.read_parquet work together seamlessly
            df = pd.read_parquet(s3_path, filesystem=self.s3)
            logging.info(f"Successfully read {len(df)} records.")
            return df
        except Exception as e:
            logging.error(f"Failed to read Parquet from {s3_path}: {e}")
            raise

    def stream_log_file(self, s3_path: str) -> Generator[str, None, None]:
        """
        Reads a large log file (e.g., .txt, .log, .csv) from S3 line by line.
        This is memory-efficient for very large files.
        """
        logging.info(f"Streaming file {s3_path}...")
        try:
            with self.s3.open(s3_path, 'r', encoding='utf-8') as f:
                for line in f:
                    yield line.strip()
            logging.info(f"Finished streaming {s3_path}.")
        except FileNotFoundError:
            logging.error(f"File not found: {s3_path}")
            raise
        except Exception as e:
            logging.error(f"Failed to stream file {s3_path}: {e}")
            raise
