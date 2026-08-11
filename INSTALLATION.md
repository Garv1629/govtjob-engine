# GovtJob AI Agent - Installation Guide

## Prerequisites

Ensure your system meets the minimum requirements:
- **Operating System**: Ubuntu 22.04 LTS, Debian 12, or Windows Server 2022 / WSL2.
- **Docker**: v24.0+ with Docker Compose v2.20+.
- **Hardware**: Minimum 2 CPU Cores, 4 GB RAM, 20 GB SSD storage.

---

## Local Development Installation

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Database Initialization**:
   ```bash
   alembic upgrade head
   python app/main.py
   ```

3. **Frontend Setup**:
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

   Access candidate dashboard at `http://localhost:3000`.

---

## Docker Production Installation

1. **Clone repository**:
   ```bash
   git clone https://github.com/org/govtjob-ai-agent.git
   cd govtjob-ai-agent
   ```

2. **Build and start services**:
   ```bash
   docker-compose up -d --build
   ```

3. **Check container logs**:
   ```bash
   docker-compose logs -f backend
   ```
