import pytest
import sys
import os
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

def test_register():
    response = client.post("/api/register/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login():
    # Avval ro'yxatdan o'tish
    client.post("/api/register/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123"
    })

    # Tizimga kirish
    response = client.post("/api/login/", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged in"

def test_login_invalid_credentials():
    response = client.post("/api/login/", json={
        "username": "wronguser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "parol yoki username notogri"
