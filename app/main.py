from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_credentials=True,
                       allow_methods=['*'],
                       allow_headers=['*'])

    @app.get('/health')
    async def check_health():
        return {'status': 'healthy',
                'environment': settings.env}

    return app


app = create_app()