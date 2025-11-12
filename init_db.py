import os
import sys
from sqlalchemy import create_engine
from app.models.models import Base
from app.core.config import settings

def init_db():
    """初始化数据库"""
    engine = create_engine(settings.DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()