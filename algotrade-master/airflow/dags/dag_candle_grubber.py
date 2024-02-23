import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from algotrade.etl.candle_grubber import run as run_candle_grubber


default_args = {
    "owner": "airflow",
    "retries": None,
}

dag_candle_grubber = DAG(
    dag_id="dag_candle_grubber",
    default_args=default_args,
    description="Candle grubber",
    # schedule=None,
    schedule="*/5 * * * *",
    max_active_runs=3,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=["algotrade"],
    catchup=False,
)


candle_grubber = PythonOperator(
    python_callable=run_candle_grubber,
    task_id="candle_grubber",
    dag=dag_candle_grubber,
)

candle_grubber
