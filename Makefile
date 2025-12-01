BASEDIR=$(CURDIR)
DOCDIR=$(BASEDIR)/docs
DISTDIR=$(BASEDIR)/dist


pip-tools:
	pip install -U pip
	curl -LsSf https://astral.sh/uv/install.sh | sh

requirements: pip-tools
	uv sync --group dev --group test

test:
	uv run python manage.py test

run-infra:
	docker compose -f deploy/docker_compose_infra.yml up --build

run-compose:
	docker compose -f deploy/docker_compose.yml up --build

build:
	docker compose -f deploy/docker_compose.yml build

run:
	uv run python manage.py compress --force && uv run python manage.py runserver

import:
	uv run python manage.py import_news

clean:
	docker compose -f deploy/docker_compose_infra.yml stop
	docker compose -f deploy/docker_compose_infra.yml rm pydigest_postgres
	docker volume rm pythondigest_pydigest_postgres_data
	docker volume rm pythondigest_pydigest_postgres_data_backups

restore:
	echo "Run manually:"
	docker cp $(ls ./backups/postgresql-pythondigest_*.sql.gz | grep `date "+%Y_%m_%d"` | sort -n | tail -1) pydigest_postgres:/backups
	docker compose -f deploy/docker_compose_infra.yml exec postgres backups
	echo "Run manually in docker:"
	docker compose -f deploy/docker_compose_infra.yml exec postgres bash
	restore $(cd /backups && ls -p | grep -v /backups  | sort -n | tail -1)

check:
	uv run pre-commit run --show-diff-on-failure --color=always --all-files

update: pip-tools
	uv lock --upgrade
	uv run pre-commit autoupdate

migrate:
	uv run python manage.py migrate
