# backend/tests/test_requests.py

"""
# Test cases for the install request API
TO run these tests, ensure the backend server is running:
# 1. Navigate to the backend directory:
    cd remoteuac/backend
    ./run.sh
# 2. Run the tests (in another terminal):
    python3 -m pytest tests/test_requests.py
"""

import requests
import json
from datetime import datetime, timedelta
from jose import jwt

BASE_URL = "http://localhost:8000/api"
SECRET_KEY = "I-Love-My-Girlfriend"
ALGORITHM = "HS256"

def get_admin_token():
    expire = datetime.utcnow() + timedelta(minutes=60)
    payload = {"sub": "admin_user", "exp": int(expire.timestamp())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def test_create_and_status_flow():
    payload = {
        "device_id": "TEST-DEVICE-01",
        "app_name": "example_installer.exe",
        "size": "15MB",
        "path": "C:/Users/Alice/Downloads",
        "download_source": "https://example.com/installer",
        "requested_changes": {"PATH": True, "Registry": ["HKLM\\Software\\Example"]},
        "timestamp": datetime.utcnow().isoformat()
    }
    # Create a new install request
    r = requests.post(f"{BASE_URL}/request", json=payload)
    assert r.status_code == 201
    result = r.json()
    req_id = result["id"]
    assert result["status"] == "pending"

    # Check status
    r2 = requests.get(f"{BASE_URL}/status/{req_id}")
    assert r2.status_code == 200
    result2 = r2.json()
    assert result2["id"] == req_id

    # Deny the request with admin token
    headers = {"Authorization": f"Bearer {get_admin_token()}"}
    r3 = requests.post(f"{BASE_URL}/approve/{req_id}?approve=false", headers=headers)
    assert r3.status_code == 200
    result3 = r3.json()
    assert result3["status"] == "denied"
