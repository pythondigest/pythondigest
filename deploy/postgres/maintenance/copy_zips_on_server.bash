#/bin/bash

BACKUP_DIR_PATH='/home/pythondigest/pythondigest/deploy/zips'

# create dataset.zip
cd /home/pythondigest/pythondigest/deploy/dataset
sudo rm -f ./*
docker exec -it pydigest_django python manage.py create_dataset 30 80
cd /home/pythondigest/pythondigest/deploy/
rm -f dataset.zip
zip -r dataset.zip dataset
mkdir -p zips
mv dataset.zip zips

# create pages.zip
cd /home/pythondigest/pythondigest/deploy/
rm -f pages.zip
zip -r pages.zip pages
mkdir -p zips
mv pages.zip zips

# clone to yandex disk
echo "Run rclone"
rclone sync --create-empty-src-dirs  $BACKUP_DIR_PATH yandex-pydigest:backups/pythondigest/zips/
