from starlette import status
from fastapi.dependencies.models import Dependant
from config.db_conf import get_db
from crud import users
from crud.users import get_user_by_token
from fastapi import Header, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

async def get_current_user(authorization: str = Header(...), db: AsyncSession = Depends(get_db)):
    """
    获取当前认证用户的信息
    
    从请求头的 Authorization 字段中提取 Bearer Token，并通过数据库查询验证用户身份。
    
    :param authorization: 请求头中的授权字符串，格式为 "Bearer {token}"
    :param db: 异步数据库会话实例，通过 Depends 注入
    :return: 通过 token 验证的用户对象
    """
    # 从授权字符串中移除 "Bearer " 前缀，提取纯 Token
    token=authorization.replace("Bearer ", "")
    # 通过 token 查询数据库，获取用户对象
    user=await users.get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失败")
    return user