from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    """
    Бизнес-логика общения с LLM: отправка запросов и управление историей.
    """

    def __init__(self,
                 chat_repo: ChatMessageRepository,
                 llm_client: OpenRouterClient):
        self._chat_repo = chat_repo
        self._llm_client = llm_client


    async def ask(self, user_id: int, prompt: str,
                  system: str | None = None,
                  max_history: int = 10,
                  temperature: float = 0.7) -> str:
        """
        Отправка запроса в LLM с учетом системной инструкции и истории диалога.
        """

        messages = []

        if system:
            messages.append({'role': 'system', 'content': system})

        history = await self._chat_repo.get_last_messages(user_id, max_history)
        for msg in history:
            messages.append({'role': msg.role, 'content': msg.content})

        messages.append({'role': 'user', 'content': prompt})
        await self._chat_repo.add_message(user_id, 'user', prompt)

        answer = await self._llm_client.chat_completion(messages, temperature)
        await self._chat_repo.add_message(user_id, 'assistant', answer)

        return answer


    async def get_history(self, user_id: int, n: int = 10) -> list[dict]:
        """
        Получение истории сообщений пользователя.
        """

        messages = await self._chat_repo.get_last_messages(user_id, n)
        return [{'role': msg.role,
                 'content': msg.content,
                 'created_at': msg.created_at}
                for msg in messages]


    async def clear_history(self, user_id: int) -> None:
        """
        Очищение истории сообщений пользователя.
        """
        
        await self._chat_repo.delete_messages(user_id)
