# Appium iOS Screen Recorder

A specialized application for automated iOS screen recording using Appium. The project features a FastAPI backend and a React frontend, integrated into a unified Docker architecture for deployment.

## Core Technologies
- **Backend:** Python 3.12, FastAPI, SQLAlchemy
- **Frontend:** React, Vite, Tailwind CSS
- **Infrastructure:** Docker, AWS (ECR, Elastic Beanstalk, CodeCommit)
- **Database:** PostgreSQL (Production), SQLite (Development)

## Local Development

### 1. Manual Execution (Non-Docker)
To run the services separately for rapid iteration:

**Backend**
```powershell
$env:MOCK_MODE="true"
$env:DATABASE_URL="sqlite:///./recordings.db"
$env:PYTHONPATH="."
uvicorn src.api.main:app --port 8000 --reload
```

**Frontend**
```powershell
cd frontend
npm install
npm run dev
```

### 2. Docker Execution
The system uses a multi-stage Docker build to compile the frontend and serve it via the Python backend.

```powershell
docker build -t ios-screen-recorder .
docker run -p 8080:8080 --env MOCK_MODE=true ios-screen-recorder
```

## AWS Deployment Workflow

### 1. Source Control (CodeCommit)
All source code and configuration files are versioned in AWS CodeCommit.
```powershell
git add .
git commit -m "commit message"
git push
```

### 2. Image Registry (ECR)
The application image is hosted in Amazon Elastic Container Registry.

**Authenticate**
```powershell
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 973508468954.dkr.ecr.eu-central-1.amazonaws.com
```

**Build and Push**
```powershell
docker build -t ios-screen-recorder .
docker tag ios-screen-recorder:latest 973508468954.dkr.ecr.eu-central-1.amazonaws.com/ios-screen-recorder:latest
docker push 973508468954.dkr.ecr.eu-central-1.amazonaws.com/ios-screen-recorder:latest
```

### 3. Environment (Elastic Beanstalk)
The application is deployed to Elastic Beanstalk using the Docker platform. The `Dockerrun.aws.json` file instructs the environment to pull the latest image from ECR.

**Deployment Command**
```powershell
eb deploy
```

**Status and Logs**
```powershell
eb status
eb logs
eb health
```

## Configuration

### Environment Variables
- `MOCK_MODE`: Set to `true` to simulate Appium recordings without a physical device.
- `DATABASE_URL`: Connection string for SQLite or PostgreSQL.
- `PORT`: Internal container port (Default: 8080).

### EB Extensions
Configuration for environment-specific settings (like database variables and deployment hooks) is located in the `.ebextensions/` directory.
- `000_deploy.config`: Deployment scripts and permissions.
- `001_envar.config`: Environment variable injections.

## Maintenance
To clear local database state, remove the `recordings.db` file. For production database migrations, ensure your PostgreSQL instance is reachable from the Elastic Beanstalk security group.
