# Thalcare AI - Docker Setup Guide

This guide explains how to containerize the Thalcare AI backend application with PostgreSQL and enable team collaboration via Docker Hub.

## 📋 Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Project Structure](#project-structure)
5. [Docker Commands](#docker-commands)
6. [Team Collaboration](#team-collaboration)
7. [Development Workflow](#development-workflow)
8. [Publishing to Docker Hub](#publishing-to-docker-hub)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This setup uses **Docker Compose** to run both the FastAPI backend and PostgreSQL database in separate containers. The containers communicate through a Docker network.

**Components:**
- **Backend Container**: FastAPI application (Port 8000)
- **PostgreSQL Container**: Database (Port 5433)
- **Volumes**: Persistent data storage
- **Network**: Bridge network for communication

---

## 📦 Prerequisites

Before starting, ensure you have:

1. **Docker Desktop** installed
   - Download from: https://www.docker.com/products/docker-desktop
   - Available for Windows, macOS, and Linux

2. **Git** installed
   - Download from: https://git-scm.com/downloads

3. **Docker Hub account** (for collaboration)
   - Sign up at: https://hub.docker.com/

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd thalcare-AI/backend
```

### 2. Build and Run Containers
```bash
# Build and start all containers
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 3. Initialize Database
In a **new terminal**, run:
```bash
# Create tables in the database
docker-compose exec backend python create_tables.py
```

### 4. Access the Application
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Database**: localhost:5433

### 5. Stop Containers
```bash
# Stop containers (preserves data)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and delete volumes (⚠️ deletes data)
docker-compose down -v
```

---

## 📁 Project Structure

```
backend/
├── Dockerfile              # Backend container definition
├── docker-compose.yml      # Multi-container orchestration
├── .dockerignore          # Files to exclude from Docker build
├── requirements.txt       # Python dependencies
├── main.py               # FastAPI application
├── database.py           # Database connection
├── models.py             # SQLAlchemy models
├── schemas.py            # Pydantic schemas
├── crud.py               # Database operations
├── create_tables.py      # Initialize database tables
├── api/
│   └── routes.py         # API endpoints
└── DOCKER_SETUP.md       # This file
```

---

## 🐳 Docker Commands

### Building
```bash
# Build backend container
docker-compose build

# Force rebuild without cache
docker-compose build --no-cache
```

### Running
```bash
# Start all services
docker-compose up

# Start in detached mode (background)
docker-compose up -d

# Start specific service
docker-compose up backend postgres
```

### Management
```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs

# Follow logs (like tail -f)
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Stop services
docker-compose stop

# Remove containers
docker-compose down
```

### Executing Commands
```bash
# Run Python script in backend container
docker-compose exec backend python create_tables.py

# Access Python shell
docker-compose exec backend python

# Access bash shell in container
docker-compose exec backend bash

# Access PostgreSQL shell
docker-compose exec postgres psql -U postgres -d thalcare_ai_db
```

---

## 👥 Team Collaboration

### Scenario: Sharing with Team

**Team Member A (You):**
1. Build and tag the image
2. Push to Docker Hub
3. Share repository link

**Team Member B:**
1. Pull the image
2. Run locally
3. Make changes
4. Push updates

### Publishing Your Image

#### Step 1: Create Repository on Docker Hub
1. Go to https://hub.docker.com/
2. Click "Create Repository"
3. Name: `thalcare-backend`
4. Visibility: Public or Private
5. Click "Create"

#### Step 2: Build and Tag Image
```bash
# Build the image with Docker Hub tag
docker build -t your-dockerhub-username/thalcare-backend:latest .

# Example:
docker build -t johndoe/thalcare-backend:latest .
```

#### Step 3: Login to Docker Hub
```bash
docker login
# Enter your Docker Hub username and password
```

#### Step 4: Push to Docker Hub
```bash
# Push the image
docker push your-dockerhub-username/thalcare-backend:latest
```

#### Step 5: Share with Team
```bash
# Share this pull command with your team:
docker pull your-dockerhub-username/thalcare-backend:latest
```

### Using Published Image

**Team Member B can:**

1. **Pull the image:**
   ```bash
   docker pull your-dockerhub-username/thalcare-backend:latest
   ```

2. **Update docker-compose.yml:**
   ```yaml
   services:
     backend:
       image: your-dockerhub-username/thalcare-backend:latest  # Use pulled image
       # build:  # Comment out build section
       #   context: .
       #   dockerfile: Dockerfile
   ```

3. **Start containers:**
   ```bash
   docker-compose up
   ```

---

## 🔄 Development Workflow

### Workflow for Individual Developer

1. **Clone repository:**
   ```bash
   git clone <your-repo-url>
   cd thalcare-AI/backend
   ```

2. **Make changes to code**

3. **Rebuild container:**
   ```bash
   docker-compose up --build
   ```

4. **Test changes:**
   ```bash
   # Test API endpoints
   curl http://localhost:8000/health
   ```

5. **Commit and push:**
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

### Workflow for Team Collaboration

**When pulling updates:**
```bash
# Pull latest code
git pull origin main

# Rebuild containers with new changes
docker-compose up --build
```

**When pushing updates:**
```bash
# After making changes
git add .
git commit -m "Added new feature"
git push origin main

# Then update Docker image
docker build -t your-dockerhub-username/thalcare-backend:latest .
docker push your-dockerhub-username/thalcare-backend:latest
```

---

## 📤 Publishing to Docker Hub (Step-by-Step)

### First Time Setup

1. **Create Docker Hub account:** https://hub.docker.com/signup

2. **Create repository:**
   - Go to https://hub.docker.com/
   - Click "Create Repository"
   - Name: `thalcare-backend`
   - Visibility: Choose Public (free) or Private

3. **Login from terminal:**
   ```bash
   docker login
   # Enter username and password
   ```

### Build and Push Image

```bash
# Navigate to backend directory
cd backend

# Build image with tag
docker build -t your-username/thalcare-backend:latest .

# Tag for versioning (optional)
docker tag your-username/thalcare-backend:latest your-username/thalcare-backend:v1.0.0

# Push to Docker Hub
docker push your-username/thalcare-backend:latest
docker push your-username/thalcare-backend:v1.0.0
```

### Pull and Use Image

```bash
# Pull the image
docker pull your-username/thalcare-backend:latest

# Run with docker-compose (update docker-compose.yml to use image)
docker-compose up
```

---

## 🔧 Troubleshooting

### Issue: "Port already in use"
**Solution:**
```bash
# Stop existing containers
docker-compose down

# Or change ports in docker-compose.yml
```

### Issue: "Cannot connect to database"
**Solution:**
```bash
# Check if postgres container is running
docker-compose ps

# Check logs
docker-compose logs postgres

# Restart containers
docker-compose restart
```

### Issue: "Module not found" errors
**Solution:**
```bash
# Rebuild without cache
docker-compose build --no-cache

# Then restart
docker-compose up
```

### Issue: "Changes not reflecting"
**Solution:**
```bash
# Rebuild container
docker-compose up --build

# Or restart specific service
docker-compose restart backend
```

### Issue: Database data lost
**Solution:**
- Data persists in Docker volumes
- Don't use `docker-compose down -v` unless you want to delete data
- Use `docker-compose down` to preserve data

### Issue: Docker Daemon not running
**Solution:**
- Start Docker Desktop application
- Wait for it to fully start (whale icon in system tray)

---

## 📊 Environment Variables

The application uses the following environment variables:

```bash
# In docker-compose.yml
DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/thalcare_ai_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=thalcare_ai_db
```

To modify for production:
1. Create `.env` file
2. Update `docker-compose.yml` to use `.env`

---

## 🎯 Best Practices

1. **Always use volumes** for database data persistence
2. **Use .dockerignore** to exclude unnecessary files
3. **Tag images** with version numbers for releases
4. **Use docker-compose** for multi-container apps
5. **Keep Dockerfile lean** - use multi-stage builds if needed
6. **Document changes** in commit messages
7. **Test locally** before pushing to Docker Hub

---

## 📝 Summary

✅ **What you can do:**
- Containerize backend + PostgreSQL
- Share with team via Docker Hub
- Allow team to pull, run, edit, and push
- Maintain version control with Git + Docker Hub

✅ **Workflow:**
1. Build → 2. Push to Docker Hub → 3. Team pulls → 4. Team edits → 5. Team pushes

✅ **Benefits:**
- Consistent environments across team
- Easy deployment
- Version control for Docker images
- Fast onboarding for new team members

---

## 🔗 Useful Links

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 💡 Quick Reference

```bash
# Complete workflow for new team member
git clone <repo-url>
cd thalcare-AI/backend
docker-compose up -d
docker-compose exec backend python create_tables.py
# Access at http://localhost:8000/docs

# Update and push
git add . && git commit -m "update" && git push
docker build -t username/thalcare-backend:latest .
docker push username/thalcare-backend:latest
```
