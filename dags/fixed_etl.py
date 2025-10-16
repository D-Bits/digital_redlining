"""
DAG to ingest data for fixed broadband.
"""
from airflow.sdk import dag, task
from config import redlining_engine, REDLINING_DB_CONN
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
    def extract():
       
        df = pd.read_csv(
            "dags/data/fixed_sample.csv",
            low_memory=False,
            on_bad_lines='skip'
        )
        # Cast the dataframe to a dictionary to share with other tasks in DAG
        df_dict = df.to_dict(orient='records')

        return df_dict


    @task()
    def transform(df_dict: dict):

        df = pd.DataFrame(df_dict)

        fact_geo = df[[
            "geography_id",
            "area_data_type", 
            "geography_type", 
            "geography_desc",
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

        # Write data to the db
        dim_speed.to_sql(
            'dim_speed', 
            con=REDLINING_DB_CONN, 
            schema='fcc_fixed',
            if_exists='append',
            method='multi', 
            index=False
        )
        dim_tech.to_sql(
            'dim_tech', 
            con=REDLINING_DB_CONN, 
            schema='fcc_fixed',
            if_exists='append',
            method='multi', 
            index=False
        )
        fact_geo.to_sql(
            'fact_geo', 
            con=REDLINING_DB_CONN, 
            schema='fcc_fixed',
            if_exists='append',
            method='multi', 
            index=False
        )

        print(f"Data loaded into fact_geo with: {len(fact_geo)} records")
        print(f"Data loaded into dim_speed with: {len(dim_speed)} records")    
        print(f"Data loaded into dim_tech with: {len(dim_tech)} records")    


    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)
    

fixed_etl()
