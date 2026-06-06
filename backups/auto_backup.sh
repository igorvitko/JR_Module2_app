#!/bin/sh

INTERVAL=3600

until pg_isready -h postgres -U postgres -d images_db; do
  echo "Чекаю postgres..."
  sleep 2
done

while true; do
    ts=$(date +%Y-%m-%d_%H-%M-%S)
    filename="backup_${ts}.sql"

    if pg_dump -U postgres -d images_db -h postgres -f "/backups/${filename}"; then
        echo "Backup created: '/backups/${filename}'"
    else
        echo "Помилка створення бекапу: '/backups/${filename}'"
    fi

    sleep $INTERVAL
done