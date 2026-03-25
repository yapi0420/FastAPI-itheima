from timeit import default_timer
from schemas.users import UserRegister
from  fastapi import APIRouter,Depends,Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news,users
from config.db_conf import get_db
from fastapi.exceptions import HTTPException
from fastapi import status

router=APIRouter(prefix= "/api/user",tags=["users"])
@router.post("/register")
async def register(user_data: UserRegister, db: AsyncSession=Depends(get_db)):
    exiting_user=await users.get_user_by_username(db,user_data.username)
    if exiting_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    user=await users.create_user(db,user_data)
    return{
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