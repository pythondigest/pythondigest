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
         PYSETUP_PATH="/app" \
         VENV_PATH="/app/.venv" \
         PIP_VERSION=24.2 \
         UV_PROJECT_ENVIRONMENT="/app/.venv" \
         UV_LINK_MODE="copy"

ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install -U "pip==$PIP_VERSION" && \
    curl -LsSf https://astral.sh/uv/install.sh | sh -s -- --install-dir /usr/local/bin

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
  python3-all-dev

# Requirements are installed here to ensure they will be cached.
# Create Python Dependency and Sub-Dependency wheels using uv.
COPY pyproject.toml uv.lock* poetry.lock* ./

RUN uv sync --frozen --no-dev

######################################################
# Production image
######################################################
FROM python as python-run-stage


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y --fix-missing \
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
