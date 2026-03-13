import pytest
from app.services.identity_spec import IdentitySpecEngine
from app.services.match_judge import MatchJudge

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
