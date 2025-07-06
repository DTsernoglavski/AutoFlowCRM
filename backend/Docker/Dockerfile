# Dockerfile
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY ../Project/requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY .. .

# Создание необходимых директорий
RUN mkdir -p templates output

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["python", "run.py"]





