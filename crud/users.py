from datetime import datetime,timedelta

from fastapi import HTTPException
from sqlalchemy import select,update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from utils import security
from schemas.users import UserUpdateRequest,UserRequest
import uuid
#根據用戶名查詢數據庫
async def get_user_by_username( db: AsyncSession,username: str):
    query =select(User).where(User.username==username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

#創建用戶
async def create_user(db: AsyncSession,user_data: UserRequest):
    hashed_password = security.get_password_hash(user_data.password)
    user = User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)#刷新數據庫
    return user

#生成Token
async def create_token(db: AsyncSession,user_id:int):
    token=str(uuid.uuid4())
    expires_at=datetime.now()+timedelta(days=7)
    query=select(UserToken).where(UserToken.user_id==user_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token

async def authenticate_user(db: AsyncSession,username: str,password: str):
    user = await get_user_by_username(db,username)
    if not user:
        return None
    if not security.verify_password(password,user.password):
        return None
    return user

#根据token查询用户
async def get_user_by_token(db: AsyncSession,token: str):
    query =select(UserToken).where(UserToken.token==token)
    result = await db.execute(query)
    user_token=result.scalar_one_or_none()
    if not user_token or user_token.expires_at>datetime.now():
        return None
    query=select( User).where(User.id==user_token.user_id)
    result=await db.execute(query)
    return result.scalar_one_or_none()

#更新用户信息
# 更新用户信息: update更新 → 检查是否命中 → 获取更新后的用户返回
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    # update(User).where(User.username == username).values(字段=值, 字段=值)
    # user_data 是一个Pydantic类型，得到字典 → ** 解包
    # 没有设置值的不更新
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))
    result = await db.execute(query)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取一下更新后的用户
    updated_user = await get_user_by_username(db, username)
    return updated_user
