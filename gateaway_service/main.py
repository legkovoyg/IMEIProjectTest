import requests
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi

# URLs других сервисов
DB_SERVICE_URL = "http://db_service:8002"
API_SERVICE_URL = "http://api_service:8001"
TG_SERVICE_URL = "http://tg_service:8003"

app = FastAPI(title="IMEI Project API Gateway", docs_url="/docs")

# === DB SERVICE ===
@app.post("/users/check")
def check_user(token: str):
    response = requests.post(f"{DB_SERVICE_URL}/users/check", json={"token": token})
    return response.json()

@app.post("/users/add")
def add_user(username: str, token: str):
    response = requests.post(f"{DB_SERVICE_URL}/users/add", json={"username": username, "token": token})
    return response.json()

@app.post("/telegram-whitelist/check")
def check_tg_user(telegram_id: str):
    response = requests.post(f"{DB_SERVICE_URL}/telegram-whitelist/check", json={"telegram_id": telegram_id})
    return response.json()

@app.post("/telegram-whitelist/add")
def add_tg_user(telegram_id: str, username: str):
    response = requests.post(f"{DB_SERVICE_URL}/telegram-whitelist/add", json={"telegram_id": telegram_id, "username": username})
    return response.json()

# === API SERVICE (IMEI CHECK) ===
@app.post("/api/check-imei")
def check_imei(imei: str):
    response = requests.post(f"{API_SERVICE_URL}/api/check-imei", json={"imei": imei})
    return response.json()


# === OpenAPI Schema Aggregation ===
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="IMEI Gateway API",
        version="1.0.0",
        description="Gateway объединяет API всех сервисов",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
