import os
import requests
from requests.auth import HTTPBasicAuth
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery import Celery

FRAPPE_URL = os.getenv("FRAPPE_URL")
FRAPPE_USER = os.getenv("FRAPPE_USER")
FRAPPE_PASSWORD = os.getenv("FRAPPE_PASSWORD")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("tasks", broker=REDIS_URL)
CRM_AUTH = HTTPBasicAuth(FRAPPE_USER, FRAPPE_PASSWORD)

app = FastAPI()

class DocumentData(BaseModel):
    first_name: str
    birth_date: str
    citizenship: str
    profession: str
    signature: str  # base64 PNG data URI

@app.post("/api/documents/render")
def render_document(data: DocumentData):
    # 1. Сохранить в CRM
    crm_payload = data.dict()
    resp = requests.post(
        f"{FRAPPE_URL}/api/resource/EmployeeData",
        json=crm_payload,
        auth=CRM_AUTH,
        timeout=5,
    )
    if resp.status_code >= 400:
        raise HTTPException(502, f"CRM error: {resp.text}")
    # 2. Передать задачу в Celery
    task = celery_app.send_task("tasks.generate_and_upload", args=[crm_payload])
    return {"status": "queued", "task_id": task.id}
