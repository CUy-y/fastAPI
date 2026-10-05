from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase


class CategoryResponse(BaseModel):
    id: int
    name: str
    sort_order: int = Field(alias="sortOrder")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class NewsDetailResponse(NewsItemBase):
    content: str
    related_news: list[NewsItemBase] = Field(default_factory=list, alias="relatedNews")


class NewsCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    content: str = Field(min_length=1)
    image: str | None = Field(default=None, max_length=500)
    author: str | None = Field(default=None, max_length=100)
    category_id: int = Field(alias="categoryId", gt=0)
    publish_time: datetime | None = Field(default=None, alias="publishTime")

    model_config = ConfigDict(populate_by_name=True)
