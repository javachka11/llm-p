from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase


router = APIRouter()

@router.post('', response_model=ChatResponse)
async def send_message(request: ChatRequest,
                       user_id: int = Depends(get_current_user_id),
                       chat_usecase: ChatUseCase = Depends(get_chat_usecase)):
    try:
        answer = await chat_usecase.ask(user_id=user_id,
                                        prompt=request.prompt,
                                        system_info=request.system_info,
                                        max_history=request.max_history,
                                        temperature=request.temperature)
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=e.message)


@router.get('/history')
async def get_history(max_history: int = 50,
                      user_id: int = Depends(get_current_user_id),
                      chat_usecase: ChatUseCase = Depends(get_chat_usecase)):
    return await chat_usecase.get_history(user_id, max_history)


@router.delete('/history', status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(user_id: int = Depends(get_current_user_id),
                        chat_usecase: ChatUseCase = Depends(get_chat_usecase)):
    await chat_usecase.clear_history(user_id)
