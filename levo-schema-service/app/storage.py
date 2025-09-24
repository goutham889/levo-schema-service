import os
from typing import Optional, Tuple
from app.models import Application, Service, SchemaRecord
from app.db import get_session
from sqlmodel import select

STORAGE_DIR = "stored_schemas"

def _service_dir(app_name: str, service_name: Optional[str]) -> str:
    dir_path = os.path.join(STORAGE_DIR, app_name)
    if service_name:
        dir_path = os.path.join(dir_path, service_name)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def get_next_version(app_name: str, service_name: Optional[str]) -> int:
    session = get_session()
    stmt = select(SchemaRecord).where(SchemaRecord.application_id == _get_app_id(session, app_name))
    if service_name:
        stmt = stmt.where(SchemaRecord.service_id == _get_service_id(session, app_name, service_name))
    rows = session.exec(stmt).all()
    if not rows:
        return 1
    return max(r.version for r in rows) + 1

def _get_app_id(session, app_name: str) -> int:
    app = session.exec(select(Application).where(Application.name == app_name)).first()
    if not app:
        from app.models import Application
        app = Application(name=app_name)
        session.add(app); session.commit(); session.refresh(app)
    return app.id

def _get_service_id(session, app_name: str, service_name: str) -> int:
    app_id = _get_app_id(session, app_name)
    svc = session.exec(select(Service).where(Service.name == service_name, Service.application_id == app_id)).first()
    if not svc:
        from app.models import Service
        svc = Service(name=service_name, application_id=app_id)
        session.add(svc); session.commit(); session.refresh(svc)
    return svc.id

def persist_schema_file(app_name: str, service_name: Optional[str], file_bytes: bytes, original_filename: str) -> Tuple[int, str]:
    session = get_session()
    app_id = _get_app_id(session, app_name)
    service_id = _get_service_id(session, app_name, service_name) if service_name else None
    version = get_next_version(app_name, service_name)
    ext = os.path.splitext(original_filename)[1] or ".yaml"
    filename = f"v{version}{ext}"
    target_dir = _service_dir(app_name, service_name)
    target_path = os.path.join(target_dir, filename)
    with open(target_path, "wb") as f:
        f.write(file_bytes)
    record = SchemaRecord(application_id=app_id, service_id=service_id, version=version, filename=target_path)
    session.add(record); session.commit(); session.refresh(record)
    return version, target_path

def list_versions(app_name: str, service_name: Optional[str]):
    session = get_session()
    app = session.exec(select(Application).where(Application.name == app_name)).first()
    if not app:
        return []
    stmt = select(SchemaRecord).where(SchemaRecord.application_id == app.id)
    if service_name:
        svc = session.exec(select(Service).where(Service.name == service_name, Service.application_id == app.id)).first()
        if not svc:
            return []
        stmt = stmt.where(SchemaRecord.service_id == svc.id)
    return session.exec(stmt.order_by(SchemaRecord.version)).all()

def get_schema_by_version(app_name: str, service_name: Optional[str], version: Optional[int] = None) -> Optional[SchemaRecord]:
    rows = list_versions(app_name, service_name)
    if not rows:
        return None
    if version is None:
        return max(rows, key=lambda r: r.version)
    for r in rows:
        if r.version == version:
            return r
    return None
