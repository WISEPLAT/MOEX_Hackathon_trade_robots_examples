import pendulum
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 


default_args = {
    "owner": "airflow",
    "retries": None,
}

dag_analyze = DAG(
    dag_id="dag_analyze",
    default_args=default_args,
    description="Analyze",
    schedule=None,
    schedule="*/30 * * * *",
    max_active_runs=1,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=["algotrade"],
    catchup=False,
)


analyze = SparkSubmitOperator(
    application='/opt/airflow/dags/algotrade/etl/analyze.py',
    conn_id='spark_default',
    verbose=1,
    task_id='analyze', 
    dag=dag_analyze,
    jars='/opt/clickhouse-native-jdbc-shaded-2.7.1.jar'
)

analyze
