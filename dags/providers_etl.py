"""
DAG to ingest data for fixed broadband.
"""
from airflow.sdk import dag, task
from config import redlining_engine
import pandas as pd
import datetime

 
@dag(
    schedule=None, 
    start_date=datetime.datetime(2025, 1, 1), 
    catchup=False,
    tags=['fcc'],
    dag_id='mobile_speed_etl'
)
def fixed_etl():

    @task()
    def extract() -> dict:
       
        provider_meta = pd.read_csv("data/fcc/bdc_us_mobile_broadband_summary_by_geography_D24_30sep2025.csv")
        mobile_provider = pd.read_csv("data/fcc/bdc_us_mobile_broadband_provider_summary_D24_30sep2025.csv")
        fixed_provider = pd.read_csv("data/fcc/bdc_us_fixed_broadband_provider_summary_D24_30sep2025.csv")

        df_dict = {
            'provider_meta': provider_meta.to_dict(orient='records'),
            'mobile_provider': mobile_provider.to_dict(orient='records'),
            'fixed_provider': fixed_provider.to_dict(orient='records'),
        }

        return df_dict
         
    @task()
    def load(df_dict: dict):

        provider_meta = pd.DataFrame(df_dict['provider_meta'])
        mobile_provider = pd.DataFrame(df_dict['mobile_provider'])
        fixed_provider = pd.DataFrame(df_dict['fixed_provider'])

        provider_meta.to_sql(
            'fact_provider_meta', 
            con=redlining_engine, 
            schema='fcc_provider',
            if_exists='append', 
            index=False
        )
        mobile_provider.to_sql(
            'dim_mobile_provider', 
            con=redlining_engine, 
            schema='fcc_provider',
            if_exists='append', 
            index=False
        )
        fixed_provider.to_sql(
            'dim_fixed_provider', 
            con=redlining_engine, 
            schema='fcc_provider',
            if_exists='append', 
            index=False
        )


    extracted_data = extract()
    load(extracted_data)
    

fixed_etl()
