#!/usr/bin/env bash


### Create a database backup.
BACKUP_DIR_PATH='/home/pythondigest/pythondigest/backups'
BACKUP_FILE_PREFIX='postgresql-pythondigest'

mkdir -p $BACKUP_DIR_PATH


echo "Backing up the '${POSTGRES_DB}' database..."


if [[ "${POSTGRES_USER}" == "postgres" ]]; then
    message_error "Backing up as 'postgres' user is not supported. Assign 'POSTGRES_USER' env with another one and try again."
    exit 1
fi

export PGHOST="${POSTGRES_HOST}"
export PGPORT="${POSTGRES_PORT}"
export PGUSER="${POSTGRES_USER}"
export PGPASSWORD="${POSTGRES_PASSWORD}"
export PGDATABASE="${POSTGRES_DB}"

backup_filename="${BACKUP_FILE_PREFIX}_$(date +'%Y_%m_%dT%H_%M_%S').sql.gz"
pg_dump | gzip > "${BACKUP_DIR_PATH}/${backup_filename}"

echo "'${POSTGRES_DB}' database backup '${backup_filename}' has been created and placed in '${BACKUP_DIR_PATH}'."
