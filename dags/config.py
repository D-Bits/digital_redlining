"""
Config file for various DAG settings.
"""
import sqlalchemy
import os 


# Environment variables
AIRFLOW_DB_CONN = os.getenv("AIRFLOW_DB_CONN")
REDLINING_DB_CONN = os.getenv("REDLINING_DB_CONN")

# DB SQL Alchemy engines
redlining_engine = sqlalchemy.create_engine(REDLINING_DB_CONN)
airflow_engine = sqlalchemy.create_engine(AIRFLOW_DB_CONN)