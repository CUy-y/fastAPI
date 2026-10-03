from datetime import datetime

from fastapi import Depends, FastAPI
from sqlalchemy import DateTime, Float, String, func, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app=FastAPI()

ASYNC_DATABASE_URL="mysql+aiomysql://root:cyy45672@localhost:3306/fastapi_learn?charset=utf8"
async_engine=create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, #输出SQL日志
    pool_size=10, #设置连接池的活跃连接数
    max_overflow=20 #设置连接池的最大连接数
    )

# 定义模型类 ：基类 + 表对应的模型类
# 基类 ： 创建时间，更新时间；书籍表： id，书名，作者，价格，库存量，创建时间，更新时间

class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍ID")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")

# 3. 建表： 定义函数建表，调用FastAPI的时候调用建表的函数    

async def create_tables():
    # 获取异步引擎，创建事务 - 建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # 创建表结构

@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 需求： 查询功能的接口，查询图书 -> 依赖注入： 创建依赖项获取数据库会话 + Depends 注入路由处理函数
AsyncSessionLoccal = async_sessionmaker(
    bind=async_engine, # 绑定异步引擎
    class_=AsyncSession, # 指定异步会话类
    expire_on_commit=False # 设置会话在提交后不自动过期，不会重新查询数据库
)

# 依赖项
async def get_db():
    async with AsyncSessionLoccal() as session:
        try:
            yield session # 返回数据库会话给路由处理函数
            await session.commit() # 提交事务
        except Exception:
            await session.rollback() # 有异常，回滚
            raise
        finally:
            await session.close() # 关闭会话

@app.get("/books/books")
async def get_book_list(
    db: AsyncSession = Depends(get_db) 
    # Depends 是 FastAPI 的依赖注入机制。
    # 执行这个路由之前，先执行 get_db，把它提供的值注入给 db。
):
    stmt = select(Book)

    result = await db.execute(stmt)

    books = result.scalars().all()

    return books

'''
with...as 这个语法就是相当于把with后面的函数赋值给as后面的变量名，
然后这个能自动释放资源，前面加async 的就是相当于异步版本.

执行 Depends 里面的函数，然后把返回结果提供回去。
FastAPI 调用依赖函数，把它提供的依赖值注入参数。

await:
当前协程在这里等待这个异步操作完成；
等待期间把执行权交还给事件循环，使其可以运行其他任务。
完成后拿到结果，再从这里继续。
'''