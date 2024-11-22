from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.word_api import word_router
from app.api.character_api import character_router

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(word_router, prefix="/api")
app.include_router(character_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

