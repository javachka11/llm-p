from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(self,
                 chat_repo: ChatMessageRepository,
                 llm_client: OpenRouterClient):
        self._chat_repo = chat_repo
        self._llm_client = llm_client


    async def ask(self, user_id: int, prompt: str,
                  system: str | None = None,
                  max_history: int = 10) -> str:
        messages = []

        if system:
            messages.append({'role': 'system', 'content': system})

        history = await self._chat_repo.get_last_messages(user_id, max_history)
        for msg in history:
            messages.append({'role': msg.role, 'content': msg.content})

        messages.append({'role': 'user', 'content': prompt})
        await self._chat_repo.add_message(user_id, 'user', prompt)

        answer = await self._llm_client.chat_completion(messages)
        await self._chat_repo.add_message(user_id, 'assistant', answer)

        return answer