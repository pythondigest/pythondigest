#/bin/bash

BACKUP_DIR_PATH='/home/pythondigest/pythondigest/backups'

# clone to yandex disk
echo "Run rclone"
rclone sync --ignore-existing --create-empty-src-dirs  $BACKUP_DIR_PATH yandex-pydigest:backups/pythondigest/postgresql/

# remove old backups
echo "Remove old backups"
find $BACKUP_DIR_PATH -name "*.sql.gz" -type f -mtime +7 -delete
