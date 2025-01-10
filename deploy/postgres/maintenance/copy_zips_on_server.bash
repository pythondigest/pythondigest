#/bin/bash

BACKUP_DIR_PATH='/home/pythondigest/pythondigest/deploy/zips'

# clone to yandex disk
echo "Run rclone"
rclone sync --ignore-existing --create-empty-src-dirs  $BACKUP_DIR_PATH yandex-pydigest:backups/pythondigest/zips/
