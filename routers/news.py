from timeit import default_timer

from  fastapi import APIRouter,Depends,Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from config.db_conf import get_db
from fastapi.exceptions import HTTPException
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
        category_id: int =Query(...,alias="categoryId"),
        page:int =1,
        page_size:int =Query(10,alias="pageSize",le=100),
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

@router.get("/detail")
async def get_news_detail(news_id: int=Query(default=...,alias="id"),db: AsyncSession=Depends(get_db)):
    news_detail=await news.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")
    # if news_detail:
    #     news_detail.views+=1
    #     await db.commit()
    views_res=await news.increase_news_views(db,news_id)
    if not views_res:
        raise HTTPException(status_code=404,detail="新闻不存在")
    related_news= await news.get_related_news(db,news_detail.id,news_detail.category_id)
    return {
          "code": 200,
          "message": "success",
          "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
          }

    }