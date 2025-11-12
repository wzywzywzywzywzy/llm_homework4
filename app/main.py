from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from app.database.database import engine
from app.models.models import Base
import app.api.auth_routes as auth_routes
import app.api.travel_routes as travel_routes

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Travel Planner", description="An AI-powered travel planning application")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由 (必须在静态文件挂载之前)
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(travel_routes.router, prefix="/api", tags=["travel"])

# 挂载静态文件
static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(static_dir):
    app.mount("/frontend", StaticFiles(directory=static_dir, html=True), name="frontend")

@app.get("/")
def read_root():
    # 重定向到前端页面
    return RedirectResponse(url="/frontend/index.html")

@app.get("/health")
def health_check():
    return {"status": "healthy"}