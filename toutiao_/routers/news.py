from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from common.result import Result
from crud import news
from config.db_conf import get_db
 
# 创建新闻模块路由
# prefix：当前文件下所有接口都会自动加上 /api/news 前缀
# tags：接口文档 Swagger 中显示的分组名称
router = APIRouter(prefix="/api/news", tags=["news"])
 
 
@router.get("/categories", response_model=Result)
async def get_categories(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    获取新闻分类
    :param db: 数据库异步会话
    :param skip: 跳过的数据条数，用于分页查询
    :param limit: 每次查询的数据条数，用于分页查询
    :return: 统一格式的新闻分类列表响应
    """
    # skip：跳过多少条数据；limit：最多返回多少条数据，用于分页查询
 
    # 调用 crud 层查询新闻分类列表
    categories = await news.get_categories(db, skip, limit)
 
    # 使用统一返回对象，避免每个接口都手写 code/message/data
    return Result.success(categories)