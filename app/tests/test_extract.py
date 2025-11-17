from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_extract_sync_ok():
    payload = {
        "query": "invoice total and currency",
        "fields": ["invoice_no", "total_amount", "currency", "date"],
    }
    resp = client.post("/api/extract", json=payload)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["data"]["invoice_no"] == "INV-001"
    assert body["data"]["currency"] == "EUR"