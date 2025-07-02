FROM python:3.9-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код воркера
COPY . .

# Запускаем Celery-воркер
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
