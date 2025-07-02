FROM python:3.9-slim

WORKDIR /app

# копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем код и шаблоны
COPY . .

# открываем порт и запускаем FastAPI
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
