import pytest
from app.services.identity_spec import IdentitySpecEngine

def test_unknown_brand_extraction():
    """Test extraction of brands not in predefined list"""
    engine = IdentitySpecEngine()

    # Test with Mitsubishi (not in predefined list)
    spec = engine.parse_text("Mitsubishi Outlander 2022 recall")
    assert spec.brand == "Mitsubishi"
    assert "Outlander" in spec.model
    assert spec.brand_confidence > 0.5

def test_alphanumeric_model():
    """Test extraction of alphanumeric models like F-150"""
    engine = IdentitySpecEngine()
    spec = engine.parse_text("Ford F-150 recall")

    assert spec.brand == "Ford"
    assert "150" in spec.model or "F-150" in spec.model

def test_year_model_pattern():
    """Test extraction with year pattern"""
    engine = IdentitySpecEngine()
    spec = engine.parse_text("2023 Camry recall")

    assert spec.model == "Camry"

def test_generic_product():
    """Test extraction of generic consumer product"""
    engine = IdentitySpecEngine()
    spec = engine.parse_text("Acme Baby Stroller model XL-2000")

    assert spec.brand == "Acme"
    assert spec.category == "consumer_product"

def test_raw_query_preserved():
    """Test that raw query is preserved for fuzzy search"""
    engine = IdentitySpecEngine()
    query = "Some Unknown Brand SuperModel 5000"
    spec = engine.parse_text(query)

    assert len(spec.source_artifacts) > 0
    assert spec.source_artifacts[0]["content"] == query
