import pytest
from app.services.identity_spec import IdentitySpecEngine
from app.services.match_judge import MatchJudge
from app.services.resolution_spec import ResolutionSpecEngine

def test_vin_extraction():
    """Test VIN extraction from text"""
    engine = IdentitySpecEngine()
    spec = engine.parse_text("My VIN is 1HGBH41JXMN109186")

    assert spec.vin == "1HGBH41JXMN109186"
    assert spec.category == "vehicle"
    assert spec.status in ["partial", "complete"]

def test_upc_extraction():
    """Test UPC extraction from text"""
    engine = IdentitySpecEngine()
    spec = engine.parse_text("Product UPC: 123456789012")

    assert spec.upc == "123456789012"

def test_brand_model_extraction():
    """Test brand and model extraction"""
    engine = IdentitySpecEngine()
    spec = engine.parse_text("Honda Accord 2023 recall")

    assert spec.brand == "Honda"
    assert "Accord" in spec.model

def test_match_scoring():
    """Test match judge scoring"""
    judge = MatchJudge()

    identity_spec = type('obj', (object,), {
        'vin': '1HGBH41JXMN109186',
        'brand': 'Honda',
        'model': 'Accord',
        'category': 'vehicle',
        'upc': None,
        'lot': None
    })()

    recall = {
        'identifiers': {'vin_pattern': '1HGBH41JXMN109186'},
        'brand': 'Honda',
        'model': 'Accord',
        'category': 'vehicle'
    }

    score, status = judge._score_match(identity_spec, recall)

    assert status == "exact_match"
    assert score == 1.0

def test_partial_match():
    """Test partial match scoring"""
    judge = MatchJudge()

    identity_spec = type('obj', (object,), {
        'vin': None,
        'brand': 'Honda',
        'model': 'Accord',
        'category': 'vehicle',
        'upc': None,
        'lot': None
    })()

    recall = {
        'identifiers': {},
        'brand': 'Honda',
        'model': 'Accord',
        'category': 'vehicle'
    }

    score, status = judge._score_match(identity_spec, recall)

    assert status == "probable_match"
    assert score > 0.5

def test_no_match():
    """Test no match scenario"""
    judge = MatchJudge()

    identity_spec = type('obj', (object,), {
        'vin': None,
        'brand': 'Toyota',
        'model': 'Camry',
        'category': 'vehicle',
        'upc': None,
        'lot': None
    })()

    recall = {
        'identifiers': {},
        'brand': 'Honda',
        'model': 'Accord',
        'category': 'vehicle'
    }

    score, status = judge._score_match(identity_spec, recall)

    assert status == "no_match"
    assert score < 0.3

def test_resolution_spec_high_risk():
    """Test resolution spec for high risk recall"""
    from app.services.identity_spec import IdentitySpecEngine

    engine = ResolutionSpecEngine()
    identity_engine = IdentitySpecEngine()

    identity_spec = identity_engine.parse_text("Tesla Model S VIN: 5YJSA1E14HF000001")

    scored_matches = [{
        'score': 1.0,
        'match_status': 'exact_match',
        'match_reasons': ['VIN match'],
        'recall': {
            'title': 'Steering Wheel Detachment',
            'description': 'Steering wheel may detach during operation',
            'risk_level': 'high',
            'remedy': 'Stop using immediately and contact dealer',
            'manufacturer': 'Tesla',
            'recall_date': '2023-01-15',
            'affected_units': 5000,
            'authority': 'NHTSA',
            'authority_record_id': 'NHTSA-23V-123'
        }
    }]

    resolution = engine.generate_resolution(identity_spec, scored_matches)

    assert resolution.match_status == "exact_match"
    assert resolution.risk_level == "high"

def test_empty_query():
    """Test handling of empty query"""
    engine = IdentitySpecEngine()
    spec = engine.parse_text("")

    assert spec.status == "minimal"

def test_multiple_identifiers():
    """Test extraction of multiple identifiers"""
    engine = IdentitySpecEngine()
    spec = engine.parse_text("Honda Accord VIN: 1HGBH41JXMN109186 UPC: 123456789012")

    assert spec.vin == "1HGBH41JXMN109186"
    assert spec.upc == "123456789012"
    assert spec.brand == "Honda"
    assert spec.model == "Accord"
