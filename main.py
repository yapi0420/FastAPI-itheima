from fastapi import FastAPI
from routers import news,users
from fastapi.middleware.cors import CORSMiddleware
app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 允许所有源
    allow_credentials=True,  #允许携带cookie
    allow_methods=["*"],    #允许所有方法
    allow_headers=["*"],    #允许所有头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
#挂载路由
app.include_router(news.router)
app.include_router(users.router)