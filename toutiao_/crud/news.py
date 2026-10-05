from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from models.news import Category, News
 
 
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    获取新闻分类
    :param db: 数据库异步会话
    :param skip: 跳过的数据条数，用于分页查询
    :param limit: 每次查询的数据条数，用于分页查询
    :return: 新闻分类 ORM 对象列表
    """
    # 构建查询语句
    # offset(skip)：跳过前 skip 条数据
    # limit(limit)：最多查询 limit 条数据
    stmt = select(Category).offset(skip).limit(limit)
 
    # 执行异步 SQL 查询
    result = await db.execute(stmt)
 
    # scalars()：取出 Category ORM 对象
    # all()：把查询结果转换成列表返回
    return result.scalars().all()

async def get_news_list(
        db:AsyncSession,
        category_id : int,
        skip : int = 0,
        limit:int = 10
):
    # 查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
 
async def get_news_count(
        db:AsyncSession,
        category_id : int
):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 只能有一个结果，否则报错

async def get_news_detail(
        db: AsyncSession,
        new_id : int
):
    # 获取新闻详情
    stmt = select(News).where(News.id == new_id)
    result = await db.execute(stmt)
 
    return result.scalar_one_or_none()

async def increase_new_views(db: AsyncSession, news_id: int):
    """
    新闻浏览量 + 1
    :param db: 数据库
    :param news_id: 新闻ID
    :return:
    """
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
 
    #更新 → 检查数据库是否真的命中了数据 → 命中了返回True
    return result.rowcount > 0

async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    """
    新闻详情-相关推荐
    """
    stmt = (
        select(News)
        .where(
            News.id != news_id,
            News.category_id == category_id
        )
        .order_by(
            News.views.desc(),
            News.publish_time.desc()
        )
        .limit(limit)
    )
 
    result = await db.execute(stmt)
    related_news = result.scalars().all()
 
    return [
        {
            "id": item.id,
            "title": item.title,
            "content": item.content,
            "image": item.image,
            "author": item.author,
            "publishTime": item.publish_time,
            "categoryId": item.category_id,
            "views": item.views
        }
        for item in related_news
    ]