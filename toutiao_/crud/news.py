from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from models.news import Category
 
 
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