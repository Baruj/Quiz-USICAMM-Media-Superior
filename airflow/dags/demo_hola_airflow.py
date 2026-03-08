from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="demo_hola_airflow",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["demo", "local"],
    description="DAG minimo para entender como funciona Airflow en local",
) as dag:
    inicio = BashOperator(
        task_id="inicio",
        bash_command='echo "Inicio del flujo en Airflow"',
    )

    espera = BashOperator(
        task_id="espera",
        bash_command="sleep 5",
    )

    fin = BashOperator(
        task_id="fin",
        bash_command='echo "Fin del flujo en Airflow"',
    )

    inicio >> espera >> fin