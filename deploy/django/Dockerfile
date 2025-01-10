######################################################
# Base Image
######################################################
ARG PYTHON_VERSION=3.11-slim-bullseye
FROM python:${PYTHON_VERSION} as python

ENV PYTHONUNBUFFERED=1 \
         PYTHONDONTWRITEBYTECODE=1 \
         PIP_NO_CACHE_DIR=off \
         PIP_DISABLE_PIP_VERSION_CHECK=on \
         PIP_DEFAULT_TIMEOUT=30 \
         POETRY_NO_INTERACTION=1 \
         POETRY_VIRTUALENVS_IN_PROJECT=true \
         POETRY_HOME="/opt/poetry" \
         PYSETUP_PATH="/app" \
         VENV_PATH="/app/.venv" \
         POETRY_VERSION=1.8.3 \
         PIP_VERSION=24.2

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN pip install -U "pip==$PIP_VERSION" "poetry==$POETRY_VERSION"

######################################################
# Builder Image
######################################################
FROM python as python-build-stage

WORKDIR $PYSETUP_PATH

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y --fix-missing \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  libffi-dev \
  libpcre3 \
  libpcre3-dev \
  git \
  python3-all-dev && python -m pip install -U pip poetry

# Requirements are installed here to ensure they will be cached.
# Create Python Dependency and Sub-Dependency Wheels.
COPY pyproject.toml poetry.lock ./

RUN poetry install --without=dev --no-ansi

######################################################
# Production image
######################################################
FROM python as python-run-stage


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y --fix-missing\
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  git \
  vim \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH

# copy application code to WORKDIR
COPY ./ ${PYSETUP_PATH}
