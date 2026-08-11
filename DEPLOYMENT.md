# Production Deployment Guide & Checklist

## Overview Architecture

```
                       ┌────────────────────────┐
                       │  Nginx Reverse Proxy   │
                       │  (HTTPS / Rate Limit)  │
                       └───────────┬────────────┘
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                   ▼
      ┌────────────────────┐               ┌────────────────────┐
      │  Next.js 15 App    │               │  FastAPI Backend   │
      │  (Frontend Port    │               │  (Orchestrator     │
      │   3000)            │               │   Port 8000)       │
      └────────────────────┘               └─────────┬──────────┘
                                                     │
                             ┌───────────────────────┼───────────────────────┐
                             ▼                       ▼                       ▼
                   ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
                   │ PostgreSQL 16    │    │ Redis 7          │    │ Playwright       │
                   │ (Database)       │    │ (Rate Limit/Pub) │    │ Browser Engine   │
                   └──────────────────┘    └──────────────────┘    └──────────────────┘
```

---

## Deployment Checklist

### Pre-Deployment
- [x] Environment variable secrets generated (`SECRET_KEY`, `ENCRYPTION_KEY`, `POSTGRES_PASSWORD`).
- [x] SSL certificate installed or Let's Encrypt Certbot configured for Nginx.
- [x] Telegram bot token and authorized user IDs verified in `.env`.
- [x] Database migration scripts validated (`alembic upgrade head`).
- [x] Docker multi-stage builds compiled without errors.

### Deployment Steps
1. **Clone Repository & Configure Environment**:
   ```bash
   git clone https://github.com/org/govtjob-ai-agent.git
   cd govtjob-ai-agent
   cp backend/.env.example backend/.env
   # Edit backend/.env with production credentials
   ```

2. **Launch Docker Production Stack**:
   ```bash
   docker-compose up -d --build
   ```

3. **Verify Health Telemetry**:
   ```bash
   curl http://localhost/api/v1/health
   curl http://localhost/api/v1/metrics
   ```

4. **Setup Automated Backups**:
   ```bash
   crontab -e
   # Add daily backup at 2 AM
   0 2 * * * /bin/bash /path/to/govtjob-ai-agent/scripts/backup_db.sh >> /var/log/govtjob_backup.log 2>&1
   ```

---

## Security Best Practices
- **Rate Limiting**: Enforced via Nginx (`limit_req_zone`) and FastAPI `SecurityAndLoggingMiddleware`.
- **Security Headers**: HSTS, CSP, X-Frame-Options, X-Content-Type-Options enabled automatically.
- **Isolated Containers**: Non-root container users for Next.js and Python processes.
