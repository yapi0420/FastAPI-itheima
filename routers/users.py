from timeit import default_timer
from schemas.users import UserRegister,UserInfoResponse,UserAuthResponse,UserInfoBase
from  fastapi import APIRouter,Depends,Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news,users
from config.db_conf import get_db
from fastapi.exceptions import HTTPException
from fastapi import status
from utils.auth import get_current_user
from utils.response import success_response

router=APIRouter(prefix= "/api/user",tags=["users"])
@router.post("/register")
async def register(user_data: UserRegister, db: AsyncSession=Depends(get_db)):
    exiting_user=await users.get_user_by_username(db,user_data.username)
    if exiting_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    user=await users.create_user(db,user_data)
    token=await users.create_token(db,user.id)

    response=UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="成功",data={response})
    # return{
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

@router.post("/login")
async def login(user_datas:UserRegister,db: AsyncSession=Depends(get_db)):
    user=await users.authenticate_user(db,user_datas.username,user_datas.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token=await users.create_token(db,user.id)
    response=UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功",data=response)

# 获取用户信息
@router.get("/info")
async def get_user_info(user=Depends(get_current_user)):

    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))