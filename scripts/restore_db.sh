#!/bin/bash

# Production Database Restoration Script
# Usage: ./scripts/restore_db.sh <path_to_backup_file>

set -e

BACKUP_FILE=$1
DB_CONTAINER="govtjob_postgres"
DB_NAME="govtjob_db"
DB_USER="govtjob"

if [ -z "$BACKUP_FILE" ]; then
    echo "[ERROR] Missing backup file path!"
    echo "Usage: ./scripts/restore_db.sh ./backups/backup_govtjob_db_20260804_120000.sql.gz"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "[ERROR] Specified backup file does not exist: $BACKUP_FILE"
    exit 1
fi

echo "=========================================="
echo "WARNING: Restoring Database from $BACKUP_FILE"
echo "Target Container: $DB_CONTAINER | Target DB: $DB_NAME"
echo "=========================================="
read -p "Are you sure you want to overwrite current database? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restoration cancelled."
    exit 1
fi

echo "Restoring database..."
gunzip -c "$BACKUP_FILE" | docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME

echo "[SUCCESS] Database restored successfully from $BACKUP_FILE!"
