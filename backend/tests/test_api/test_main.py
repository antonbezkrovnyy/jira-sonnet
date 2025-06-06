from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    # Act
    response = client.get("/health")
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}