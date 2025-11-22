import logging
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CompletenessValidator:
    """
    Checks completeness by reconciling counts and key metrics between
    a source (e.g., operational DB) and a destination (e.g., data warehouse).
    """
    def __init__(self, source_conn_str: str, dest_conn_str: str):
        try:
            self.source_engine = create_engine(source_conn_str)
            self.dest_engine = create_engine(dest_conn_str)
            logging.info("Engines created for source and destination.")
        except Exception as e:
            logging.error(f"Failed to create engines: {e}")
            raise

    def _get_query_result(self, engine, query: str) -> int | float:
        """Helper to run a query and return a single scalar result."""
        with engine.connect() as conn:
            return conn.execute(text(query)).scalar_one()

    def check_row_count(self, source_table: str, dest_table: str, source_filter: str = "") -> dict:
        """Compares the row count of two tables, with an optional filter."""
        source_query = f"SELECT COUNT(*) FROM {source_table} WHERE 1=1 {source_filter}"
        dest_query = f"SELECT COUNT(*) FROM {dest_table} WHERE 1=1 {source_filter}"
        
        source_count = self._get_query_result(self.source_engine, source_query)
        dest_count = self._get_query_result(self.dest_engine, dest_query)
        
        is_complete = (source_count == dest_count)
        logging.info(f"Row Count Check: Source={source_count}, Dest={dest_count}, Match: {is_complete}")
        return {
            "check": "row_count",
            "source_count": source_count,
            "dest_count": dest_count,
            "match": is_complete
        }

    def check_metric_sum(self, source_table: str, dest_table: str, metric_col: str) -> dict:
        """Compares the SUM() of a key metric (e.g., 'sales') in two tables."""
        source_query = f"SELECT SUM({metric_col}) FROM {source_table}"
        dest_query = f"SELECT SUM({metric_col}) FROM {dest_table}"

        source_sum = self._get_query_result(self.source_engine, source_query)
        dest_sum = self._get_query_result(self.dest_engine, dest_query)
        
        # Use a small tolerance for floating point comparisons
        is_complete = abs(source_sum - dest_sum) < 0.001
        logging.info(f"Metric Sum Check ({metric_col}): Source={source_sum}, Dest={dest_sum}, Match: {is_complete}")
        return {
            "check": "metric_sum",
            "metric": metric_col,
            "source_sum": source_sum,
            "dest_sum": dest_sum,
            "match": is_complete
        }
