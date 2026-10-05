from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_history(db: AsyncSession, user_id: int, news_id: int):
    result = await db.execute(
        select(History).where(
            History.user_id == user_id, History.news_id == news_id
        )
    )
    history = result.scalar_one_or_none()
    if history is None:
        history = History(user_id=user_id, news_id=news_id)
        db.add(history)
    else:
        history.view_time = datetime.now()
    await db.flush()
    return history


async def get_history_list(
    db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10
):
    total_result = await db.execute(
        select(func.count(History.id)).where(History.user_id == user_id)
    )
    total = total_result.scalar_one()
    result = await db.execute(
        select(
            News,
            History.view_time.label("view_time"),
            History.id.label("history_id"),
        )
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc(), History.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return result.all(), total


async def delete_history(db: AsyncSession, user_id: int, news_id: int) -> bool:
    result = await db.execute(
        delete(History).where(
            History.user_id == user_id, History.news_id == news_id
        )
    )
    return result.rowcount > 0


async def clear_history(db: AsyncSession, user_id: int) -> int:
    result = await db.execute(delete(History).where(History.user_id == user_id))
    return result.rowcount or 0
