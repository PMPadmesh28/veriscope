import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"backend"))
from ml.predict import predict_text
from services.risk_score import calculate_risk

def test_model_returns_valid_prediction():
    result=predict_text("Scientists publish a peer reviewed study in a major journal.")
    assert result["prediction"] in {"FAKE","REAL"}
    assert 0 <= result["confidence"] <= 1

def test_risk_bounds():
    result=calculate_risk("FAKE",0.91)
    assert 0 <= result["risk_score"] <= 100
    assert result["risk_level"] in {"LOW","MEDIUM","HIGH"}
