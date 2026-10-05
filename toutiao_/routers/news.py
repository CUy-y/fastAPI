from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from common.page_result import PageResult
from common.result import Result
from config.db_conf import get_db
from crud import news as news_crud
from schemas.base import NewsItemBase
from schemas.news import CategoryResponse, NewsDetailResponse


router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
):
    categories = await news_crud.get_categories(db, skip, limit)
    data = [CategoryResponse.model_validate(item) for item in categories]
    return Result.success(data=data)


@router.get("/list")
async def get_news_list(
    category_id: int = Query(..., alias="categoryId", gt=0),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, alias="pageSize", ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * page_size
    items = await news_crud.get_news_list(db, category_id, offset, page_size)
    total = await news_crud.get_news_count(db, category_id)
    return PageResult.page(
        list_data=[NewsItemBase.model_validate(item) for item in items],
        total=total,
        has_more=(offset + len(items)) < total,
    )


@router.get("/detail")
async def get_news_detail(
    news_id: int = Query(..., alias="id", gt=0),
    db: AsyncSession = Depends(get_db),
):
    item = await news_crud.get_news_detail(db, news_id)
    if item is None:
        raise HTTPException(status_code=404, detail="该新闻不存在")

    await news_crud.increase_news_views(db, news_id)
    await db.refresh(item)
    related = await news_crud.get_related_news(db, item.id, item.category_id)
    detail = NewsDetailResponse.model_validate(item)
    detail.related_news = [NewsItemBase.model_validate(row) for row in related]
    return Result.success(message="获取新闻详情成功", data=detail)
