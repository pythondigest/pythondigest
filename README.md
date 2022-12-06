python-news-digest
==================

[![build and deploy to server](https://github.com/pythondigest/pythondigest/actions/workflows/ci.yml/badge.svg)](https://github.com/pythondigest/pythondigest/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/pythondigest/pythondigest/badge.svg?branch=master)](https://coveralls.io/github/pythondigest/pythondigest?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/pythondigest/pythondigest/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/pythondigest/pythondigest/?branch=master)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)


What is it?
-----------


It is the repo with sources of project Python Digest (site - https://pythondigest.ru/ )
Python Digest is an aggregator of Python News
We aggregator many different links from Python World:

- books
- articles
- meetups
- releases
- etc

PythonDigest is a `Open Source` project!
We use `Python 3`

Contributing
------------

In general, we follow the "fork-and-pull" Git workflow.

> We develop in `develop` branch

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

> We recommend to use `git-flow`


How to start
------------

Clone project

```
git clone https://github.com/pythondigest/pythondigest.git
```

Create `virtualenv` and install dependencies:

```
virtualenv --python=python3 ./env
source ./env/bin/activate
cd pythondigest
pip install -r requirements.txt
```

Init database and install some fixtures:

```
python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py loaddata digest/fixtures/sections.yaml
python manage.py loaddata digest/fixtures/parsing_rules.json
```

Create super user
```
python manage.py createsuperuser
```

Ok! You are ready for work with Python Digest! (runserver...)

For developers:

```
python manage.py loaddata digest/fixtures/dev_issues.yaml
python manage.py loaddata digest/fixtures/dev_resource.yaml
python manage.py loaddata digest/fixtures/dev_items.yaml
```

Run tests
---------

```
python manage.py test
```
