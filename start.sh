#!/bin/bash

echo "Starting RecallSpec Search..."

# Start infrastructure
echo "Starting Docker services..."
docker-compose up -d

# Wait for services
echo "Waiting for services to be ready..."
sleep 10

# Start backend
echo "Starting backend API..."
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000 &

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm install
npm start &

echo "RecallSpec Search is running!"
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
