from timeit import default_timer

from  fastapi import APIRouter,Depends,Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from config.db_conf import get_db
#创建apirouter 实例

"""
接口实现流程
模块化路由->API 接口规范文档
定义模型类->数据库表（数据库设计文档）
在crud（数据库增删改查）文件夹里创建文件，封装操作数据库的方法
在路由处理函数里面调用crud封装好的方法，响应结果
"""
router = APIRouter(prefix= "/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(db: AsyncSession=Depends(get_db),skip: int=0,limit: int=100):

    categories= await news.get_categories(db,skip,limit)
    return {
        "code":200,
        "message": "获取新闻成功",
        "data" : categories,
    }

@router.get("/list")
async def get_news_list(
        category_id: int =Query(default=...,alias="categoryId"),
        page:int =1,
        page_size:int =Query(default=10,alias="pageSize",le=100),
        db: AsyncSession=Depends(get_db)
):
    news_list=await news.get_news_list(db,category_id,(page-1)*page_size,page_size)
    total = await news.get_news_count(db,category_id)
    has_more =((page-1)*page_size+len(news_list) < total)
    return {
        "code":200,
        "message": "获取新闻成功",
        "data" : {
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }