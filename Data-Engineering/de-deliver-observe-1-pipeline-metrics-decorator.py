import time
import logging
from contextlib import contextmanager
from functools import wraps

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MockMetricsClient:
    """Mock client for a metrics backend (e.g., Prometheus, StatsD)."""
    def gauge(self, metric_name, value, tags=None):
        logging.info(f"GAUGE: {metric_name} = {value} (tags: {tags})")
        
    def counter(self, metric_name, value=1, tags=None):
        logging.info(f"COUNTER: {metric_name} += {value} (tags: {tags})")
        
    def histogram(self, metric_name, value, tags=None):
        logging.info(f"HISTOGRAM: {metric_name} observed {value} (tags: {tags})")

class PipelineMonitor:
    """Provides decorators/context managers for monitoring job execution."""
    
    def __init__(self, client: MockMetricsClient):
        self.client = client

    @contextmanager
    def monitor_job(self, job_name: str):
        """
        A context manager to monitor a job's latency, success/failure,
        and throughput.
        """
        tags = {'job': job_name}
        self.client.counter(f"job.started", tags=tags)
        start_time = time.monotonic()
        
        # This tracker dict can be updated inside the 'with' block
        tracker_stats = {"records_processed": 0}
        
        try:
            yield tracker_stats
            self.client.counter(f"job.success", tags=tags)
            
        except Exception as e:
            self.client.counter(f"job.failed", tags=tags)
            logging.error(f"Job '{job_name}' failed: {e}")
            raise # Re-raise the exception
            
        finally:
            latency = time.monotonic() - start_time
            self.client.histogram(f"job.latency_seconds", latency, tags=tags)
            
            # Calculate throughput
            records = tracker_stats.get("records_processed", 0)
            if records > 0 and latency > 0:
                throughput = records / latency
                self.client.gauge(f"job.throughput_records_sec", throughput, tags=tags)

# --- Example Usage ---
metrics_client = MockMetricsClient()
monitor = PipelineMonitor(client=metrics_client)

@monitor.monitor_job(job_name="daily_user_etl")
def run_etl_job(tracker):
    """Simulated ETL job."""
    print("ETL job running...")
    time.sleep(0.5) # Simulate work
    tracker["records_processed"] = 10000
    print("ETL job finished.")

# Run the job
try:
    with monitor.monitor_job(job_name="daily_report_job") as tracker:
        print("Report job running...")
        time.sleep(0.2)
        tracker["records_processed"] = 500
        # Uncomment to test failure:
        # raise ValueError("DB connection failed")
        print("Report job finished.")
except Exception:
    pass
