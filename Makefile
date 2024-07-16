SHELL := /bin/bash

build:
	docker compose up -d --build

up:
	docker compose up -d

bash:
	docker compose exec app bash

down:
	docker compose down

shell:
	docker compose run --rm app ipython

logs:
	docker compose logs -f app

network:
	docker network create common-network

test:
	docker compose run  --env ENV=TEST --rm app

lint:
	docker compose run --env ENV=LINT --rm app