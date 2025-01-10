#/bin/bash

BACKUP_DIR_PATH='/home/pythondigest/pythondigest/deploy/media'

# clone to yandex disk
echo "Run rclone"
rclone sync --ignore-existing --create-empty-src-dirs  $BACKUP_DIR_PATH yandex-pydigest:backups/pythondigest/media/
