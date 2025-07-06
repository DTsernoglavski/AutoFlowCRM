from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from models import AdminForm, EmployeeForm, DocumentResponse
from docxtpl import DocxTemplate

from datetime import datetime
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Employee Documents API",
    description="API для создания документов сотрудников",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание директорий если они не существуют
TEMPLATES_DIR = Path("templates")
OUTPUT_DIR = Path("output")
TEMPLATES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Employee Documents API", "version": "1.0.0"}


@app.post("/api/documents/render/admin", response_model=DocumentResponse)
async def render_admin_document(form_data: AdminForm):
    """
    Создает документ на основе данных админской анкеты
    """
    try:
        # Путь к шаблону
        template_path = TEMPLATES_DIR / "admin_template.docx"

        if not template_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Шаблон админской анкеты не найден. Загрузите admin_template.docx в папку templates/"
            )

        # Загрузка шаблона
        doc = DocxTemplate(template_path)

        # Подготовка данных для шаблона
        context = {
            'user_name': form_data.user_name,
            'email_address': form_data.email_address,
            'gender': form_data.gender.value,
            'phone_number': form_data.phone_number,
            'employment_type': form_data.employment_type.value,
            'contract_role': form_data.contract_role,
            'starting_date': form_data.starting_date.strftime('%d.%m.%Y'),
            'salary_before_tax': f"{form_data.salary_before_tax:,.2f}",
            'current_date': datetime.now().strftime('%d.%m.%Y')
        }

        # Заполнение шаблона
        doc.render(context)

        # Сохранение результата
        output_filename = f"admin_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        output_path = OUTPUT_DIR / output_filename
        doc.save(output_path)

        logger.info(f"Админский документ создан: {output_filename}")

        return DocumentResponse(
            status="ok",
            message="Документ успешно создан",
            filename=output_filename
        )

    except Exception as e:
        logger.error(f"Ошибка при создании админского документа: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при создании документа: {str(e)}")


@app.post("/api/documents/render/employee", response_model=DocumentResponse)
async def render_employee_document(form_data: EmployeeForm):
    """
    Создает документ на основе данных анкеты работника
    """
    try:
        # Путь к шаблону
        template_path = TEMPLATES_DIR / "employee_template.docx"

        if not template_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Шаблон анкеты работника не найден. Загрузите employee_template.docx в папку templates/"
            )

        # Загрузка шаблона
        doc = DocxTemplate(template_path)

        # Подготовка данных для шаблона
        context = {
            # Личные данные
            'first_name': form_data.personal_details.first_name,
            'last_name': form_data.personal_details.last_name,
            'user_name': form_data.personal_details.user_name,
            'id_number_passport': form_data.personal_details.id_number_passport,
            'date_of_birth': form_data.personal_details.date_of_birth.strftime('%d.%m.%Y'),
            'city': form_data.personal_details.city,
            'address': form_data.personal_details.address,
            'apartment_number': form_data.personal_details.apartment_number or 'Не указано',
            'phone_number': form_data.personal_details.phone_number,

            # Информация о трудоустройстве
            'contract_role': form_data.employment_info.contract_role,
            'employment_type': form_data.employment_info.employment_type.value,
            'starting_date': form_data.employment_info.starting_date.strftime('%d.%m.%Y'),
            'salary_before_tax': f"{form_data.employment_info.salary_before_tax:,.2f}",

            # Банковские данные
            'select_region': form_data.bank_details.select_region,
            'name_clarification': form_data.bank_details.name_clarification,
            'bank_name': form_data.bank_details.bank_name,
            'swift': form_data.bank_details.swift,
            'iban': form_data.bank_details.iban,
            'payer_agreement_id': form_data.bank_details.payer_agreement_id,
            'country_code': form_data.bank_details.country_code,

            # Дополнительная информация
            'current_date': datetime.now().strftime('%d.%m.%Y')
        }

        # Заполнение шаблона
        doc.render(context)

        # Сохранение результата
        output_filename = f"employee_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        output_path = OUTPUT_DIR / output_filename
        doc.save(output_path)

        logger.info(f"Документ работника создан: {output_filename}")

        return DocumentResponse(
            status="ok",
            message="Документ успешно создан",
            filename=output_filename
        )

    except Exception as e:
        logger.error(f"Ошибка при создании документа работника: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при создании документа: {str(e)}")


@app.get("/api/documents/download/{filename}")
async def download_document(filename: str):
    """
    Скачивание созданного документа
    """
    file_path = OUTPUT_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )


@app.post("/api/templates/upload/{template_type}")
async def upload_template(template_type: str, file: UploadFile = File(...)):
    """
    Загрузка шаблона документа
    template_type: 'admin' или 'employee'
    """
    if template_type not in ['admin', 'employee']:
        raise HTTPException(status_code=400, detail="Тип шаблона должен быть 'admin' или 'employee'")

    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате .docx")

    try:
        template_filename = f"{template_type}_template.docx"
        template_path = TEMPLATES_DIR / template_filename

        # Сохранение файла
        content = await file.read()
        with open(template_path, "wb") as f:
            f.write(content)

        logger.info(f"Шаблон загружен: {template_filename}")

        return {"status": "ok", "message": f"Шаблон {template_type} успешно загружен"}

    except Exception as e:
        logger.error(f"Ошибка при загрузке шаблона: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке шаблона: {str(e)}")


@app.get("/api/health")
async def health_check():
    """
    Проверка состояния сервиса
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "templates_available": {
            "admin": (TEMPLATES_DIR / "admin_template.docx").exists(),
            "employee": (TEMPLATES_DIR / "employee_template.docx").exists()
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)