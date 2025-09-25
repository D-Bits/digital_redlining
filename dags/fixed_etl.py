"""
DAG to ingest data for fixed broadband.
"""
from airflow.sdk import dag, task
from typing import Dict
import pandas as pd
import datetime
import glob


@dag(schedule='@daily', start_date=datetime.datetime(2023, 1, 1), catchup=False)
def fixed_etl():

    @task()
    def extract() -> dict:
        
        # Get all CSV file paths from the directory
        csv_files = glob.glob('data/fcc/fixed/*.csv')
        # Read and concatenate all CSV files into a single DataFrame
        df = pd.concat([pd.read_csv(f, low_memory=False) for f in csv_files], ignore_index=True)
        # Cast the dataframe to a dictionary to share with other tasks in DAG
        df_dict = df.to_dict(orient='records')

        return df_dict


    @task()
    def transform(df_dict: dict) -> dict:

        df = pd.DataFrame(df_dict)
        df_dict = df.to_dict(orient='records')

        return df_dict
        

    @task()
    def load(df_dict: dict):

        # Here you would typically load the DataFrame to a database or data warehouse
        # For demonstration, we will just print the DataFrame shape
        print(f"Data loaded with shape: {df.shape}")    

    extracted_data = extract()
    transformed_data = transform(extracted_data)
    

fixed_etl()
