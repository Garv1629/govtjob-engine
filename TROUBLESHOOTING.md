# Operations Playbook & Troubleshooting Guide

## Common Operational Issues & Remediation

### 1. Telegram Bot Webhook Fails to Process Updates
- **Symptom**: Telegram bot does not respond to `/start` or inline button clicks.
- **Root Cause**: Invalid `TELEGRAM_BOT_TOKEN`, user ID authorization mismatch, or webhook SSL validation failure.
- **Remediation**:
  1. Inspect status: `curl http://localhost/api/v1/telegram/status`.
  2. Verify user ID is listed in `TELEGRAM_ALLOWED_USER_IDS` in `.env`.
  3. Re-initialize bot webhook:
     ```bash
     curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://yourdomain.com/api/v1/telegram/webhook
     ```

### 2. Playwright Headless Browser Timeout / Crash
- **Symptom**: Workflow pauses at `AUTOMATION_RUNNING` or logs `TimeoutError: Navigation 30000ms exceeded`.
- **Root Cause**: Slow portal server response (SSC/UPSC captcha page delay) or missing OS browser dependencies.
- **Remediation**:
  1. Check system RAM usage: `curl http://localhost/api/v1/metrics`. Ensure at least 1.5 GB available.
  2. Reinstall Playwright dependencies inside container:
     ```bash
     docker exec -it govtjob_backend playwright install-deps
     ```
  3. Trigger state machine auto-recovery: `curl -X POST http://localhost/api/v1/workflow/wf_id/recover`.

### 3. Database Connection Pool Exhaustion
- **Symptom**: Backend returns HTTP 500 with `TimeoutError: QueuePool limit of size 20 overflow`.
- **Remediation**:
  1. Increase pool settings in `.env`: `DB_POOL_SIZE=30` and `DB_MAX_OVERFLOW=20`.
  2. Restart backend worker: `docker-compose restart backend`.

---

## Log Inspection Quick Commands

```bash
# View live backend application logs
docker-compose logs -f --tail=100 backend

# Search structured JSON error logs
grep '"level": "ERROR"' backend/logs/app.log

# Inspect security audit trail
cat backend/logs/audit.log
```
