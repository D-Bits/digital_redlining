
start:
	sudo astro dev start 

stop:
	sudo astro dev stop

restart:
	sudo astro dev restart

# Migrate change to the airflow metadata database
migrate:
	sudo docker exec -it digital-redlining_0cb618-dag-processor-1 airflow db migrate