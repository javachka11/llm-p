from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings


engine = create_async_engine(url=f'sqlite+aiosqlite:///{settings.sqlite_path}')

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
