import os
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2016, 2, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "nyc_taxi_etl",
    default_args=default_args,
    schedule_interval="0 15 * * *",
    catchup=True,
    end_date=datetime(2016, 2, 28),
)

etl_task = DockerOperator(
    task_id="run_etl",
    image="etl-service",
    auto_remove=True,
    command="python etl.py {{ ds }}",
    docker_url="unix://var/run/docker.sock",
    network_mode="core_network",
    environment={
        "MONGO_URI": os.getenv("MONGO_URI"),
        "MONGO_DB_NAME": os.getenv("MONGO_DB_NAME"),
        "MONGO_COLLECTION_NAME": os.getenv("MONGO_COLLECTION_NAME"),
    },
    dag=dag,
)

etl_task
