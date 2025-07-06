from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"

# Модель для админской анкеты
class AdminForm(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=100)
    email_address: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    gender: Gender
    phone_number: str = Field(..., min_length=10, max_length=20)
    employment_type: EmploymentType
    contract_role: str = Field(..., min_length=2, max_length=100)
    starting_date: date
    salary_before_tax: float = Field(..., gt=0)

# Модель для личных данных работника
class EmployeePersonalDetails(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    user_name: str = Field(..., min_length=2, max_length=100)
    id_number_passport: str = Field(..., min_length=5, max_length=50)
    date_of_birth: date
    city: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=200)
    apartment_number: Optional[str] = Field(None, max_length=20)
    phone_number: str = Field(..., min_length=10, max_length=20)

# Модель для информации о трудоустройстве
class EmploymentInfo(BaseModel):
    contract_role: str = Field(..., min_length=2, max_length=100)
    employment_type: EmploymentType
    starting_date: date
    salary_before_tax: float = Field(..., gt=0)

# Модель для банковских данных
class BankDetails(BaseModel):
    select_region: str = Field(..., min_length=2, max_length=100)
    name_clarification: str = Field(..., min_length=2, max_length=100)
    bank_name: str = Field(..., min_length=2, max_length=100)
    swift: str = Field(..., min_length=8, max_length=11)
    iban: str = Field(..., min_length=15, max_length=34)
    payer_agreement_id: str = Field(..., min_length=5, max_length=50)
    country_code: str = Field(..., min_length=2, max_length=3)

# Полная модель анкеты работника
class EmployeeForm(BaseModel):
    personal_details: EmployeePersonalDetails
    employment_info: EmploymentInfo
    bank_details: BankDetails

# Модель ответа
class DocumentResponse(BaseModel):
    status: str = "ok"
    message: Optional[str] = None
    filename: Optional[str] = None