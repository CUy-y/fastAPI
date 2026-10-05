from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
 
from common.result import Result
from config.db_confing import get_db
from schemas.users import UserRequest
from crud import users
 
router = APIRouter(prefix="/api/user", tags=["users"])
 
 
# 用户注册
@router.post("register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 根据用户名查询数据库
    db_user = await users.get_user_by_username(db, user_data.username)
    if db_user:
        return Result.error("用户已存在",400)
 
    # 新增用户
    user = await users.create_user(db, user_data)
 
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": user.id,
                "username": user_data.username,
                "bio": user.bio,
                "avatar": user.avatar
            }
        }
    }