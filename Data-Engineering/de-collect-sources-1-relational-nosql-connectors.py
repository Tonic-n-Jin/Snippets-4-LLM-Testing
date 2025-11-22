import logging
import pandas as pd
from sqlalchemy import create_engine, text
from pymongo import MongoClient, errors
from typing import Any, Dict, List, Generator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SqlConnector:
    """Handles connection and paginated querying for relational databases."""
    
    def __init__(self, db_conn_str: str):
        try:
            self.engine = create_engine(db_conn_str)
            logging.info("SQLAlchemy engine created successfully.")
        except Exception as e:
            logging.error(f"Failed to create SQLAlchemy engine: {e}")
            raise

    def query_paginated(self, query: str, page_size: int = 1000) -> Generator[pd.DataFrame, None, None]:
        """
        Executes a large query in chunks using OFFSET/LIMIT.
        Yields DataFrames page by page to conserve memory.
        """
        offset = 0
        while True:
            paginated_query = f"{query} LIMIT {page_size} OFFSET {offset}"
            logging.info(f"Executing query with OFFSET {offset}...")
            try:
                with self.engine.connect() as conn:
                    df = pd.read_sql(text(paginated_query), conn)
                
                if df.empty:
                    logging.info("Query finished, no more data.")
                    break
                
                yield df
                offset += page_size
                
            except Exception as e:
                logging.error(f"Error during paginated query: {e}")
                raise

class NoSqlConnector:
    """Handles connection and querying for MongoDB."""
    
    def __init__(self, conn_str: str, db_name: str):
        try:
            self.client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
            self.client.server_info() # Test connection
            self.db = self.client[db_name]
            logging.info(f"MongoDB client connected to db '{db_name}'.")
        except errors.ServerSelectionTimeoutError as e:
            logging.error(f"MongoDB connection failed: {e}")
            raise

    def find_documents(self, collection_name: str, filter: Dict[str, Any], projection: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Finds multiple documents in a collection based on a filter."""
        try:
            collection = self.db[collection_name]
            results = list(collection.find(filter, projection))
            logging.info(f"Found {len(results)} documents in '{collection_name}'.")
            return results
        except Exception as e:
            logging.error(f"Failed to find documents: {e}")
            raise
