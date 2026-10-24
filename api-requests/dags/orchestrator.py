import sys
import os

from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
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
    schedule="*/5 * * * *",
    catchup=False,
) as dag:
    test_task = PythonOperator(
        task_id="ingest_weather_data",
        python_callable=main,
    )

    transform_data_task = DockerOperator(
        task_id="transform_weather_data",
        image="ghcr.io/dbt-labs/dbt-postgres:1.9.0",
        command=["run"],
        working_dir="/usr/app",
        environment={
            "DBT_PROFILES_DIR": "/usr/app",
        },
        private_environment={
            "DB_USER": os.environ["DB_USER"],
            "DB_PASSWORD": os.environ["DB_PASSWORD"],
        },
        mounts=[
            Mount(
                source=os.environ["DBT_PROJECT_PATH"],
                target="/usr/app",
                type="bind",
            ),
        ],
        docker_url="unix:///var/run/docker.sock",
        network_mode="api-requests_default",
        mount_tmp_dir=False,
        auto_remove="success",
    )

    test_task >> transform_data_task
