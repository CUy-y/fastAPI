from pydantic import BaseModel
 
# 用户请求
class UserRequest(BaseModel):
    username: str
    password: str