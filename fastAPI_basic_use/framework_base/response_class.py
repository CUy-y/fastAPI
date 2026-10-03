from datetime import datetime

from fastapi import FastAPI
from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.ext.asyncio import create_async_engine
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


