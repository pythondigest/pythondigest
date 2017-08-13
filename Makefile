BASEDIR=$(CURDIR)
DOCDIR=$(BASEDIR)/docs
DISTDIR=$(BASEDIR)/dist


pip-tools:
		pip install -U pip
		pip install -U pip-tools

requirements: pip-tools
		pip-compile requirements.in
		pip-sync requirements.txt

test:
		python manage.py test
