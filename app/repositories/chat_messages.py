from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    """
    Репозиторий для таблицы `chat_messages`.
    """

    def __init__(self, session: AsyncSession):
        self._session = session


    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """
        Добавление нового сообщения.
        """

        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message


    async def get_last_messages(self, user_id: int, n: int = 10) -> list[ChatMessage]:
        """
        Получение последних n сообщений пользователя в порядке их добавления.
        """

        result = await self._session.execute(select(ChatMessage)
                                             .where(ChatMessage.user_id == user_id)
                                             .order_by(ChatMessage.created_at.desc())
                                             .limit(n))
        messages = result.scalars().all()
        return list(messages)


    async def delete_messages(self, user_id: int) -> None:
        """
        Удаление сообщений пользователя.
        """

        await self._session.execute(delete(ChatMessage)
                                    .where(ChatMessage.user_id == user_id))
        await self._session.commit()
