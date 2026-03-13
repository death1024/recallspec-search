@echo off
echo Deploying RecallSpec Search with Docker...

echo Stopping existing containers...
docker-compose down

echo Building Docker images...
docker-compose build

echo Starting services...
docker-compose up -d

echo Waiting for services to start...
timeout /t 15 /nobreak

echo Initializing database...
docker-compose exec -T backend python init_db.py

echo Deployment complete!
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
