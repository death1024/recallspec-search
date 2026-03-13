# RecallSpec Search

An Agentic Search Engine that converts vague product clues into verified recall decisions.

> **Note:** This project was developed for a friend in the United States to help consumers quickly identify product recalls and take appropriate safety actions. It aggregates official recall data from CPSC, NHTSA, and FDA to provide accurate, actionable information.

## What It Does

- **Input:** Product photos, barcodes, VINs, or text descriptions
- **Process:** Extracts product identity → searches official recall sources → matches and scores results
- **Output:** Actionable recall resolution with clear next steps

## Features

✅ Text search (VIN, UPC, brand, model, keywords)
✅ Image upload with OCR field extraction
✅ Multi-source recall search (CPSC, NHTSA, FDA)
✅ 4-state match classification (exact/probable/unresolved/no_match)
✅ Action cards with official remedy text
✅ Watchlist for monitoring products
✅ Shareable result links
✅ Audit logging

## Data Sources

- **CPSC** - Consumer products (toys, appliances, furniture)
- **NHTSA** - Vehicles, tires, child seats, equipment
- **FDA** - Drugs, medical devices, food

## Quick Start

### 1. Start Infrastructure

```bash
cd recallspec-search
docker-compose up -d
```

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

Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs

### 4. Start Frontend

```bash
cd ../frontend
npm install
npm start
```

Frontend: http://localhost:3000

## Usage Examples

### Search by VIN
```
1HGBH41JXMN109186
```

### Search by UPC
```
123456789012
```

### Search by Text
```
Honda Accord 2023 recall
baby stroller Acme brand
```

### Upload Product Image
Click "Choose File" and upload a photo of product label, then click "Search Image"

## API Endpoints

### POST /api/v1/search
Search by text query
```json
{
  "query": "Honda Accord",
  "fields": {"brand": "Honda", "model": "Accord"}
}
```

### POST /api/v1/search/image
Search by image upload (multipart/form-data)

### POST /api/v1/watchlist
Add item to watchlist

### GET /api/v1/watchlist
Get all watchlist items

### POST /api/v1/share
Create shareable link

### GET /api/v1/share/{token}
View shared result

## Match States

- **exact_match** - Unique identifier match (VIN/UPC) or all key fields match
- **probable_match** - Partial match, missing some fields
- **unresolved** - Insufficient data to confirm
- **no_match** - No relevant recalls found

## Project Structure

```
recallspec-search/
├── backend/
│   ├── app/
│   │   ├── api/routes/     # API endpoints
│   │   ├── services/       # Core business logic
│   │   ├── adapters/       # Data source adapters
│   │   ├── models/         # Pydantic models
│   │   └── db/             # Database connections
│   ├── ingestion/          # Background sync tasks
│   └── tests/              # Unit tests
├── frontend/
│   └── src/
│       ├── components/     # React components
│       └── App.js          # Main app
├── docs/                   # Documentation
└── docker-compose.yml      # Infrastructure setup
```

## Development

### Run Tests
```bash
cd backend
pytest tests/
```

### Data Ingestion
```bash
# Sync CPSC recalls
celery -A ingestion.tasks worker --loglevel=info
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and components
- [Data Sources](docs/DATA_SOURCES.md) - API details and sync strategies
- [API Documentation](docs/API.md) - Endpoint specifications
- [Quick Start](docs/QUICKSTART.md) - Detailed setup guide

## License

MIT License

## Contributing

See [PRD](recallspec-search-prd.md) for project requirements and roadmap.

## Architecture

- **Backend:** Python + FastAPI
- **Frontend:** React + TypeScript
- **Data:** PostgreSQL + Elasticsearch + Redis
- **Jobs:** Celery for background ingestion

## Core Concepts

**Product Identity Spec:** Structured representation of product (brand, model, UPC, VIN, etc.)

**Recall Resolution Spec:** Match result with evidence, risk level, and action card

**Match States:** exact_match | probable_match | unresolved | no_match
