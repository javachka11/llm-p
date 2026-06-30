from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase


auth_router = APIRouter()

@auth_router.post('/register', response_model=UserPublic,
                  status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest,
                   auth_usecase: AuthUseCase = Depends(get_auth_usecase))\
                   -> UserPublic:
    """
    Регистрация нового пользователя.
    """

    try:
        return await auth_usecase.register(request.email, request.password)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=e.message)


@auth_router.post('/login', response_model=TokenResponse)
async def login(oauth2_form: OAuth2PasswordRequestForm = Depends(),
                auth_usecase: AuthUseCase = Depends(get_auth_usecase))\
                -> TokenResponse:
    """
    Аутентификация пользователя через OAuth2 форму и получение JWT-токена.
    """

    try:
        access_token = await auth_usecase.login(oauth2_form.username, oauth2_form.password)
        return TokenResponse(access_token=access_token)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=e.message)


@auth_router.get('/me', response_model=UserPublic)
async def get_current_user(user_id: int = Depends(get_current_user_id),
                           auth_usecase: AuthUseCase = Depends(get_auth_usecase))\
                           -> UserPublic:
    """
    Получение профиля текущего авторизованного пользователя.
    """
    
    try:
        return await auth_usecase.get_profile(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)
