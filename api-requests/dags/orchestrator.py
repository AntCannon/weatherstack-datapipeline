import sys

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from pendulum import datetime

sys.path.insert(0, "/opt/airflow/pipeline/api-requests")
from insert_records import main


def example_task():
    print("Airflow successfully ran my first task.")


with DAG(
    dag_id="weather_api_orchestrator",
    description="Load weather data into Postgres",
    start_date=datetime(2026, 10, 7, tz="America/New_York"),
    schedule=None,
    catchup=False,
) as dag:
    test_task = PythonOperator(
        task_id="ingest_weather_data",
        python_callable=main,
    )
