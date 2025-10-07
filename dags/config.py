"""
Config file for various DAG settings.
"""
import os 


# Environment variables
AIRFLOW_DB_CONN = os.getenv("AIRFLOW_DB_CONN")
REDLINING_DB_CONN = os.getenv("REDLINING_DB_CONN")
