from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_seance_rejette_duree_negative():
    response = client.post("/seance", json={
        "user_id": "test",
        "sport": "course",
        "duree_min": -5,
        "ressenti": "fatigue"
    })
    assert response.status_code == 422

def test_seance_rejette_champ_manquant():
    response = client.post("/seance", json={
        "user_id": "test",
        "sport": "course",
        "duree_min": 30
    })
    assert response.status_code == 422

def test_seance_complete():
    response = client.post("/seance", json={
        "user_id": "test",
        "sport": "course",
        "duree_min": 30,
        "ressenti": "fatigue"
    })
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "ton" in data
    assert "signaux_faibles" in data
    assert "session_count" in data
    assert data["ton"] in ["chaleureux", "motivant", "doux", "alerte"]