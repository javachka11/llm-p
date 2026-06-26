from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    index=True)
    email: Mapped[str] = mapped_column(String(255),
                                       unique=True,
                                       nullable=False,
                                       index=True)
    password_hash: Mapped[str] = mapped_column(String(255),
                                               nullable=False)
    role: Mapped[str] = mapped_column(String(30),
                                      default='user',
                                      nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=lambda: datetime\
                                                 .now(timezone.utc))

    messages: Mapped[list['ChatMessage']] = relationship(back_populates='user',
                                                         cascade='all, delete-orphan')


class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    index=True)
    user_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey('users.id'),
                                         nullable=False,
                                         index=True)
    role: Mapped[str] = mapped_column(String(30),
                                      nullable=False)
    content: Mapped[str] = mapped_column(Text,
                                         nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=lambda: datetime\
                                                 .now(timezone.utc))

    user: Mapped['User'] = relationship(back_populates='messages')