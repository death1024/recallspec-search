# RecallSpec Search Architecture

## System Overview

RecallSpec Search is a monolithic Python application with modular services that converts vague product clues into verified recall decisions.

## Core Components

### 1. Identity Spec Engine
- Parses user input (text, VIN, UPC) into structured Product Identity Spec
- Extracts fields using regex and keyword matching
- Assigns confidence scores per field
- Identifies missing critical fields

### 2. Retrieval Engine
- Three-tier search strategy:
  - **Tier 1:** Exact match (VIN, UPC via PostgreSQL)
  - **Tier 2:** Structured filter (brand + model via Elasticsearch)
  - **Tier 3:** Fuzzy full-text (semantic search via Elasticsearch)
- Routes queries to appropriate data sources (CPSC, NHTSA, FDA)

### 3. Match Judge
- Scores matches on 0-1 scale
- Classifies into 4 states:
  - exact_match (≥0.9)
  - probable_match (0.6-0.89)
  - unresolved (0.3-0.59)
  - no_match (<0.3)

### 4. Resolution Spec Engine
- Generates Recall Resolution Spec with action cards
- Extracts official remedy text (no LLM generation)
- Identifies uncertainties and missing fields

### 5. Data Adapters
- **CPSC:** Consumer products via REST API
- **NHTSA:** Vehicle recalls via REST API + VIN lookup
- **FDA:** Enforcement reports (future)

## Data Flow

```
User Query
    ↓
Identity Spec Engine → Product Identity Spec
    ↓
Retrieval Engine → Candidate Recalls
    ↓
Match Judge → Scored Matches
    ↓
Resolution Spec Engine → Recall Resolution Spec + Action Card
    ↓
API Response
```

## Technology Stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL (structured data), Elasticsearch (search), Redis (cache)
- **Jobs:** Celery for background ingestion
- **Frontend:** React 18, Axios

## Database Schema

### PostgreSQL Tables
- `recalls` - Normalized recall records from all sources
- `identity_specs` - User query parsed into structured specs
- `resolution_specs` - Match results with action cards
- `watchlist_items` - User-monitored products

### Elasticsearch Index
- `recalls` - Full-text searchable recall records with n-gram tokenization
