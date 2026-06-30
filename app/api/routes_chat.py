from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase


chat_router = APIRouter()

@chat_router.post('', response_model=ChatResponse)
async def send_message(request: ChatRequest,
                       user_id: int = Depends(get_current_user_id),
                       chat_usecase: ChatUseCase = Depends(get_chat_usecase))\
                        -> ChatResponse:
    """Отправка запроса к LLM и получение от неё ответа."""

    try:
        answer = await chat_usecase.ask(user_id=user_id,
                                        prompt=request.prompt,
                                        system=request.system,
                                        max_history=request.max_history,
                                        temperature=request.temperature)
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=e.message)


@chat_router.get('/history')
async def get_history(max_history: int = 10,
                      user_id: int = Depends(get_current_user_id),
                      chat_usecase: ChatUseCase = Depends(get_chat_usecase))\
                      -> list[dict[str, Any]]:
    """
    Получение истории сообщений текущего пользователя.
    """

    return await chat_usecase.get_history(user_id, max_history)


@chat_router.delete('/history', status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(user_id: int = Depends(get_current_user_id),
                        chat_usecase: ChatUseCase = Depends(get_chat_usecase)):
    """
    Очищение истории сообщений текущего пользователя.
    """

    await chat_usecase.clear_history(user_id)
