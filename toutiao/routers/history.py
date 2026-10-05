from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from common.result import Result
from config.db_conf import get_db
from crud import history as history_crud
from crud import news as news_crud
from models.users import User
from schemas.base import NewsItemBase
from schemas.history import (
    HistoryAddRequest,
    HistoryListResponse,
    HistoryNewsItemResponse,
)
from utils.auth import get_current_user


router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
    data: HistoryAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if await news_crud.get_news_detail(db, data.news_id) is None:
        raise HTTPException(status_code=404, detail="该新闻不存在")
    record = await history_crud.add_history(db, user.id, data.news_id)
    return Result.success(message="添加成功", data={"id": record.id})


@router.get("/list")
async def get_history_list(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, alias="pageSize", ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows, total = await history_crud.get_history_list(
        db, user.id, page, page_size
    )
    items = [
        HistoryNewsItemResponse.model_validate(
            {
                **NewsItemBase.model_validate(item).model_dump(by_alias=True),
                "historyId": history_id,
                "viewTime": view_time,
            }
        )
        for item, view_time, history_id in rows
    ]
    data = HistoryListResponse(
        list=items,
        total=total,
        hasMore=total > page * page_size,
    )
    return Result.success(message="获取浏览历史成功", data=data)


@router.delete("/delete/{news_id}")
async def delete_history(
    news_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    removed = await history_crud.delete_history(db, user.id, news_id)
    if not removed:
        raise HTTPException(status_code=404, detail="历史记录不存在")
    return Result.success(message="删除成功")


@router.delete("/clear")
async def clear_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    count = await history_crud.clear_history(db, user.id)
    return Result.success(message=f"清空了{count}条记录")
