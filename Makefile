.PHONY: build prune shell-frontend shell-django

build:
	docker-compose up --build

up: build

down:
	docker-compose -f docker-compose.yml down

shell-frontend:
	docker exec -it microblog_frontend /bin/bash

shell-django:
	docker exec -it microblog_django /bin/bash

prune:
	docker system prune -f

default: build