.PHONY: build up down restart clean dev prod build-dev

IMAGE_TAG ?= latest

build:
	docker compose build --no-cache

build-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml build --no-cache

up:
	docker compose up -d

dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

prod:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

restart:
	docker compose restart

clean:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v

