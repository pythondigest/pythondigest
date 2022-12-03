BASEDIR=$(CURDIR)
DOCDIR=$(BASEDIR)/docs
DISTDIR=$(BASEDIR)/dist


pip-tools:
	pip install -U pip
	pip install -U pip-tools

requirements: pip-tools
	pip-compile --generate-hashes --reuse-hashes --build-isolation --pip-args "--retries 10 --timeout 30" requirements.in
	pip-sync requirements.txt

test:
	python manage.py test

run-infra:
	docker compose -f deploy/docker_compose_infra.yml up --build

run-compose:
	docker compose -f deploy/docker_compose.yml up --build

build:
	docker compose -f deploy/docker_compose.yml build

run:
	python manage.py runserver

import:
	python manage.py import_news

clean:
	docker compose -f deploy/docker_compose_infra.yml stop
	docker compose -f deploy/docker_compose_infra.yml rm pydigest_postgres
	docker volume rm pythondigest_pydigest_postgres_data
	docker volume rm pythondigest_pydigest_postgres_data_backups

restore:
	docker cp /home/axsapronov/Cloud/Dropbox/Backups/pydigest/postgresql-pythondigest-`date "+%Y-%m-%d"`.sqlc pydigest_postgres:/backups
	docker compose -f deploy/docker_compose_infra.yml exec postgres backups
	docker compose -f deploy/docker_compose_infra.yml exec postgres restore postgresql-pythondigest-`date "+%Y-%m-%d"`.sqlc

check:
	pre-commit run --show-diff-on-failure --color=always --all-files
