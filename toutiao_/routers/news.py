from fastapi import APIRouter
 
# 创建 APIRouter 实例
router = APIRouter(prefix="/api/news", tags=["news"])
 
@router.get("/categories")
async def get_categories():
    return {"message":"获取分类成功"}