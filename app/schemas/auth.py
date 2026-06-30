from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """
    Схема запроса на регистрацию нового пользователя в системе.

    Атрибуты:\\
    email - электронный адрес пользователя;\\
    password - пароль пользователя.
    """

    email: EmailStr = Field(..., max_length=64,
                            description='Email пользователя')
    password: str = Field(..., min_length=8, max_length=64,
                          description='Пароль пользователя')


class TokenResponse(BaseModel):
    """
    Схема ответа при успешном входе в систему.

    Атрибуты:\\
    access_token - JWT-токен доступа;\\
    token_type - тип токена.
    """
    
    access_token: str = Field(...,
                              description='JWT-токен доступа')
    token_type: str = Field(default='bearer', max_length=32,
                            description='Тип токена')
