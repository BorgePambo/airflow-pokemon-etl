from airflow import DAG
from datetime import datetime
from pokemon import extract_pokemn
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "borginho",
    "start_date": datetime(2025, 5, 1)  # sem zero à esquerda no mês
}

dag = DAG(
    'pokemon_extract',
    default_args=default_args,  
    schedule_interval="0 10 * * *",
    catchup=False,
    max_active_runs=1
)

start_pipeline = DummyOperator(
    task_id="start_pipeline",
    dag=dag
)

extract_pokemns = PythonOperator(
    task_id="extract_pokemons",
    python_callable=extract_pokemn,
    dag=dag  # estava faltando o `dag` aqui
)

done_pipeline = DummyOperator(
    task_id="done_pipeline",
    dag=dag
)

start_pipeline >> extract_pokemns >> done_pipeline
