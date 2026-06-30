from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.routes_auth import auth_router
from app.api.routes_chat import chat_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Создание таблицы при запуске приложения и освобождение ресурсов при его завершении.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    """
    Создание экземпляра FastAPI с настроенными middleware, health-check и роутерами.
    """

    app = FastAPI(title=settings.app_name,
                  lifespan=lifespan)
    
    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_credentials=True,
                       allow_methods=['*'],
                       allow_headers=['*'])
    
    @app.get('/health')
    async def check_health():
        return {'status': 'healthy',
                'environment': settings.env}
    
    app.include_router(auth_router, prefix='/auth', tags=['auth'])
    app.include_router(chat_router, prefix='/chat', tags=['chat'])
    
    return app


app = create_app()
