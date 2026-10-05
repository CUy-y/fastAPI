from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Favorite(Base):
    __tablename__ = "favorite"
    __table_args__ = (
        UniqueConstraint("user_id", "news_id", name="uq_favorite_user_news"),
        Index("ix_favorite_user_id", "user_id"),
        Index("ix_favorite_news_id", "news_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    news_id: Mapped[int] = mapped_column(
        ForeignKey("news.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=func.current_timestamp()
    )
