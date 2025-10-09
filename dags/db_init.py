"""
DAG to initialize the redlining database.
"""
from airflow.sdk import dag, task, DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from config import redlining_engine
import pandas as pd


@dag(
    schedule=None, 
    start_date=pd.Timestamp("2025-01-01"), 
    catchup=False,
    tags=['other'],
    dag_id='db_init'
)
def db_init():

    @task()
    def create_db():

        return PostgresOperator(task_id='create_db', conn_id='airflow_default', sql='CREATE DATABASE IF NOT EXISTS redlining;')
    
    @task()
    def create_tables():

        return PostgresOperator(task_id='create_tables', conn_id='redlining_pg', sql="queries/tables.sql")

    create_db = create_db()
    create_tables = create_tables() 


# db_init()

# def create_db():

#     return PostgresOperator(
#         task_id='create_db', 
#         conn_id='airflow_default', 
#         sql='CREATE DATABASE IF NOT EXISTS redlining;'
#     )


# def create_tables():

#     return PostgresOperator(
#         task_id='create_tables', 
#         conn_id='redlining_pg', 
#         sql="queries/tables.sql"
#     )


# with DAG(
#     dag_id='db_init',
#     schedule=None,
#     start_date=pd.Timestamp("2025-01-01"),
#     catchup=False,
#     tags=['other']
# ) as dag:

#     create_db = create_db()
#     create_tables = create_tables() 

#     create_db >> create_tables