from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(alias="isFavorite")

    model_config = ConfigDict(populate_by_name=True)


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(alias="newsId", gt=0)

    model_config = ConfigDict(populate_by_name=True)


class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")


class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(populate_by_name=True)
