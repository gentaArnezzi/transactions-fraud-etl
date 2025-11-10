from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Jalankan skrip python berurutan untuk kesederhanaan
DEFAULT_ARGS = {
    "owner": "irgy",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="financial_etl_dag",
    default_args=DEFAULT_ARGS,
    schedule_interval="0 2 * * *",  # setiap hari jam 02:00
    start_date=datetime(2025, 11, 1),
    catchup=False,
    tags=["etl", "finance"],
):
    extract_api = BashOperator(
        task_id="extract_api",
        bash_command="python ${AIRFLOW_HOME}/../scripts/extract_api.py",
    )

    extract_db = BashOperator(
        task_id="extract_db",
        bash_command="python ${AIRFLOW_HOME}/../scripts/extract_db.py",
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="python ${AIRFLOW_HOME}/../scripts/transform.py",
    )

    load = BashOperator(
        task_id="load",
        bash_command="python ${AIRFLOW_HOME}/../scripts/load.py",
    )

    extract_api >> extract_db >> transform >> load

