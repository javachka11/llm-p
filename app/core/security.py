import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Any

from app.core.config import settings


def hash_password(password: str) -> str:
    """
    Хэширование пароля.    
    """

    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """
    Проверка соответствия введённого пароля и хэша.
    """
    return bcrypt.checkpw(password.encode(), 
                          password_hash.encode())


def create_access_token(user_id: int, role: str) -> str:
    """
    Создание JWT-токена.

    Поля JWT-токена:\\
    sub - идентификатор пользователя;\\
    role - роль пользователя;\\
    iat - время выдачи токена;\\
    exp - время истечения токена.
    """

    now = datetime.now(timezone.utc)
    payload = {'sub': str(user_id),
               'role': role,
               'iat': now,
               'exp': now + timedelta(minutes=settings.access_token_expire_minutes)}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Декодирование JWT-токена.
    """

    payload = jwt.decode(token, settings.jwt_secret,
                         algorithms=[settings.jwt_alg],
                         options={'verify_exp': True})
    return payload
