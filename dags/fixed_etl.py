"""
DAG to ingest data for fixed broadband.
"""
from airflow.sdk import dag, task
import pandas as pd
import datetime


@dag(schedule='@daily', start_date=datetime.datetime(2025, 1, 1), catchup=False)
def fixed_etl():

    @task()
    def extract() -> dict:
       
        df = pd.read_csv("data/fcc/bdc_us_fixed_broadband_summary_by_geography_12-24.csv")
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

        df = pd.DataFrame(df_dict)
        # Here you would typically load the DataFrame to a database or data warehouse
        # For demonstration, we will just print the DataFrame shape
        print(f"Data loaded with shape: {df.shape}")    

    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)
    

fixed_etl()
