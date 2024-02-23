import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from algotrade.etl.obstat_grubber import run as run_obstat_grubber


default_args = {
    "owner": "airflow",
    "retries": None,
}

dag_obstat_grubber = DAG(
    dag_id="dag_obstat_grubber",
    default_args=default_args,
    description="obstat grubber",
    # schedule=None,
    schedule="*/5 * * * *",
    max_active_runs=3,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=["algotrade"],
    catchup=False,
)


obstat_grubber = PythonOperator(
    python_callable=run_obstat_grubber,
    task_id="obstat_grubber",
    dag=dag_obstat_grubber,
)

obstat_grubber
