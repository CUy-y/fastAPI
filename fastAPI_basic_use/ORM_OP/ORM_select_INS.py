'''
    查询
核心语句：await db.execute(select(模型类))，
返回一个ORM对象

获取所有数据：
result = await db.execute(select(模型类))
books = result.scalars().all()

获取单条：
result = await db.execute(select(模型类).where(模型类.字段==值))
book = result.scalars().first()
db.get(模型类，主键) 方法：获取单条数据，如果没有返回None
'''

from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
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
    result = await db.execute(select(Book))
    book = result.scalars().all() # 获取所有
    # book = result.scalars().first() # 获取单条
    # book = await db.get(Book, 2) # 获取单条，主键为2
    return book

# 先插入一些数据
@app.post("/books")
async def add_books(
    db: AsyncSession=Depends(get_db)
):
    books = [
        Book(
            bookname="活着",
            author="余华",
            price=39.0,
            publisher="作家出版社"
        ),
        Book(
            bookname="平凡的世界",
            author="路遥",
            price=78.0,
            publisher="北京十月文艺出版社"
        ),
        Book(
            bookname="百年孤独",
            author="加西亚·马尔克斯",
            price=56.8,
            publisher="南海出版公司"
        ),
        Book(
            bookname="解忧杂货店",
            author="东野圭吾",
            price=42.0,
            publisher="南海出版公司"
        )
    ]
    db.add_all(books)

    return {
        "message": "添加成功"
    }

# 比较判断
# 需求：路径参数 书籍id
@app.get("/book/get_book/{book_id}")
async def get_book_list(book_id,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(Book.id ==book_id))
    book = result.scalar_one_or_none()
    # 因为id是主键，所以一般只有一个，这个语句的作用是：
    # 从查询结果中取出“唯一的一条 ORM 对象”，如果没有则返回 None。
    return book

# 需求：条件 价格大于等于200
@app.get("/book/get_book_price/{price}")
async def get_book_price_list(
    price:int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(Book.price >= price))
    books = result.scalars().all()
    return books


# 模糊查询
# 需求： 作者以 。。。 开头
@app.get("/book/get_book_author/{Author}")
async def get_book_price_list(
    Author: str,
    db: AsyncSession = Depends(get_db)
):
    tmp :str = Author + "%"
    result = await db.execute(select(Book).where(Book.author.like(tmp)))
    # 实际上由更直观的写法：
    # select(Book).where(Book.author.startswith(Author))
    books = result.scalars().all()
    return books
'''
# 以某字符串开头
Book.author.startswith("余")

# 以某字符串结尾
Book.author.endswith("华")

# 包含某字符串
Book.author.contains("华")

# LIKE：以“余”开头
Book.author.like("余%")

# LIKE：以“华”结尾
Book.author.like("%华")

# LIKE：包含“华”
Book.author.like("%华%")
'''

# 需求：同时查询多个条件
@app.get("/book/get_book_author_AND_price/{Author}/{price}")
async def get_book_author_AND_price_list(
    Author: str,
    price: float,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(
        Book.author.startswith(Author),
        Book.price >= price))
    books = result.scalars().all()
    return books

# 正常情况下是Query参数
# 例如下面调用：/books?author=余&price=30
# 而不是/books/余/30
@app.get("/book/search")
async def get_book_author_AND_price_list2(
    Author: str = Query(...),
    price: float = Query(...),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(
        Book.author.startswith(Author),
        Book.price >= price))
    books = result.scalars().all()
    return books
'''
& 与，| 或，~ 非
'''


# 包含查询：in_()
@app.get("/book/search_id")
async def get_book_id_list(
    id_list: list[int] = Query(...),
    db: AsyncSession = Depends(get_db)
):    
    result = await db.execute(
        select(Book).where(Book.id.in_(id_list))
    )
    book = result.scalars().all()
    return book


# 聚合查询： func.方法(模型类.属性)
# count：统计行数量
# avg：求平均值
# max：求最大值
# min：求最小值
# sum：求和
@app.get("/book/count")
async def get_count(
    db: AsyncSession = Depends(get_db)
):
    # 聚合查询 select(func.方法名(模型类.属性))
    # result = await db.execute(select(func.count(Book.id)))
    # result = await db.execute(select(func.max(Book.price)))
    # result = await db.execute(select(func.sum(Book.price)))
    result = await db.execute(select(func.avg(Book.price)))
    count = result.scalar() # 用来提取一个数字 -> 标量值
    return count


# 分页查询： select.offset().limit()
# offset: 跳过的记录数
# limit: 返回的记录数
# offset 值 = (当前页码 - 1) * 每页数量 limit

@app.get("/book/get_books")
async def get_book_list(
    page: int = 1,
    page_size: int = 3,
    db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * page_size
    stmt = select(Book).offset(skip).limit(page_size)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return {"books": books}    

class BookUpdata(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str

# 删，改
@app.put("/book/updata/{book_id}")
async def updata_book(
    book_id: int,
    data: BookUpdata,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    # 实际上可以直接：
    # book = await db.get(Book, book_id) # 这个更简单
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book.bookname = data.bookname
    book.author = data.author
    book.publisher = data.publisher
    book.price = data.price
    return book

@app.delete("/book/delete_book/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    # 先查再删 提交
    db_book = await db.get(Book, book_id)
    # 如果查不到，抛出异常
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # 查到谁就删除谁
    await db.delete(db_book)
    await db.commit()
    return {"message": "Book deleted"}