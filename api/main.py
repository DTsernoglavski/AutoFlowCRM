import os
import base64
import io

import requests
from requests.auth import HTTPBasicAuth
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from tasks import generate_and_upload  # ваш Celery-таск

app = FastAPI()

# Параметры CRM из .env
FRAPPE_URL = os.getenv("FRAPPE_URL", "http://frappe:8000")
FRAPPE_USER = os.getenv("FRAPPE_USER", "Administrator")
FRAPPE_PWD = os.getenv("FRAPPE_PASSWORD", "admin123")
CRM_AUTH = HTTPBasicAuth(FRAPPE_USER, FRAPPE_PWD)

# Модели запросов

class DocumentData(BaseModel):
    first_name: str = Field(..., description="Имя, латиницей")
    birth_date: str = Field(..., description="Дата рождения, YYYY-MM-DD")
    citizenship: str
    profession: str
    signature: str = Field(
        ..., description="Base64 PNG data URI, e.g. data:image/png;base64,...."
    )

class LeadData(BaseModel):
    lead_name: str
    email_id: str
    mobile_no: str
    company: str

# Эндпоинт для рендера документов и Dropbox

@app.post("/api/documents/render")
async def render_document(data: DocumentData):
    # Валидация
    if not data.first_name.isascii():
        raise HTTPException(400, "Имя должно быть латиницей")

    # Создать запись в CRM (DocType EmployeeData)
    crm_payload = data.dict()
    crm_resp = requests.post(
        f"{FRAPPE_URL}/api/resource/EmployeeData",
        json=crm_payload,
        auth=CRM_AUTH,
        timeout=5,
    )
    if crm_resp.status_code >= 400:
        raise HTTPException(502, f"CRM error: {crm_resp.text}")

    # Отправить задачу рендера в Celery
    task = generate_and_upload.delay(data.dict())
    return {"status": "queued", "task_id": task.id}

# Эндпоинт для создания лида в CRM

@app.post("/api/crm/lead")
async def create_lead(lead: LeadData):
    url = f"{FRAPPE_URL}/api/resource/Lead"
    payload = lead.dict()
    resp = requests.post(url, json=payload, auth=CRM_AUTH, timeout=5)
    if not resp.ok:
        raise HTTPException(502, f"CRM error ({resp.status_code}): {resp.text}")
    return resp.json()


# Тестовый корневой эндпоинт
@app.get("/")
async def root():
    return {"message": "AutoFlowCRM API is up and running"} 
