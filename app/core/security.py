from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

ctx = CryptContext(schemes=['sha256_crypt'])


def hash_password(password: str) -> str:
    return ctx.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return ctx.verify(plain_password, hashed_password)


def create_access_token(user_id: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {'sub': str(user_id),
               'role': role,
               'iat': now,
               'exp': now + timedelta(minutes=settings.access_token_expire_minutes)}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret,
                             algorithms=[settings.jwt_alg])
        return payload
    except JWTError:
        raise ValueError('Invalid token!')