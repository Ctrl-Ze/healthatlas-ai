import pytest

from chiron.services.analysis_service import AnalysisService


@pytest.fixture
def service():
    return AnalysisService()


# ---------------------------
# Test empty input
# ---------------------------
def test_analyze_empty(service):
    result = service.analyze([])
    assert result["warnings"] == []
    assert result["facts"] == {"high": [], "low": [], "normal": []}
    assert result["analysis"]["abnormal_count"] == 0
    assert result["analysis"]["risk_level"] == "low"
    assert result["results"] == []


# ---------------------------
# Test normal value
# ---------------------------
def test_analyze_normal(service):
    tests = [
        {
            "analyte": "Glucose",
            "value": 90,
            "normal_low": 70,
            "normal_high": 100,
            "unit": "mg/dL",
        }
    ]
    result = service.analyze(tests)

    assert result["facts"]["normal"] == ["Glucose"]
    assert result["facts"]["low"] == []
    assert result["facts"]["high"] == []
    assert result["warnings"] == []
    assert result["analysis"]["abnormal_count"] == 0
    assert result["analysis"]["risk_level"] == "low"
    assert result["results"][0]["status"] == "normal"
    assert "within normal range" in result["results"][0]["interpretation"]


# ---------------------------
# Test low value
# ---------------------------
def test_analyze_low(service):
    tests = [
        {
            "analyte": "Hemoglobin",
            "value": 10,
            "normal_low": 12,
            "normal_high": 16,
            "unit": "g/dL",
        }
    ]
    result = service.analyze(tests)

    assert result["facts"]["low"] == ["Hemoglobin"]
    assert result["facts"]["normal"] == []
    assert result["facts"]["high"] == []
    assert len(result["warnings"]) == 1
    assert "below normal" in result["warnings"][0]
    assert result["analysis"]["abnormal_count"] == 1
    assert result["analysis"]["risk_level"] == "moderate"
    assert result["results"][0]["status"] == "low"


# ---------------------------
# Test high value
# ---------------------------
def test_analyze_high(service):
    tests = [
        {
            "analyte": "Cholesterol",
            "value": 250,
            "normal_low": 120,
            "normal_high": 200,
            "unit": "mg/dL",
        }
    ]
    result = service.analyze(tests)

    assert result["facts"]["high"] == ["Cholesterol"]
    assert result["facts"]["normal"] == []
    assert result["facts"]["low"] == []
    assert len(result["warnings"]) == 1
    assert "above normal" in result["warnings"][0]
    assert result["analysis"]["abnormal_count"] == 1
    assert result["analysis"]["risk_level"] == "moderate"
    assert result["results"][0]["status"] == "high"


# ---------------------------
# Test unknown status (missing value)
# ---------------------------
def test_analyze_unknown_value(service):
    tests = [
        {
            "analyte": "UnknownAnalyte",
            "value": None,
            "normal_low": 10,
            "normal_high": 20,
        }
    ]
    result = service.analyze(tests)

    # No low/high/normal since value is None
    assert result["facts"]["low"] == []
    assert result["facts"]["high"] == []
    assert result["facts"]["normal"] == []
    assert result["results"][0]["status"] == "unknown"
    assert "Unable to determine status" in result["results"][0]["interpretation"]


# ---------------------------
# Test multiple tests affecting risk level
# ---------------------------
def test_analyze_multiple_abnormal(service):
    tests = [
        {"analyte": "A1", "value": 5, "normal_low": 10, "normal_high": 20},  # low
        {"analyte": "A2", "value": 25, "normal_low": 10, "normal_high": 20},  # high
        {"analyte": "A3", "value": 15, "normal_low": 10, "normal_high": 20},  # normal
        {"analyte": "A4", "value": 8, "normal_low": 10, "normal_high": 20},  # low
    ]
    result = service.analyze(tests)

    assert set(result["facts"]["low"]) == {"A1", "A4"}
    assert result["facts"]["high"] == ["A2"]
    assert result["facts"]["normal"] == ["A3"]
    assert result["analysis"]["abnormal_count"] == 3
    assert result["analysis"]["risk_level"] == "elevated"
    assert len(result["warnings"]) == 3
