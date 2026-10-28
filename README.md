# Real-Time ML Inference REST API & Capstone

A containerized FastAPI microservice that loads a trained binary-classification model and serves real-time predictions with class probabilities. It includes a Dockerfile, input validation, automated tests, and interactive API documentation.

> **Important:** This repository ships with a model trained on **synthetic demo data** so the service can run immediately. It is a portfolio/capstone template, not a validated model for real-world decisions. Replace the demo training data and evaluate the model before production use.

## Features

- `POST /predict` returns a class prediction and probability for each class.
- `GET /health` provides a health check.
- Pydantic request/response schemas and explicit feature validation.
- Model and feature names loaded from versionable artifacts.
- Docker image runs as a non-root user and includes a health check.
- Unit/API tests for success cases, schema, and error responses.
- OpenAPI documentation served automatically by FastAPI.

## Repository layout

```text
real-time-ml-inference-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── schemas.py
├── models/
│   ├── champion_model.joblib
│   └── feature_names.json
├── tests/
│   └── test_api.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── train_model.py
└── README.md
```

## Architecture

```text
Client / Consumer
      |
      | POST /predict (JSON)
      v
FastAPI + Pydantic validation
      |
      | Validate exact feature names and finite numeric values
      v
Preprocessing + Logistic Regression pipeline
      |
      | predict() and predict_proba()
      v
JSON response: prediction + probabilities + model_version
```

**Request lifecycle:** The service loads the serialized scikit-learn pipeline once when the application starts. Each request is validated, reordered to the model's expected feature order, passed to the model, and returned as JSON. Invalid feature sets return HTTP `422`.

## Requirements

- Python 3.11 recommended
- pip
- Docker (optional, for container execution)

## Run locally

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2. Install pinned dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the API

The repository includes a trained demo model. To regenerate it reproducibly:

```bash
python train_model.py
```

Then run:

```bash
uvicorn app.main:app --reload
```

Open the interactive docs at `http://127.0.0.1:8000/docs`; OpenAPI JSON is at `http://127.0.0.1:8000/openapi.json`.

## API documentation

### `GET /health`

Success (`200 OK`):

```json
{
  "status": "ok",
  "model_version": "1.0.0"
}
```

### `POST /predict`

Content-Type: `application/json`

The payload must contain exactly these six numeric features: `feature_1` through `feature_6`. Feature order in the JSON does not matter; the service orders them to match the model.

Example request:

```json
{
  "features": {
    "feature_1": 0.2,
    "feature_2": -1.1,
    "feature_3": 1.4,
    "feature_4": 0.7,
    "feature_5": -0.3,
    "feature_6": 0.9
  }
}
```

Example response (values are illustrative; run the endpoint to obtain the actual output):

```json
{
  "prediction": 1,
  "probabilities": {
    "0": 0.184,
    "1": 0.816
  },
  "model_version": "1.0.0"
}
```

- `prediction`: predicted class (`0` or `1`).
- `probabilities`: model probability for each class; values should sum to approximately `1`.
- `model_version`: service/model version, configurable with the `MODEL_VERSION` environment variable.

Error responses:
- `422 Unprocessable Entity`: malformed request, missing/unknown feature, or non-finite feature value.
- `500 Internal Server Error`: prediction failure after validation. The response intentionally avoids returning internal exception details.

### Example with curl

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "feature_1": 0.2,
      "feature_2": -1.1,
      "feature_3": 1.4,
      "feature_4": 0.7,
      "feature_5": -0.3,
      "feature_6": 0.9
    }
  }'
```

Windows PowerShell users can run the request from `/docs` if shell quoting causes issues.

## Run tests

```bash
pytest -v
```

The test suite checks the health endpoint, successful prediction schema, missing and unknown features, and malformed payloads.

## Build and run with Docker

Build the image:

```bash
docker build -t realtime-ml-inference:1.0.0 .
```

Run the container:

```bash
docker run --rm -p 8000:8000 realtime-ml-inference:1.0.0
```

Then visit `http://127.0.0.1:8000/docs` or check `http://127.0.0.1:8000/health`.

Override the displayed model version if needed:

```bash
docker run --rm -p 8000:8000 -e MODEL_VERSION=1.0.1 realtime-ml-inference:1.0.0
```

## Production hardening checklist

Before using this pattern for a real model:

- Train on approved, representative data and document the target and feature definitions.
- Evaluate with a holdout set; record metrics, threshold choice, calibration, and known limitations.
- Pin and scan dependencies; rebuild images regularly.
- Add authentication/authorization, TLS at the ingress, rate limits, request-size limits, and monitoring.
- Log request IDs, latency, error rates, and model version; do not log sensitive raw inputs.
- Add model/data versioning, rollback, drift checks, and a retraining process.
- Store secrets outside source control and define retention/access policies.
- Load-test and deploy behind a production ASGI/server infrastructure appropriate to the environment.

## Certification submission checklist

- [x] Model artifact included
- [x] FastAPI `/predict` endpoint with probabilities
- [x] Dockerfile with pinned dependencies
- [x] Automated API tests
- [x] API documentation and architecture in this README
- [ ] Run `pytest -v` successfully in your own environment
- [ ] Build and smoke-test the Docker image
- [ ] Replace synthetic demo data if the capstone requires a domain-specific champion model

## Suggested GitHub repository description

`Production-style FastAPI microservice for real-time ML inference with prediction probabilities, input validation, Docker, tests, and OpenAPI documentation.`

## Suggested GitHub caption

Built a **Real-Time ML Inference REST API** using FastAPI and scikit-learn. The project packages a trained demo model behind a validated `/predict` endpoint, returns class probabilities, includes automated API tests, and runs in a Docker container. I also documented the architecture, request/response schemas, setup, and deployment workflow.

#MachineLearning #FastAPI #MLOps #Docker #Python #RESTAPI
