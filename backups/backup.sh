#!/usr/bin/env bash

set -euo pipefail

ts=$(date +%Y-%m-%d_%H-%M-%S)
filename="backup_${ts}.sql"

docker exec postgres pg_dump -U postgres -d images_db -f "/backups/${filename}"

echo "Backup created: '/backups/${filename}'"