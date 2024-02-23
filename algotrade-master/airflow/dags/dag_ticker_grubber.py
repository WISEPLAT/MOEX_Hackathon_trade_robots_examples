import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from algotrade.etl.ticker_grubber import run as run_ticker_grubber


default_args = {
    "owner": "airflow",
    "retries": None,
}

dag_ticker_grubber = DAG(
    dag_id="dag_ticker_grubber",
    default_args=default_args,
    description="Ticker grubber",
    schedule=None,
    # schedule="0 0 * * 3",
    max_active_runs=3,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=["algotrade"],
    catchup=False,
)


ticker_grubber = PythonOperator(
    python_callable=run_ticker_grubber,
    task_id="ticker_grubber",
    dag=dag_ticker_grubber,
)

ticker_grubber
