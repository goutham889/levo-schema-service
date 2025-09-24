import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import Optional

# Dummy imports to make it run
try:
    from app.db import init_db, get_session
    from app.storage import persist_schema_file, list_versions, get_schema_by_version
    from app.validator import validate_openapi
except ModuleNotFoundError:
    # Minimal dummy functions if files not ready
    def init_db(): pass
    def get_session(): return None
    def persist_schema_file(app_name, service_name, content, filename): return 1, "fake_path.yaml"
    def list_versions(app_name, service_name=None): return []
    def get_schema_by_version(app_name, service_name=None, version=None): return None
    def validate_openapi(content): return True, "OK"

app = FastAPI(title="Levo Schema Service")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

# Optional: add /upload endpoint if you want to test uploads
import logging

@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    application: str = Form(...),
    service: Optional[str] = Form(None)
):
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Received file: {file.filename}, application: {application}, service: {service}")

    contents = await file.read()
    logging.info(f"File size: {len(contents)} bytes")

    # Validate OpenAPI spec
    try:
        ok, msg = validate_openapi(contents)
        if not ok:
            return {"error": msg}
    except Exception as e:
        logging.exception("Validation failed")
        raise HTTPException(status_code=400, detail=str(e))

    # TODO: Save to DB / filesystem
    return {"application": application, "service": service, "filename": file.filename}
