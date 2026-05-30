"""Risk engine unit tests"""
import pytest
from app.services.risk_engine import RiskEngine


def test_risk_check_valid_candidate():
    """Test valid candidate passes checks"""
    engine = RiskEngine()
    candidate = {
        "asset_id": "test-asset",
        "conviction": 0.8,
        "thesis": "Test thesis",
    }
    
    is_valid, flags = engine.check_candidate(candidate)
    assert is_valid is True
    assert len(flags) == 0


def test_risk_check_low_confidence():
    """Test low confidence candidate fails"""
    engine = RiskEngine(min_confidence=0.7)
    candidate = {
        "asset_id": "test-asset",
        "conviction": 0.5,
        "thesis": "Test thesis",
    }
    
    is_valid, flags = engine.check_candidate(candidate)
    assert is_valid is False
    assert len(flags) > 0
    assert any("low_confidence" in f for f in flags)


def test_risk_check_missing_fields():
    """Test candidate with missing fields"""
    engine = RiskEngine()
    candidate = {
        "conviction": 0.8,
        # Missing asset_id and thesis
    }
    
    is_valid, flags = engine.check_candidate(candidate)
    assert is_valid is False
    assert "missing_asset_id" in flags
    assert "missing_thesis" in flags


def test_filter_candidates():
    """Test candidate filtering"""
    engine = RiskEngine(min_confidence=0.6, max_candidates=2)
    
    candidates = [
        {"asset_id": "a1", "conviction": 0.9, "thesis": "T1"},
        {"asset_id": "a2", "conviction": 0.8, "thesis": "T2"},
        {"asset_id": "a3", "conviction": 0.7, "thesis": "T3"},
        {"asset_id": "a4", "conviction": 0.5, "thesis": "T4"},  # Low confidence
    ]
    
    result = engine.filter_candidates(candidates)
    
    assert result["summary"]["total"] == 4
    assert result["summary"]["accepted_count"] == 2  # Limited by max_candidates
    assert result["summary"]["rejected_count"] == 1  # Low confidence one
    assert len(result["accepted"]) == 2
