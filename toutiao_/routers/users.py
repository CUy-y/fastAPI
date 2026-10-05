from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.result import Result
from config.db_conf import get_db
from crud import users as users_crud
from models.users import User
from schemas.users import (
    UserAuthResponse,
    UserChangePasswordRequest,
    UserInfoResponse,
    UserRequest,
    UserUpdateRequest,
)
from utils.auth import get_current_user


router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(
    user_data: UserRequest, db: AsyncSession = Depends(get_db)
):
    if await users_crud.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=409, detail="用户名已存在")

    user = await users_crud.create_user(db, user_data)
    token = await users_crud.create_token(db, user.id)
    data = UserAuthResponse(
        token=token, userInfo=UserInfoResponse.model_validate(user)
    )
    return Result.success(message="注册成功", data=data)


@router.post("/login")
async def login(
    user_data: UserRequest, db: AsyncSession = Depends(get_db)
):
    user = await users_crud.authenticate_user(
        db, user_data.username, user_data.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = await users_crud.create_token(db, user.id)
    data = UserAuthResponse(
        token=token, userInfo=UserInfoResponse.model_validate(user)
    )
    return Result.success(message="登录成功", data=data)


@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return Result.success(
        message="获取用户信息成功", data=UserInfoResponse.model_validate(user)
    )


@router.put("/update")
async def update_user_info(
    user_data: UserUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    updated_user = await users_crud.update_user(db, user, user_data)
    return Result.success(
        message="更新用户信息成功",
        data=UserInfoResponse.model_validate(updated_user),
    )


@router.put("/password")
async def update_password(
    password_data: UserChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    changed = await users_crud.change_password(
        db, user, password_data.old_password, password_data.new_password
    )
    if not changed:
        raise HTTPException(status_code=400, detail="旧密码不正确")
    return Result.success(message="密码修改成功")
