#!/bin/bash

echo "🚀 Deploying RecallSpec Search with Docker..."

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down

# Build images
echo "Building Docker images..."
docker-compose build

# Start all services
echo "Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 15

# Initialize database
echo "Initializing database..."
docker-compose exec -T backend python init_db.py

echo "✅ Deployment complete!"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
