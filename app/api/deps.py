from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from typing import AsyncGenerator

from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.core.security import decode_access_token


oauth2_form = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генерация сессии базы данных на время запроса.
    """
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_user_repo(db: AsyncSession = Depends(get_session)) -> UserRepository:
    """
    Генерация репозитория пользователей.
    """

    return UserRepository(db)


def get_chat_repo(db: AsyncSession = Depends(get_session)) -> ChatMessageRepository:
    """
    Генерация репозитория сообщений чата.
    """

    return ChatMessageRepository(db)


def get_openrouter_client() -> OpenRouterClient:
    """
    Генерация клиента OpenRouter.
    """

    return OpenRouterClient()


def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) \
                     -> AuthUseCase:
    """
    Генерация usecase аутентификации.
    """
    
    return AuthUseCase(user_repo)


def get_chat_usecase(chat_repo: ChatMessageRepository = Depends(get_chat_repo),
                     openrouter_client: OpenRouterClient = \
                     Depends(get_openrouter_client)) -> ChatUseCase:
    """
    Генерация usecase чата.
    """
    
    return ChatUseCase(chat_repo, openrouter_client)


async def get_current_user_id(token: str = Depends(oauth2_form)) -> int:
    """
    Получение id пользователя по JWT-токену.
    """
    
    try:
        payload = decode_access_token(token)
        user_id = int(payload['sub'])
        return user_id
    except (JWTError, KeyError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Ошибка аутентификации',
                            headers={'WWW-Authenticate': 'Bearer'})
