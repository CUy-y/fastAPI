from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category, News


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Category).order_by(Category.sort_order, Category.id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_news_list(
    db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10
):
    result = await db.execute(
        select(News)
        .where(News.category_id == category_id)
        .order_by(News.publish_time.desc(), News.id.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_news_count(db: AsyncSession, category_id: int) -> int:
    result = await db.execute(
        select(func.count(News.id)).where(News.category_id == category_id)
    )
    return result.scalar_one()


async def get_news_detail(db: AsyncSession, news_id: int):
    result = await db.execute(select(News).where(News.id == news_id))
    return result.scalar_one_or_none()


async def increase_news_views(db: AsyncSession, news_id: int) -> bool:
    result = await db.execute(
        update(News).where(News.id == news_id).values(views=News.views + 1)
    )
    return result.rowcount > 0


async def get_related_news(
    db: AsyncSession, news_id: int, category_id: int, limit: int = 5
):
    result = await db.execute(
        select(News)
        .where(News.id != news_id, News.category_id == category_id)
        .order_by(News.views.desc(), News.publish_time.desc())
        .limit(limit)
    )
    return result.scalars().all()
