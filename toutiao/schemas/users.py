from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=72)

    @field_validator("username")
    @classmethod
    def strip_username(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("用户名不能为空")
        return value

    @field_validator("password")
    @classmethod
    def bcrypt_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("密码 UTF-8 编码后不能超过 72 字节")
        return value


class UserInfoResponse(BaseModel):
    id: int
    username: str
    nickname: str | None = None
    avatar: str | None = None
    gender: str | None = None
    bio: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(alias="userInfo")

    model_config = ConfigDict(populate_by_name=True)


class UserUpdateRequest(BaseModel):
    nickname: str | None = Field(default=None, max_length=50)
    avatar: str | None = Field(default=None, max_length=255)
    gender: str | None = Field(default=None, pattern="^(male|female|unknown)$")
    bio: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)


class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(alias="oldPassword", min_length=1, max_length=72)
    new_password: str = Field(alias="newPassword", min_length=6, max_length=72)

    @field_validator("old_password", "new_password")
    @classmethod
    def bcrypt_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("密码 UTF-8 编码后不能超过 72 字节")
        return value

    model_config = ConfigDict(populate_by_name=True)
