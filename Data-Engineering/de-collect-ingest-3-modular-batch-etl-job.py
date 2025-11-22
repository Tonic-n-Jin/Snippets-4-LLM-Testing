import pandas as pd
import logging
import argparse
import s3fs
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from datetime import date

# ---
# This example shows a modular ETL job, runnable via a scheduler (e.g., Airflow).
# It follows the E-T-L pattern clearly and is built for orchestration.
# It decouples the E, T, and L steps for testability.
# ---

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DailyUserETL:
    def __init__(self, source_db_conn_str: str, dest_s3_bucket: str):
        """
        Initializes the ETL job with source and destination.
        
        :param source_db_conn_str: SQLAlchemy connection string for the source DB
        :param dest_s3_bucket: S3 bucket name (e.g., 'my-data-lake')
        """
        try:
            self.source_engine = create_engine(source_db_conn_str)
            self.s3fs = s3fs.S3FileSystem()
            self.dest_bucket = dest_s3_bucket
            logging.info("ETL Job initialized.")
        except Exception as e:
            logging.error(f"Failed to initialize ETL job: {e}")
            raise

    def extract(self, execution_date: date) -> pd.DataFrame:
        """Pulls raw data from the source operational database."""
        query = f"""
        SELECT 
            u.id as user_id, 
            u.email, 
            u.created_at, 
            o.id as order_id, 
            o.order_total, 
            o.created_at as order_timestamp
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE DATE(u.created_at) = '{execution_date.isoformat()}'
           OR DATE(o.created_at) = '{execution_date.isoformat()}'
        """
        logging.info(f"Extracting data for date: {execution_date}")
        with self.source_engine.connect() as conn:
            data = pd.read_sql(query, conn)
        logging.info(f"Extracted {len(data)} raw records.")
        return data

    def transform(self, raw_data: pd.DataFrame, execution_date: date) -> pd.DataFrame:
        """Applies business logic and cleaning to the raw data."""
        if raw_data.empty:
            logging.warning("No data to transform.")
            return pd.DataFrame()
            
        logging.info("Starting transformation...")
        
        # 1. Handle nulls
        raw_data['order_total'] = raw_data['order_total'].fillna(0)
        
        # 2. Aggregate
        daily_summary = raw_data.groupby('user_id').agg(
            email=('email', 'first'),
            user_created_at=('created_at', 'first'),
            total_order_value=('order_total', 'sum'),
            total_orders=('order_id', 'nunique')
        ).reset_index()
        
        # 3. Add partition column
        daily_summary['load_date'] = execution_date
        
        logging.info(f"Transformed data into {len(daily_summary)} summary records.")
        return daily_summary

    def load(self, transformed_data: pd.DataFrame, execution_date: date) -> str:
        """Loads the transformed data into the destination (S3/Data Lake)."""
        if transformed_data.empty:
            logging.warning("No data to load.")
            return None
            
        # Define output path with date partitioning
        year = execution_date.year
        month = execution_date.month
        day = execution_date.day
        output_path = f"{self.dest_bucket}/users/daily_summary/year={year}/month={month}/day={day}/data.parquet"
        
        logging.info(f"Loading data to {output_path}...")
        
        # Convert to Arrow Table and write as Parquet
        table = pa.Table.from_pandas(transformed_data)
        with self.s3fs.open(output_path, 'wb') as f:
            pq.write_table(table, f, compression='snappy')
            
        logging.info("Load complete.")
        return output_path

    def run(self, execution_date: date):
        """Orchestrates the full E-T-L process."""
        try:
            raw_df = self.extract(execution_date)
            transformed_df = self.transform(raw_df, execution_date)
            load_path = self.load(transformed_df, execution_date)
            logging.info(f"ETL run successful for {execution_date}. Output: {load_path}")
        except Exception as e:
            logging.error(f"ETL run failed for {execution_date}: {e}")
            raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Daily User ETL Job")
    parser.add_argument(
        "--date", 
        required=True, 
        help="Execution date in YYYY-MM-DD format"
    )
    # In a real app, DB/S3 details would come from env vars or a config service
    parser.add_argument("--db-conn", required=True, help="Source DB connection string")
    parser.add_argument("--s3-bucket", required=True, help="Destination S3 bucket")
    
    args = parser.parse_args()
    
    exec_date = date.fromisoformat(args.date)
    
    job = DailyUserETL(
        source_db_conn_str=args.db_conn,
        dest_s3_bucket=args.s3_bucket
    )
    job.run(exec_date)
