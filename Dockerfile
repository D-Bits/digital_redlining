FROM astrocrpublic.azurecr.io/runtime:3.1-1


WORKDIR /usr/local/airflow/

COPY requirements.txt . 


RUN pip install --no-cache-dir -r requirements.txt
