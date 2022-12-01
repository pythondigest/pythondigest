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
	docker compose -f local.infra.yml up --build

run-docker:
	docker compose -f local.yml up --build

build:
	docker compose -f local.yml build

run:
	python manage.py runserver

clean:
	docker compose -f local.infra.yml rm postgres
	docker volume rm pythondigest_pydigest_postgres_data
	docker volume rm pythondigest_pydigest_postgres_backups

check:
	pre-commit run --show-diff-on-failure --color=always --all-files
