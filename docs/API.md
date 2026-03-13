# API Documentation

## Base URL
`http://localhost:8000`

## Endpoints

### Search

**POST /api/v1/search**

Search for product recalls by text, VIN, UPC, or structured fields.

**Request Body:**
```json
{
  "query": "1HGBH41JXMN109186",
  "fields": {
    "brand": "Honda",
    "model": "Accord"
  }
}
```

**Response:**
```json
{
  "identity_spec": {
    "id": "uuid",
    "status": "complete",
    "category": "vehicle",
    "brand": "Honda",
    "vin": "1HGBH41JXMN109186",
    "missing_fields": []
  },
  "resolution_spec": {
    "match_status": "exact_match",
    "risk_level": "high",
    "action_card": {
      "immediate_action": "Contact dealer for free repair",
      "next_steps": ["Schedule repair appointment"],
      "official_source": "https://..."
    }
  }
}
```

### Watchlist

**POST /api/v1/watchlist**

Add item to watchlist for monitoring.

**GET /api/v1/watchlist**

Get all watchlist items.

**DELETE /api/v1/watchlist/{item_id}**

Remove item from watchlist.

## Match States

- **exact_match:** Unique identifier match or all key fields match
- **probable_match:** Partial match, missing some fields
- **unresolved:** Insufficient data to confirm
- **no_match:** No relevant recalls found
