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


oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_chat_repo(db: AsyncSession = Depends(get_db)) -> ChatMessageRepository:
    return ChatMessageRepository(db)


def get_llm_client() -> OpenRouterClient:
    return OpenRouterClient()


def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) \
                     -> AuthUseCase:
    return AuthUseCase(user_repo)


def get_chat_usecase(chat_repo: ChatMessageRepository = Depends(get_chat_repo),
                     llm_client: OpenRouterClient = Depends(get_llm_client)) \
                    -> ChatUseCase:
    return ChatUseCase(chat_repo, llm_client)


async def get_current_user_id(token: str = Depends(oauth2)) -> int:
    try:
        payload = decode_access_token(token)
        user_id = int(payload['sub'])
        return user_id
    except (JWTError, KeyError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Ошибка аутентификации',
                            headers={'WWW-Authenticate': 'Bearer'})
