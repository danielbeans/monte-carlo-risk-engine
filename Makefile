.PHONY: build up down restart clean

IMAGE_TAG ?= latest

build:
	docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

clean:
	docker compose down -v

