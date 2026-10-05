from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    result = await db.execute(
        select(Favorite.id).where(
            Favorite.user_id == user_id, Favorite.news_id == news_id
        )
    )
    return result.scalar_one_or_none() is not None


async def add_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.flush()
    return favorite


async def remove_news_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    result = await db.execute(
        delete(Favorite).where(
            Favorite.user_id == user_id, Favorite.news_id == news_id
        )
    )
    return result.rowcount > 0


async def get_favorite_list(
    db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10
):
    total_result = await db.execute(
        select(func.count(Favorite.id)).where(Favorite.user_id == user_id)
    )
    total = total_result.scalar_one()
    result = await db.execute(
        select(
            News,
            Favorite.created_at.label("favorite_time"),
            Favorite.id.label("favorite_id"),
        )
        .join(Favorite, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc(), Favorite.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return result.all(), total


async def remove_all_favorites(db: AsyncSession, user_id: int) -> int:
    result = await db.execute(delete(Favorite).where(Favorite.user_id == user_id))
    return result.rowcount or 0
