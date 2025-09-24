import typer
import requests
from pathlib import Path

app = typer.Typer()

API_URL = "http://127.0.0.1:8000"


@app.command()
def import_spec(spec: str, application: str, service: str = None):
    """Simulate: levo import --spec /path/to/openapi.yaml --application app-name [--service service-name]"""
    p = Path(spec)
    if not p.exists():
        raise typer.Exit(code=1)

    files = {"file": (p.name, open(p, "rb"))}
    data = {"application": application}
    if service:
        data["service"] = service

    r = requests.post(f"{API_URL}/upload", data=data, files=files)
    print(r.status_code, r.text)


if __name__ == "__main__":
    app()
