import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from algotrade.etl.dump_psql import run as run_dump_psql


default_args = {
    "owner": "airflow",
    "retries": None,
}

dag_dump_psql = DAG(
    dag_id="dag_dump_psql",
    default_args=default_args,
    description="Autodump postgresql",
    schedule="0 0 * * 3",
    max_active_runs=1,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=["datawagon"],
    catchup=False,
)


dump_psql = PythonOperator(
    python_callable=run_dump_psql,
    task_id="dump_psql",
    dag=dag_dump_psql,
)

dump_psql
