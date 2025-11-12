from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./travel_planner.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 语音识别API配置
    SPEECH_API_KEY: Optional[str] = None
    SPEECH_API_SECRET: Optional[str] = None
    
    # 地图API配置
    MAP_API_KEY: Optional[str] = None
    
    # AI大模型API配置
    AI_API_KEY: Optional[str] = None
    AI_API_ENDPOINT: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings()