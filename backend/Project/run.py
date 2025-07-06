import uvicorn
from Project.Main import app

if __name__ == "__main__":
    print("Запуск сервера Employee Documents API...")
    print("Документация доступна по адресу: http://localhost:8000/docs")
    print("Альтернативная документация: http://localhost:8000/redoc")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )