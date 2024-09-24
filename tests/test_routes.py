import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_debt():
    response = client.post("/api/debts/", json={
        "debt_type": "owed_to",
        "person_name": "Asliddin",
        "amount": 100.0,
        "currency": "USD",
        "description": "Loan for business",
        "due_date": "2024-12-31T23:59:59"
    })
    assert response.status_code == 200
    assert response.json()["person_name"] == "Asliddin"

def test_read_debts():
    response = client.get("/api/debts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_settings():
    response = client.get("/api/settings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_monitoring_statistics():
    response = client.get("/api/monitoring/")
    assert response.status_code == 200
    assert "total_amount" in response.json()
    assert "total_debts" in response.json()
