# Quick Start Guide

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- pip and npm

## Installation

### 1. Start Infrastructure

```bash
cd recallspec-search
docker-compose up -d
```

This starts PostgreSQL, Elasticsearch, and Redis.

### 2. Initialize Database

```bash
cd backend
pip install -r requirements.txt
python init_db.py
```

### 3. Start Backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend runs at http://localhost:8000
API docs at http://localhost:8000/docs

### 4. Start Frontend

```bash
cd ../frontend
npm install
npm start
```

Frontend runs at http://localhost:3000

## Usage Examples

### Search by VIN
```
1HGBH41JXMN109186
```

### Search by text
```
Honda Accord 2023 recall
```

### Search by UPC
```
123456789012
```

## API Testing

```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Honda Accord"}'
```

## Troubleshooting

**Elasticsearch not starting:**
- Increase Docker memory to 4GB+

**Port conflicts:**
- Change ports in docker-compose.yml

**Module import errors:**
- Ensure you're in the backend directory
- Run `pip install -r requirements.txt`
