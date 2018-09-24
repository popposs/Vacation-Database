all: stop build bootstrap-db run

refresh-db: boostrap-db run

stop:
	docker-compose down 

build: 
	docker-compose build

run:
	docker-compose up

bootstrap-db:	
	docker-compose up -d db
	docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

