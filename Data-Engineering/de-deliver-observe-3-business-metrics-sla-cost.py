import pandas as pd
import logging
from datetime import time, datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ---
# Simulate metadata databases that store pipeline results and costs.
# In production, this would be a SQL database (e.g., Postgres, Snowflake).
# ---
pipeline_logs_df = pd.DataFrame({
    'job_name': ['daily_financial_report', 'user_etl', 'daily_financial_report'],
    'execution_date': pd.to_datetime(['2025-11-16', '2025-11-16', '2025-11-15']),
    'completion_time': pd.to_datetime(['2025-11-16 09:30:00', '2025-11-16 02:00:00', '2025-11-15 08:55:00']),
    'gigabytes_processed': [5.2, 80.5, 5.1]
})

pipeline_costs_df = pd.DataFrame({
    'job_name': ['daily_financial_report', 'user_etl', 'daily_financial_report'],
    'execution_date': pd.to_datetime(['2025-11-16', '2025-11-16', '2025-11-15']),
    'run_cost_usd': [0.75, 4.20, 0.74]
})


class BusinessMonitor:
    """Queries metadata stores to check business-level KPIs."""
    
    def __init__(self, logs_df, costs_df):
        # In production, this would be a SQLAlchemy connection string
        self.logs = logs_df
        self.costs = costs_df

    def check_sla_adherence(self, job_name: str, execution_date: str, sla_time: time):
        """Checks if a job met its completion time SLA."""
        log = self.logs[
            (self.logs['job_name'] == job_name) &
            (self.logs['execution_date'] == execution_date)
        ]
        
        if log.empty:
            logging.warning(f"SLA Check: No log found for {job_name} on {execution_date}")
            return {"sla_met": False, "status": "job_did_not_run"}
            
        completion_time = log.iloc[0]['completion_time'].time()
        sla_met = completion_time <= sla_time
        
        logging.info(f"SLA Check ({job_name}): Completed at {completion_time}, SLA: {sla_time}. Met: {sla_met}")
        return {"sla_met": sla_met, "completion_time": completion_time}

    def get_cost_per_gb(self, job_name: str, execution_date: str):
        """Calculates the processing cost per gigabyte."""
        log = self.logs[(self.logs['job_name'] == job_name) & (self.logs['execution_date'] == execution_date)]
        cost = self.costs[(self.costs['job_name'] == job_name) & (self.costs['execution_date'] == execution_date)]
        
        if log.empty or cost.empty:
            logging.error(f"Cost Check: Missing log or cost for {job_name} on {execution_date}")
            return None
        
        total_cost = cost.iloc[0]['run_cost_usd']
        total_gb = log.iloc[0]['gigabytes_processed']
        
        cost_per_gb = total_cost / total_gb
        logging.info(f"Cost Check ({job_name}): ${total_cost:.2f} / {total_gb} GB = ${cost_per_gb:.4f} per GB")
        return {"cost_per_gb": cost_per_gb, "total_cost": total_cost, "total_gb": total_gb}

# --- Example Usage ---
monitor = BusinessMonitor(pipeline_logs_df, pipeline_costs_df)

# 1. Check SLA for the financial report (SLA is 09:00 AM)
monitor.check_sla_adherence(
    job_name='daily_financial_report',
    execution_date='2025-11-16',
    sla_time=time(9, 0, 0) # Fails, completed at 9:30
)

# 2. Calculate cost for the user ETL
monitor.get_cost_per_gb(
    job_name='user_etl',
    execution_date='2025-11-16'
)
