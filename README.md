# Appium iOS Screen Recorder

A modern web application for recording iOS device screens using Appium, designed to work with **PostgreSQL** in production but configured for **SQLite** for easy local development.

## Prerequisites
- **Python 3.8+**
- **Node.js 16+**

## Quick Start (Local Development)
For local testing, we use **SQLite** (a local file database) so you don't need to install a database server.

You will need **two terminal windows**.

### Terminal 1: Backend
The backend runs on port `8000`.

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run server (Mock Mode + SQLite)
# Unix/Bash:
export MOCK_MODE=true
export DATABASE_URL="sqlite:///./recordings.db"
export PYTHONPATH=.
uvicorn src.api.main:app --port 8000 --reload

# Windows PowerShell:
# $env:MOCK_MODE="true"; $env:DATABASE_URL="sqlite:///./recordings.db"; $env:PYTHONPATH="."; uvicorn src.api.main:app --port 8000 --reload
```

### Terminal 2: Frontend
The frontend runs on port `5173`.

```bash
cd frontend
npm install
npm run dev
```

---

## Production Setup (PostgreSQL)
For production deployment, use a real PostgreSQL database.

### 1. Database Setup
Ensure you have a PostgreSQL server running (e.g., AWS RDS or local).

```bash
# Export your PostgreSQL connection string
export DATABASE_URL="postgresql://user:password@localhost:5432/appium_recorder"
```

### 2. Run Backend
Do not use `MOCK_MODE` for production.

```bash
uvicorn src.api.main:app --port 8000
```

---

## Debugging & Maintenance

### Check Server Status
**Backend**: `netstat -ano | findstr :8000`
**Frontend**: `netstat -ano | findstr :5173`

### Kill Process (Windows)
```powershell
taskkill //F //PID <PID>
```

### Common Issues
- **"AttributeError: 'str' object has no attribute 'hex'**: This is a database type mismatch. Fixed in latest version by auto-converting UUIDs.
- **Port In Use**: Use the `taskkill` command above to free the port.
