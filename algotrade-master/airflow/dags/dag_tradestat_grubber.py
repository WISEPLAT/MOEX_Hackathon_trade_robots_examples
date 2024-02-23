import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from algotrade.etl.tradestat_grubber import run as run_tradestat_grubber


default_args = {
    "owner": "airflow",
    "retries": None,
}

dag_tradestat_grubber = DAG(
    dag_id="dag_tradestat_grubber",
    default_args=default_args,
    description="tradestat grubber",
    # schedule=None,
    schedule="*/5 * * * *",
    max_active_runs=3,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=["algotrade"],
    catchup=False,
)


tradestat_grubber = PythonOperator(
    python_callable=run_tradestat_grubber,
    task_id="tradestat_grubber",
    dag=dag_tradestat_grubber,
)

tradestat_grubber
