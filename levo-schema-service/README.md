Run locally:


1. Create a venv and install dependencies:


python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


2. Start the API server:


uvicorn app.main:app --reload


3. Use the CLI to import a spec (in another terminal):


python cli.py import-spec --spec ./path/to/openapi.yaml --application my-app --service my-service


4. Run tests:


pytest -q




Notes:
- Schemas are persisted under `./schemas/{application}/{service?}/v{n}.(yaml|json)`
- The API validates OpenAPI specs using `openapi-spec-validator` before storing.