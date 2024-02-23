import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from algotrade.etl.orderstat_grubber import run as run_orderstat_grubber


default_args = {
    "owner": "airflow",
    "retries": None,
}

dag_orderstat_grubber = DAG(
    dag_id="dag_orderstat_grubber",
    default_args=default_args,
    description="orderstat grubber",
    # schedule=None,
    schedule="*/5 * * * *",
    max_active_runs=3,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=["algotrade"],
    catchup=False,
)


orderstat_grubber = PythonOperator(
    python_callable=run_orderstat_grubber,
    task_id="orderstat_grubber",
    dag=dag_orderstat_grubber,
)

orderstat_grubber
