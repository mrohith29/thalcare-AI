# Quick Start Guide

## Running the Application

### Prerequisites
- Docker Desktop installed
- Docker is running

### Steps

1. **Build and start containers:**
   ```bash
   docker-compose up --build
   ```

2. **Initialize database (in a new terminal):**
   ```bash
   docker-compose exec backend python create_tables.py
   ```

3. **Access the application:**
   - **API Documentation (Swagger UI)**: http://localhost:8000/docs
   - **API**: http://localhost:8000
   - **Health Check**: http://localhost:8000/health

### Stop the containers:
```bash
docker-compose down
```

### View logs:
```bash
docker-compose logs -f backend
```

## Project Structure

```
thalcare-AI/
├── backend/          # Backend application code
│   ├── api/
│   ├── models.py
│   ├── schemas.py
│   ├── main.py
│   └── requirements.txt
├── Dockerfile        # Backend container definition
├── docker-compose.yml # Multi-container setup
├── .dockerignore     # Files to exclude from build
└── datasets/         # Data files
```

## File Structure in Container

- Root: `/app/`
- Backend code: `/app/backend/`
- Working directory: `/app/backend/` (where commands run)
