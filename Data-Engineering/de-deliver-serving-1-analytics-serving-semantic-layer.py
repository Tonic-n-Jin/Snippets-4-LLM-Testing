import pandas as pd
import logging
from sqlalchemy import create_engine, text
from datetime import date

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AnalyticsService:
    """
    A simple "Semantic Layer" that provides business-ready data.
    It connects to a data warehouse and serves pre-aggregated
    analytical views to BI tools or analysts.
    """
    def __init__(self, db_conn_str: str):
        try:
            self.engine = create_engine(db_conn_str)
            logging.info("AnalyticsService connected to data warehouse.")
        except Exception as e:
            logging.error(f"Failed to create engine: {e}")
            raise

    def get_sales_summary(self, start_date: date, end_date: date, regions: list[str] = None) -> pd.DataFrame:
        """
        Serves a pre-defined, aggregated OLAP-style view of sales.
        This query would be run by a BI tool (e.g., Tableau, Looker).
        """
        query = text("""
        SELECT
            d.calendar_date,
            p.product_category,
            g.region_name,
            SUM(f.sales_amount) AS total_sales,
            AVG(f.profit) AS average_profit,
            COUNT(DISTINCT f.order_id) AS total_orders
        FROM
            fact_sales f
        JOIN
            dim_date d ON f.date_key = d.date_key
        JOIN
            dim_product p ON f.product_key = p.product_key
        JOIN
            dim_geography g ON f.geo_key = g.geo_key
        WHERE
            d.calendar_date BETWEEN :start_date AND :end_date
            AND (:filter_regions = FALSE OR g.region_name IN :regions)
        GROUP BY
            d.calendar_date, p.product_category, g.region_name
        ORDER BY
            d.calendar_date, total_sales DESC;
        """)
        
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "filter_regions": bool(regions),
            "regions": tuple(regions or [])
        }
        
        logging.info(f"Serving sales summary for {start_date} to {end_date}")
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql(query, conn, params=params)
            logging.info(f"Served {len(df)} summary rows.")
            return df
        except Exception as e:
            logging.error(f"Failed to serve analytics query: {e}")
            raise
```