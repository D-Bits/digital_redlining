"""
DAG to initialize the redlining database.
"""
from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
# from airflow.providers.postgres.operators.postgres import PostgresOperator
import datetime


@dag(
    schedule=None, 
    start_date=datetime.datetime(2025, 1, 1), 
    catchup=False,
    tags=['fcc'],
    dag_id='db_init'
)
def db_init():

    @task
    def create_db():

        create_database = SQLExecuteQueryOperator(
            task_id='create_db', 
            conn_id='pg_main',
            database='postgres', 
            sql='init.sql',
            autocommit=True
        )

    @task
    def create_schemas():
        
        create_schemas = SQLExecuteQueryOperator(
            task_id='create_schemas', 
            conn_id='pg_redlining', 
            database='redlining',
            sql="schemas.sql",
            autocommit=True
        )
    
    @task
    def create_tables():

        create_tbl = SQLExecuteQueryOperator(
            task_id='create_tables', 
            conn_id='pg_redlining', 
            database='redlining',
            sql="tables.sql",
            autocommit=True
        )


    create_db()
    create_schemas()
    create_tables() 


db_init()

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