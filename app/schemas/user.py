from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    """
    Схема публичной информации о пользователе.

    Атрибуты:\\
    id - уникальный идентификатор;\\
    email - электронный адрес;\\
    role - роль.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: str
