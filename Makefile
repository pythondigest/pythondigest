BASEDIR=$(CURDIR)
DOCDIR=$(BASEDIR)/docs
DISTDIR=$(BASEDIR)/dist


pip-tools:
		pip install pip
		pip install pip-tools

requirements: pip-tools
		pip-compile requirements.in
		pip-sync requirements.txt
