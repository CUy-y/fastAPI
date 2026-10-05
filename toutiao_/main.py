from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import insert, select

from config.db_conf import async_engine
from models import favorite, history, news, users  # noqa: F401 - register all ORM models
from models.base import Base
from models.news import Category
from routers import favorite as favorite_router
from routers import history as history_router
from routers import news as news_router
from routers import users as users_router
from utils.exception_handlers import register_exception_handlers


DEFAULT_CATEGORIES = (
    "头条",
    "社会",
    "国内",
    "国际",
    "娱乐",
    "体育",
    "科技",
    "财经",
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # The database itself is created once during project setup. The app creates
    # missing tables and starter categories without dropping or replacing data.
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with async_engine.begin() as connection:
        existing = set((await connection.execute(select(Category.name))).scalars())
        missing = [
            {"name": name, "sort_order": index}
            for index, name in enumerate(DEFAULT_CATEGORIES, start=1)
            if name not in existing
        ]
        if missing:
            await connection.execute(insert(Category), missing)

    yield
    await async_engine.dispose()


app = FastAPI(title="今日头条", version="1.0.0", lifespan=lifespan)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router.router)
app.include_router(users_router.router)
app.include_router(favorite_router.router)
app.include_router(history_router.router)


@app.get("/")
async def root():
    return {"message": "今日头条 API 正在运行", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}
