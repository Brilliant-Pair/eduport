flake8:
	flake8 --ignore=F405 .

black:
	black .

isort:
	isort .

base:
	pip install -r ./requirements/base.txt

local:
	pip install -r ./requirements/local.txt

production:
	pip install -r ./requirements/production.txt

l-build:
	docker compose -f ./local.yaml up --build -d

l-up:
	docker compose -f ./local.yaml up 

l-stop:
	docker compose -f ./local.yaml stop

l-down:
	docker compose -f ./local.yaml down

l-down-v:
	docker compose -f ./local.yaml down -v

l-logs:
	docker compose -f ./local.yaml logs

l-web-logs:
	docker compose -f ./local.yaml logs web

l-db-logs:
	docker compose -f ./local.yaml logs web

status:
	docker ps

shell:
	docker exec -it web bash

makemigrations:
	docker exec web python manage.py makemigrations

migrate:
	docker exec web python manage.py migrate
	
superuser:
	docker exec -it web python manage.py createsuperuser

backup:
	docker exec db backup.sh

backups:
	docker exec db backups.sh

remove-all:
	docker compose -f local.yaml down --rmi all