from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'data_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:
    
    def extract_data(**context):
        """Pull data from multiple sources"""
        sources = ['database', 'api', 's3']
        data = {}
        for source in sources:
            data[source] = fetch_from_source(source)
        return data
    
    def transform_data(**context):
        """Apply business logic transformations"""
        data = context['task_instance'].xcom_pull(
            task_ids='extract'
        )
        transformed = apply_transformations(data)
        validate_data_quality(transformed)
        return transformed
    
    def load_data(**context):
        """Load to data warehouse"""
        data = context['task_instance'].xcom_pull(
            task_ids='transform'
        )
        load_to_warehouse(data)
    
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract_data
    )
    
    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform_data
    )
    
    load_task = PythonOperator(
        task_id='load',
        python_callable=load_data
    )
    
    extract_task >> transform_task >> load_task