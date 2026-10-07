from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from pendulum import datetime


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
        task_id="test_airflow",
        python_callable=example_task,
    )
