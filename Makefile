export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up test

build:
	docker-compose build

up:
	docker-compose up -d api

down:
	docker-compose down --remove-orphans

test: up
	docker-compose run --rm --no-deps --entrypoint=pytest api /tests/unit /tests/e2e

unit:
	docker-compose run --rm --no-deps --entrypoint=pytest api /tests/unit

e2e: up
	docker-compose run --rm --no-deps --entrypoint=pytest api /tests/e2e

logs:
	docker-compose logs api | tail -100

black:
	black -l 86 $$(find * -name '*.py')
