#/bin/bash

BACKUP_DIR_PATH='/home/pythondigest/pythondigest/deploy/media'

# clone to yandex disk
echo "Run rclone"
rclone sync --ignore-existing --create-empty-src-dirs  $BACKUP_DIR_PATH yandex-pydigest:backups/pythondigest/media/

# remove old backups
echo "Remove old files"
find $BACKUP_DIR_PATH -name "*.sql.gz" -type f -mtime +1000 -delete
