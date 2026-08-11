# Zero-Downtime Upgrade & Migration Guide

## Upgrade Workflow

To upgrade the GovtJob AI Agent to a new release without interrupting active scraper monitoring or user sessions:

1. **Pull Latest Code**:
   ```bash
   git pull origin main
   ```

2. **Database Backup (Mandatory)**:
   ```bash
   ./scripts/backup_db.sh
   ```

3. **Apply Database Migrations**:
   ```bash
   docker exec -t govtjob_backend alembic upgrade head
   ```

4. **Rebuild & Rolling Restart Containers**:
   ```bash
   docker-compose up -d --no-deps --build backend frontend
   ```

5. **Verify Telemetry & Health Endpoint**:
   ```bash
   curl http://localhost/api/v1/health
   ```

---

## Rollback Procedure

If issues occur after upgrading:

1. **Revert Docker Containers**:
   ```bash
   docker-compose down
   git checkout tags/v1.0.0
   docker-compose up -d
   ```

2. **Restore Database Backup**:
   ```bash
   ./scripts/restore_db.sh ./backups/backup_govtjob_db_<timestamp>.sql.gz
   ```
