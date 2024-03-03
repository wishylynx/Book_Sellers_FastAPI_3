from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.configurations.database import create_db_and_tables, delete_db_and_tables, global_init
from src.routers import v1_router

from dotenv import load_dotenv
import os

from src.routers.v1.sellers import sellers_router


dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
print(f"Loaded DB_HOST from .env: {os.getenv('DB_HOST')}")
print(f"Loaded DB_NAME from .env: {os.getenv('DB_NAME')}")


@asynccontextmanager
async def lifespan(app: FastAPI):  # Рекомендуется теперь вместо @app.on_event()
    # Запускается при старте приложения
    global_init()
    await create_db_and_tables()
    yield
    # Убрал удаление базы данных
    # await delete_db_and_tables()


# Само приложение fastApi. именно оно запускается сервером и служит точкой входа
# в нем можно указать разные параметры для сваггера и для ручек (эндпоинтов).
def create_application():
    return FastAPI(
        title="Book Library App",
        description="Учебное приложение для группы MTS Shad",
        version="0.0.1",
        responses={404: {"description": "Not Found!"}},
        default_response_class=ORJSONResponse,  # Подключаем быстрый сериализатор,
        lifespan=lifespan,
    )


app = create_application()


def _configure():
    app.include_router(v1_router)
    app.include_router(sellers_router, prefix="/api/v1/seller", tags=["sellers"])


# @app.on_event("startup")  # Вместо этого теперь рекомендуется lifespan
# async def startup_event():
#     global_init()
#     await create_db_and_tables()


_configure()
