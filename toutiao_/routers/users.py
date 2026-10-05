# 用户注册
from fastapi.params import Depends

from toutiao_.common.result import Result
from toutiao_.config.db_conf import get_db
from toutiao_.crud import users
from toutiao_.schemas.users import UserAuthResponse, UserRequest
from toutiao_.utils.response import success_response


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 根据用户名查询数据库
    db_user = await users.get_user_by_username(db, user_data.username)
    if db_user:
        return Result.error("用户已存在", 400)
 
    # 新增用户
    user = await users.create_user(db, user_data)
 
    # 生成 Token
    token = await users.create_token(db, user.id)
 
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user_data.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar
    #         }
    #     }
    # }
 
    ## 构建响应数据：token + 用户信息
    # model_validate: 将 ORM 模型对象转换为 Pydantic 响应模型
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(data=response_data)