from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserRequest):
    user = User(
        username=user_data.username,
        password=security.get_hash_password(user_data.password),
    )
    db.add(user)
    await db.flush()
    return user


async def create_token(db: AsyncSession, user_id: int) -> str:
    result = await db.execute(
        select(UserToken)
        .where(UserToken.user_id == user_id)
        .order_by(UserToken.id.desc())
        .limit(1)
    )
    token_record = result.scalar_one_or_none()
    token = uuid4().hex
    expires_at = datetime.now() + timedelta(days=7)

    if token_record:
        token_record.token = token
        token_record.expires_at = expires_at
    else:
        db.add(UserToken(user_id=user_id, token=token, expires_at=expires_at))
    await db.flush()
    return token


async def get_user_by_token(db: AsyncSession, token: str):
    result = await db.execute(
        select(User)
        .join(UserToken, UserToken.user_id == User.id)
        .where(UserToken.token == token, UserToken.expires_at > datetime.now())
    )
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if user is None or not security.verify_password(password, user.password):
        return None
    return user


async def update_user(db: AsyncSession, user: User, user_data: UserUpdateRequest):
    changes = user_data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(user, field, value)
    await db.flush()
    return user


async def change_password(
    db: AsyncSession, user: User, old_password: str, new_password: str
) -> bool:
    if not security.verify_password(old_password, user.password):
        return False
    user.password = security.get_hash_password(new_password)
    await db.flush()
    return True
