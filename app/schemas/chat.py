from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    system_info: str | None = Field(None, description='Системная инструкция')
    max_history: int = Field(10, ge=0, le=50, description='Число сообщений из истории')
    temperature: float = Field(0.7, ge=0.0, le=2.0, description='Температура LLM-модели')


class ChatResponse(BaseModel):
    answer: str
