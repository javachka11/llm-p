from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.users import UserRepository
from app.schemas.user import UserPublic


class AuthUseCase:
    """
    Бизнес-логика аутентификации: регистрация, вход и получение профиля.
    """

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> UserPublic:
        """
        Регистрация нового пользователя.
        """
        
        existing_user = await self._user_repo.get_by_email(email)
        if existing_user:
            raise ConflictError(f'Пользователь {email} уже зарегистрирован.')

        password_hash = hash_password(password)
        user = await self._user_repo.create(email, password_hash)
        return UserPublic.model_validate(user)


    async def login(self, email: str, password: str) -> str:
        """
        Аутентификация пользователя с получением JWT-токена.
        """

        user = await self._user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError(f'Пользователя {email} не существует.')

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError('Неверный пароль.')

        return create_access_token(user.id, user.role)


    async def get_profile(self, user_id: int) -> UserPublic:
        """
        Получение профиля пользователя по его id.
        """
        
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError('Пользователь не найден.')

        return UserPublic.model_validate(user)
