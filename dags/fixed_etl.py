"""
DAG to ingest data for fixed broadband.
"""
from airflow.sdk import dag, task, DAG
import pandas as pd
import datetime


@dag(
    schedule=None, 
    start_date=datetime.datetime(2025, 1, 1), 
    catchup=False,
    tags=['fcc'],
    dag_id='fixed_speed_etl'
)
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

        fact_geo = df[[
            "geography_id",
            "area_data_type", 
            "geography_type", 
            "geography_desc", 
            "total_area"
        ]]
        dim_speed = df[[
            "geography_id", 
            "speed_02_02", 
            "speed_10_1", 
            "speed_25_3", 
            "speed_100_20", 
            "speed_250_25", 
            "speed_1000_100"
        ]]
        dim_tech = df[[
            "geography_id", 
            "area_data_type",
            "biz_res",
            "technology",
            "total_units"
        ]]

        df_dict = {
            "fact_geo": fact_geo.to_dict(orient='records'),
            "dim_speed": dim_speed.to_dict(orient='records'),
            "dim_tech": dim_tech.to_dict(orient='records')
        }

        return df_dict
        

    @task()
    def load(df_dict: dict):

        fact_geo = pd.DataFrame.from_dict(df_dict["fact_geo"])
        dim_speed = pd.DataFrame.from_dict(df_dict["dim_speed"])
        dim_tech = pd.DataFrame.from_dict(df_dict["dim_tech"])

        

        print(f"Data loaded into fact_geo with shape: {fact_geo.shape}")
        print(f"Data loaded into fact_geo with shape: {dim_speed.shape}")    
        print(f"Data loaded into fact_geo with shape: {dim_tech.shape}")    


    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)
    

fixed_etl()
