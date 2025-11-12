from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from app.database.database import get_db
from app.schemas.schemas import UserCreate, User, Token, UserLogin
from app.services import user_service, auth_service, auth_utils
from app.core.config import settings
from datetime import timedelta
from pydantic import BaseModel
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 定义用于表单数据的模型
class UserCreateForm(BaseModel):
    username: str
    email: str
    password: str

class UserLoginForm(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(
    # 支持JSON和表单数据
    user: UserCreate = None,
    # 表单数据参数
    username: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # 如果通过表单传递数据，则创建UserCreate对象
        if username is not None and email is not None and password is not None:
            user = UserCreate(username=username, email=email, password=password)
        
        # 检查用户对象是否存在
        if user is None:
            raise HTTPException(status_code=400, detail="Missing user data")
        
        # 检查用户名是否已存在
        db_user = user_service.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # 检查邮箱是否已存在
        db_user = user_service.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # 创建新用户
        return user_service.create_user(db=db, user=user)
    
    except Exception as e:
        logger.error(f"用户注册失败: {str(e)}")
        # 如果是已知的HTTP异常，重新抛出
        if isinstance(e, HTTPException):
            raise e
        # 否则返回通用错误信息
        raise HTTPException(status_code=500, detail=f"注册失败: {str(e)}")


@router.post("/login", response_model=Token)
def login_user(
    # 支持JSON和表单数据
    user: UserLogin = None,
    # 表单数据参数
    username: str = Form(None),
    password: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # 如果通过表单传递数据，则创建UserLogin对象
        if username is not None and password is not None:
            user = UserLogin(username=username, password=password)
        
        # 检查用户对象是否存在
        if user is None:
            raise HTTPException(status_code=400, detail="Missing login credentials")
        
        # 验证用户
        db_user = user_service.authenticate_user(db, user.username, user.password)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        logger.error(f"用户登录失败: {str(e)}")
        # 如果是已知的HTTP异常，重新抛出
        if isinstance(e, HTTPException):
            raise e
        # 否则返回通用错误信息
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")


@router.get("/me", response_model=User)
def get_current_user(current_user: User = Depends(auth_utils.get_current_user)):
    return current_user