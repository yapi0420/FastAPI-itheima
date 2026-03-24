from click import echo
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine


#数据库URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:yzb060906@localhost:3306/news_app?charset=utf8mb4"


#创建异步引擎
async_engin = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    )

#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engin,
    class_=AsyncSession,
    expire_on_commit=False,
)
async def get_db():
    """
    获取数据库连接
    :return:
    """
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception :
            await db.rollback()
            raise
        finally:
            await db.close()