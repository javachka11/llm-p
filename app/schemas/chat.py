from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Схема запроса на отправку сообщения в чат.

    Атрибуты:\\
    prompt - текст сообщения пользователя;\\
    system - опциональная системная инструкция;\\
    max_history - число сообщений, взятых из истории;\\
    temperature - температура модели.
    """

    prompt: str = Field(..., min_length=1,
                        title='Текст сообщения')
    system: str | None = Field(default=None,
                               title='Системная инструкция')
    max_history: int = Field(default=10, ge=0, le=50,
                             title='Число сообщений из истории')
    temperature: float = Field(default=0.7, ge=0.0, le=2.0,
                               title='Температура LLM-модели')


class ChatResponse(BaseModel):
    """
    Схема ответа от LLM.

    Атрибуты:\\
    answer - текст ответа.
    """

    answer: str = Field(...,
                        title='Текст ответа')
