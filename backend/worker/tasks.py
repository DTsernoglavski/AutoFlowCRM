import os
import base64
import io
from celery import Celery
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from PIL import Image
import dropbox

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

celery_app = Celery("tasks", broker=REDIS_URL)

@celery_app.task(name="tasks.generate_and_upload")
def generate_and_upload(payload):
    # 1. Рендер docx
    tpl = DocxTemplate("employee_template.docx")
    # 2. Вставка подписи как картинки
    sig_data = payload.get("signature", "")
    if sig_data.startswith("data:image/png;base64,"):
        sig_data = sig_data.replace("data:image/png;base64,", "")
    img_bytes = base64.b64decode(sig_data)
    image = Image.open(io.BytesIO(img_bytes))
    image.save("signature.png")
    signature_img = InlineImage(tpl, "signature.png", width=Mm(40))
    context = {**payload, "signature": signature_img}
    tpl.render(context)
    tpl.save("output.docx")
    # 3. Загрузка в Dropbox
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    with open("output.docx", "rb") as f:
        dbx.files_upload(f.read(), "/output.docx", mode=dropbox.files.WriteMode.overwrite)
    return {"uploaded": "/output.docx"}
