
start:
	sudo docker-compose up

startb:
	sudo docker-compose up --build

build:
	sudo docker-compose build

# Open a bash shell inside the Airflow trigger container
airflow_bash:
	sudo docker run -it digital_redlining-airflow-triggerer bash