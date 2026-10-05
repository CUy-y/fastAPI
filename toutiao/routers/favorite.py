from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from common.result import Result
from config.db_conf import get_db
from crud import favorite as favorite_crud
from crud import news as news_crud
from models.users import User
from schemas.base import NewsItemBase
from schemas.favorite import (
    FavoriteAddRequest,
    FavoriteCheckResponse,
    FavoriteListResponse,
    FavoriteNewsItemResponse,
)
from utils.auth import get_current_user


router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId", gt=0),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    favorited = await favorite_crud.is_news_favorite(db, user.id, news_id)
    return Result.success(
        message="检查收藏状态成功",
        data=FavoriteCheckResponse(isFavorite=favorited),
    )


@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if await news_crud.get_news_detail(db, data.news_id) is None:
        raise HTTPException(status_code=404, detail="该新闻不存在")
    if await favorite_crud.is_news_favorite(db, user.id, data.news_id):
        raise HTTPException(status_code=409, detail="该新闻已收藏")
    favorite = await favorite_crud.add_news_favorite(db, user.id, data.news_id)
    return Result.success(message="添加收藏成功", data={"id": favorite.id})


@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId", gt=0),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    removed = await favorite_crud.remove_news_favorite(db, user.id, news_id)
    if not removed:
        raise HTTPException(status_code=404, detail="收藏记录不存在")
    return Result.success(message="删除收藏成功")


@router.get("/list")
async def get_favorite_list(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, alias="pageSize", ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows, total = await favorite_crud.get_favorite_list(
        db, user.id, page, page_size
    )
    items = [
        FavoriteNewsItemResponse.model_validate(
            {
                **NewsItemBase.model_validate(item).model_dump(by_alias=True),
                "favoriteId": favorite_id,
                "favoriteTime": favorite_time,
            }
        )
        for item, favorite_time, favorite_id in rows
    ]
    data = FavoriteListResponse(
        list=items,
        total=total,
        hasMore=total > page * page_size,
    )
    return Result.success(message="获取收藏列表成功", data=data)


@router.delete("/clear")
async def clear_favorites(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    count = await favorite_crud.remove_all_favorites(db, user.id)
    return Result.success(message=f"清空了{count}条记录")
