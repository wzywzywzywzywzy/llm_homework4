from sqlalchemy.orm import Session
from app.models.models import User, TravelPlan, Expense
from app.schemas.schemas import UserCreate, TravelPlanCreate, TravelPlanUpdate, ExpenseCreate
from app.core.security import get_password_hash, verify_password
from passlib.exc import MissingBackendError


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
    except MissingBackendError as e:
        raise Exception(f"密码哈希处理失败: {str(e)}")
    
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_travel_plans(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(TravelPlan).filter(TravelPlan.user_id == user_id).offset(skip).limit(limit).all()


def get_travel_plan(db: Session, plan_id: int):
    return db.query(TravelPlan).filter(TravelPlan.id == plan_id).first()


def create_travel_plan(db: Session, plan: TravelPlanCreate, user_id: int):
    db_plan = TravelPlan(**plan.dict(), user_id=user_id)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def update_travel_plan(db: Session, plan_id: int, plan: TravelPlanUpdate):
    db_plan = db.query(TravelPlan).filter(TravelPlan.id == plan_id).first()
    if db_plan:
        update_data = plan.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_plan, key, value)
        db.commit()
        db.refresh(db_plan)
    return db_plan


def delete_travel_plan(db: Session, plan_id: int):
    db_plan = db.query(TravelPlan).filter(TravelPlan.id == plan_id).first()
    if db_plan:
        db.delete(db_plan)
        db.commit()
    return db_plan


def get_expenses(db: Session, user_id: int, plan_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(Expense).filter(Expense.user_id == user_id)
    if plan_id:
        query = query.filter(Expense.plan_id == plan_id)
    return query.offset(skip).limit(limit).all()


def create_expense(db: Session, expense: ExpenseCreate, user_id: int):
    # 如果没有提供expense_date，则使用当前时间
    expense_dict = expense.dict()
    if expense_dict.get('expense_date') is None:
        expense_dict['expense_date'] = datetime.utcnow()
    
    db_expense = Expense(**expense_dict, user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense