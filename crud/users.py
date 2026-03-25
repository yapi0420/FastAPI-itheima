from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import  User
from utils import security
from schemas.users import UserRegister
#根據用戶名查詢數據庫
async def get_user_by_username( db: AsyncSession,username: str):
    query =select(User).where(User.username==username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

#創建用戶
async def create_user(db: AsyncSession,user_data: UserRegister):
    hashed_password = security.get_password_hash(user_data.password)
    user = User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)#刷新數據庫
    return user