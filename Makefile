all: stop build bootstrap-db run

stop:
	docker-compose down 

build: 
	docker-compose build

run:
	docker-compose up

bootstrap-db:	
	docker-compose up -d db
	docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

refresh-db:
	docker-compose down
	docker volume rm upgrade_coding_challenge_dbdata
