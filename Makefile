.PHONY: up down restart psql logs clean

DB_URL ?= postgres://postgres:postgrespassword@localhost:5432/playground

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down -v
	docker compose up -d

psql:
	docker exec -it playground-postgres psql -U postgres -d playground

logs:
	docker compose logs -f postgres

# Run SQL script directly: make run file=database/concurrency/01-write-skew/setup.sql
run:
	docker exec -i playground-postgres psql -U postgres -d playground < $(file)
