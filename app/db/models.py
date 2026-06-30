from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    """
    Модель пользователя приложения.

    Атрибуты:\\
    id - уникальный идентификатор (автоинкремент);\\
    email - электронный адрес;\\
    password_hash - хэш пароля;\\
    role - роль;\\
    created_at - дата и время регистрации (UTC);\\
    messages - связь one-to-many с ChatMessage.
    """
    
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    index=True)
    
    email: Mapped[str] = mapped_column(String(64),
                                       unique=True,
                                       nullable=False,
                                       index=True)
    
    password_hash: Mapped[str] = mapped_column(String(255),
                                               nullable=False)
    
    role: Mapped[str] = mapped_column(String(32),
                                      default='user',
                                      nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=lambda: datetime\
                                                 .now(timezone.utc))

    messages: Mapped[list['ChatMessage']] = relationship(back_populates='user',
                                                         cascade='all, delete-orphan')


class ChatMessage(Base):
    """
    Модель сообщения в чате приложения.

    Атрибуты:\\
    id - уникальный идентификатор (автоинкремент);\\
    user_id - внешний ключ на таблицу users;\\
    role - роль отправителя;\\
    content - текст сообщения;\\
    created_at - дата и время отправки сообщения (UTC);\\
    user - связь many-to-one с User.
    """

    __tablename__ = 'chat_messages'

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    index=True)
    user_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey('users.id'),
                                         nullable=False,
                                         index=True)
    role: Mapped[str] = mapped_column(String(32),
                                      nullable=False)
    content: Mapped[str] = mapped_column(Text,
                                         nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=lambda: datetime\
                                                 .now(timezone.utc))

    user: Mapped['User'] = relationship(back_populates='messages')
