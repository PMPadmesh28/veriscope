import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"backend"))
from app import app

def test_health():
    client=app.test_client()
    response=client.get("/api/health")
    assert response.status_code==200
    assert response.get_json()["status"]=="ok"

def test_analyze_text():
    client=app.test_client()
    response=client.post("/api/analyze",data={"text":"A university publishes a new research report."})
    assert response.status_code==200
    data=response.get_json()
    assert "prediction" in data
    assert "risk_score" in data
    assert "summary" in data
