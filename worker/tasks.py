import os
from celery import Celery
import dropbox

# Берём настройки из окружения
REDIS_URL     = os.getenv("REDIS_URL", "redis://redis:6379/0")
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

app = Celery("tasks", broker=REDIS_URL)

@app.task
def upload_to_dropbox(file_path: str, dropbox_path: str):
    """
    Загружает локальный файл output.docx в папку в вашем Dropbox.
    """
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    with open(file_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path)
    return {"uploaded": dropbox_path}
