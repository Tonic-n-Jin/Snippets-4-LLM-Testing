from pyspark.sql import SparkSession
from pyspark.sql.functions import *

class SparkProcessor:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("DataPipeline") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()
    
    def process_large_dataset(self, input_path):
        """Process terabytes of data efficiently"""
        df = self.spark.read.parquet(input_path)
        
        # Optimized transformations
        result = df.filter(col("active") == True) \
            .groupBy("category", "date") \
            .agg(
                sum("amount").alias("total_amount"),
                count("*").alias("transaction_count"),
                avg("amount").alias("avg_amount")
            ) \
            .withColumn("processing_time", current_timestamp())
        
        # Dynamic partitioning for output
        result.repartition("date") \
            .write \
            .partitionBy("date") \
            .mode("overwrite") \
            .parquet("s3://bucket/processed/")