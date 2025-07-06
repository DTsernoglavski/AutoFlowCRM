# Employee Documents API

API для создания документов сотрудников на основе шаблонов Word.

## Установка и запуск

### 1. Подготовка окружения

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Структура проекта

```
project/
├── Main.py                 # Основное приложение FastAPI
├── models.py               # Модели данных
├── run.py                  # Скрипт запуска сервера
├── requirements.txt        # Зависимости
├── examples.json           # Примеры данных
├── templates/              # Шаблоны документов - Этого пока что нет
│   ├── admin_template.docx
│   └── employee_template.docx
└── output/                 # Созданные документы
```

### 3. Запуск сервера

```bash
python run.py
```

Сервер будет доступен по адресу: `http://localhost:8000`

## API Endpoints

### Основные маршруты

- **GET** `/` - Информация о API
- **GET** `/docs` - Swagger документация
- **GET** `/redoc` - Альтернативная документация
- **GET** `/api/health` - Проверка состояния сервиса

### Создание документов

#### 1. Админская анкета
- **POST** `/api/documents/render/admin`
- Создает документ на основе данных админской анкеты

Пример запроса:
```json
{
  "user_name": "ivan_petrov",
  "email_address": "ivan.petrov@company.com",
  "gender": "male",
  "phone_number": "+7 999 123-45-67",
  "employment_type": "full_time",
  "contract_role": "Senior Developer",
  "starting_date": "2024-01-15",
  "salary_before_tax": 150000.00
}
```

#### 2. Анкета работника
- **POST** `/api/documents/render/employee`
- Создает документ на основе полной анкеты работника

Пример запроса:
```json
{
  "personal_details": {
    "first_name": "Иван",
    "last_name": "Петров",
    "user_name": "ivan_petrov",
    "id_number_passport": "1234 567890",
    "date_of_birth": "1990-05-15",
    "city": "Москва",
    "address": "ул. Тверская, д. 1",
    "apartment_number": "25",
    "phone_number": "+7 999 123-45-67"
  },
  "employment_info": {
    "contract_role": "Senior Developer",
    "employment_type": "full_time",
    "starting_date": "2024-01-15",
    "salary_before_tax": 150000.00
  },
  "bank_details": {
    "select_region": "Москва",
    "name_clarification": "Иван Петров",
    "bank_name": "Сбербанк",
    "swift": "SABRRUMM",
    "iban": "RU1234567890123456789012",
    "payer_agreement_id": "PAY123456789",
    "country_code": "RU"
  }
}
```

### Управление шаблонами

- **POST** `/api/templates/upload/{template_type}` - Загрузка шаблона
  - `template_type`: "admin" или "employee"
  - Файл: .docx формат

### Скачивание документов

- **GET** `/api/documents/download/{filename}` - Скачивание созданного документа

## Создание шаблонов Word

### Для админской анкеты (admin_template.docx)

В документе Word используйте следующие переменные:
- `{{ user_name }}` - Имя пользователя
- `{{ email_address }}` - Email адрес
- `{{ gender }}` - Пол
- `{{ phone_number }}` - Номер телефона
- `{{ employment_type }}` - Тип трудоустройства
- `{{ contract_role }}` - Должность
- `{{ starting_date }}` - Дата начала работы
- `{{ salary_before_tax }}` - Зарплата до налогов
- `{{ current_date }}` - Текущая дата

### Для анкеты работника (employee_template.docx)

Используйте следующие переменные:

**Личные данные:**
- `{{ first_name }}` - Имя
- `{{ last_name }}` - Фамилия
- `{{ user_name }}` - Имя пользователя
- `{{ id_number_passport }}` - Номер паспорта/ID
- `{{ date_of_birth }}` - Дата рождения
- `{{ city }}` - Город
- `{{ address }}` - Адрес
- `{{ apartment_number }}` - Номер квартиры
- `{{ phone_number }}` - Номер телефона

**Информация о трудоустройстве:**
- `{{ contract_role }}` - Должность
- `{{ employment_type }}` - Тип трудоустройства
- `{{ starting_date }}` - Дата начала работы
- `{{ salary_before_tax }}` - Зарплата до налогов

**Банковские данные:**
- `{{ select_region }}` - Регион
- `{{ name_clarification }}` - Уточнение имени
- `{{ bank_name }}` - Название банка
- `{{ swift }}` - SWIFT код
- `{{ iban }}` - IBAN
- `{{ payer_agreement_id }}` - ID соглашения плательщика
- `{{ country_code }}` - Код страны

**Дополнительно:**
- `{{ current_date }}` - Текущая дата

## Типы данных

### Gender (Пол)
- `male` - Мужской
- `female` - Женский
- `other` - Другой

### Employment Type (Тип трудоустройства)
- `full_time` - Полный рабочий день
- `part_time` - Неполный рабочий день
- `contract` - Контракт
- `internship` - Стажировка

## Тестирование

### Curl примеры

```bash
# Создание админского документа
curl -X POST "http://localhost:8000/api/documents/render/admin" \
  -H "Content-Type: application/json" \
  -d @admin_example.json

# Создание документа работника
curl -X POST "http://localhost:8000/api/documents/render/employee" \
  -H "Content-Type: application/json" \
  -d @employee_example.json
```

### Ответы API

Успешный ответ:
```json
{
  "status": "ok",
  "message": "Документ успешно создан",
  "filename": "admin_output_20240115_143022.docx"
}
```

Ошибка:
```json
{
  "detail": "Описание ошибки"
}
```

## Обработка ошибок

API возвращает следующие коды ошибок:
- `400` - Неверные данные запроса
- `404` - Шаблон не найден
- `422` - Ошибка валидации данных
- `500` - Внутренняя ошибка сервера

## Логирование

Все операции логируются в консоль с информацией о:
- Создании документов
- Загрузке шаблонов
- Ошибках обработки