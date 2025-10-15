"""
DAG to ingest data for mobile broadband.
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
def mobile_etl():

    @task()
    def extract() -> dict:
       
        df = pd.read_csv("data/fcc/bdc_us_mobile_broadband_summary_by_geography_D24_30sep2025.csv")
        # Cast the dataframe to a dictionary to share with other tasks in DAG
        df_dict = df.to_dict(orient='records')

        return df_dict


    @task()
    def transform(df_dict: dict) -> dict:

        df = pd.DataFrame(df_dict)

        fact_geo = df[[
            "geography_id", 
            "geography_type", 
            "geography_desc", 
            "total_area"
        ]]
        dim_3g = df[[
            "geography_id",
            "mobilebb_5g_spd1_area_st_pct",
            "mobilebb_5g_spd1_area_iv_pct",
        ]]
        dim_4g = df[[
            "geography_id",
            "mobilebb_4g_spd1_area_st_pct",
            "mobilebb_4g_spd1_area_iv_pct",
        ]]
        dim_5g = df[[
            "geography_id",
            "mobilebb_5g_spd1_area_st_pct",
            "mobilebb_5g_spd1_area_iv_pct",
            "mobilebb_5g_spd2_area_st_pct",
            "mobilebb_5g_spd2 _area_iv_pct",
        ]]


        df_dict = {
            "fact_geo": fact_geo.to_dict(orient='records'),
            "dim_3g": dim_3g.to_dict(orient='records'),
            "dim_4g": dim_4g.to_dict(orient='records'),
            "dim_5g": dim_5g.to_dict(orient='records')
        }

        return df_dict
        

    @task()
    def load(df_dict: dict):

        fact_geo = pd.DataFrame.from_dict(df_dict["fact_geo"])
        dim_3g = pd.DataFrame.from_dict(df_dict["dim_3g"])
        dim_4g = pd.DataFrame.from_dict(df_dict["dim_4g"])
        dim_5g = pd.DataFrame.from_dict(df_dict["dim_4g"])

        # Write data to the db
        fact_geo.to_sql(
            'fact_geo', 
            con=redlining_engine, 
            schema='fcc_mobile',
            if_exists='append', 
            method='multi',
            index=False
        )
        dim_3g.to_sql(
            'dim_3g', 
            con=redlining_engine, 
            schema='fcc_mobile',
            if_exists='append', 
            method='multi',
            index=False
        )
        dim_4g.to_sql(
            'dim_4g', 
            con=redlining_engine, 
            schema='fcc_mobile',
            if_exists='append',
            method='multi', 
            index=False
        )
        dim_5g.to_sql(
            'dim_5g', 
            con=redlining_engine, 
            schema='fcc_mobile',
            if_exists='append',
            method='multi', 
            index=False
        )

        print(f"Data loaded into fact_geo with shape: {len(fact_geo)}")
        print(f"Data loaded into dim_3g with shape: {len(dim_3g)}")    
        print(f"Data loaded into dim_4g with shape: {len(dim_4g)}")
        print(f"Data loaded into dim_5g with shape: {len(dim_5g)}")    


    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)
    

mobile_etl()
