#!/bin/bash

echo "🔧 Starting RecallSpec Search in development mode..."

# Start infrastructure services only
echo "Starting infrastructure (PostgreSQL, Elasticsearch, Redis)..."
docker-compose up -d postgres elasticsearch redis

# Wait for services
echo "Waiting for services..."
sleep 10

# Initialize database
echo "Initializing database..."
cd backend
python init_db.py

# Start backend in background
echo "Starting backend..."
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ Development environment ready!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; docker-compose stop postgres elasticsearch redis" EXIT
wait
