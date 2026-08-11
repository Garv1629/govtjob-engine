#!/bin/bash

# Production Database Automated Backup Script
# Usage: ./scripts/backup_db.sh

set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups"
DB_CONTAINER="govtjob_postgres"
DB_NAME="govtjob_db"
DB_USER="govtjob"

mkdir -p "$BACKUP_DIR"

BACKUP_FILE="$BACKUP_DIR/backup_${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "=========================================="
echo "Starting Database Backup for $DB_NAME"
echo "Timestamp: $TIMESTAMP"
echo "=========================================="

if [ "$(docker ps -q -f name=$DB_CONTAINER)" ]; then
    echo "Executing pg_dump inside container $DB_CONTAINER..."
    docker exec -t $DB_CONTAINER pg_dump -U $DB_USER -d $DB_NAME | gzip > "$BACKUP_FILE"
    echo "[SUCCESS] Compressed backup written to: $BACKUP_FILE"
else
    echo "[FALLBACK] Docker container not active; checking SQLite fallback..."
    if [ -f "./backend/govtjob.db" ]; then
        sqlite3 ./backend/govtjob.db ".backup '$BACKUP_DIR/backup_sqlite_${TIMESTAMP}.db'"
        echo "[SUCCESS] SQLite backup written to: $BACKUP_DIR/backup_sqlite_${TIMESTAMP}.db"
    else
        echo "[ERROR] No active database instance located for backup!"
        exit 1
    fi
fi

# Rotate backups older than 30 days
echo "Rotating backups older than 30 days..."
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +30 -delete
find "$BACKUP_DIR" -type f -name "*.db" -mtime +30 -delete

echo "Database Backup Completed Successfully!"
