from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

SIMPLE_OPENAPI_JSON = b"""
{
  "openapi": "3.0.0",
  "info": {"title": "test", "version": "1.0.0"},
  "paths": {}
}
"""


def test_upload_app_schema():
    files = {"file": ("openapi.json", io.BytesIO(SIMPLE_OPENAPI_JSON), "application/json")}
    data = {"application": "test-app"}
    r = client.post("/upload", data=data, files=files)
    assert r.status_code == 200
    body = r.json()
    assert body["application"] == "test-app"
    assert body["version"] == 1
