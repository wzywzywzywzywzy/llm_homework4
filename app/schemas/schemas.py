from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class TravelPlanBase(BaseModel):
    title: str
    destination: str
    start_date: datetime
    end_date: datetime
    budget: float
    preferences: str


class TravelPlanCreate(TravelPlanBase):
    pass


class TravelPlanUpdate(TravelPlanBase):
    details: Optional[str] = None


class TravelPlan(TravelPlanBase):
    id: int
    user_id: int
    details: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    category: str
    amount: float
    description: str
    expense_date: datetime = None


class ExpenseCreate(ExpenseBase):
    plan_id: int
    
    class Config:
        # 在创建时，expense_date是可选的，如果没有提供则使用当前时间
        extra = "forbid"


class Expense(ExpenseBase):
    id: int
    user_id: int
    plan_id: int
    created_at: datetime

    class Config:
        from_attributes = True