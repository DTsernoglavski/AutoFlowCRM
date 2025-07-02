import os
import base64
import io
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from docxtpl import DocxTemplate
from PIL import Image

REDIS_URL = os.getenv("REDIS_URL")
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

app = FastAPI()

class FormData(BaseModel):
    first_name: str
    birth_date: str
    citizenship: str
    profession: str
    signature: str

@app.post("/api/documents/render")
async def render(data: FormData):
    # Простейшая валидация
    if not data.first_name.isascii():
        raise HTTPException(400, "Имя должно быть латиницей")
    # рендерим шаблон
    tpl = DocxTemplate("template.docx")          # файл-шаблон должен лежать в этой папке
    context = data.dict()
    # раскодируем подпись
    img_bytes = base64.b64decode(context["signature"].split(",")[1])
    img = Image.open(io.BytesIO(img_bytes))
    # вставка подписи в шаблон (пример, зависит от шаблона)
    tpl.render(context)
    output_path = "output.docx"
    tpl.save(output_path)
    return {"status": "ok", "path": output_path}
