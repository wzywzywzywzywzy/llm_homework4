from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.database.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联的旅行计划和预算信息通过关系在ORM中定义


class TravelPlan(Base):
    __tablename__ = "travel_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String, index=True)
    destination = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Float)
    preferences = Column(Text)  # 存储用户偏好
    details = Column(Text)  # 存储详细的旅行计划
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    plan_id = Column(Integer, index=True)
    category = Column(String)
    amount = Column(Float)
    description = Column(String)
    expense_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), server_default=func.now())