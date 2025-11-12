from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.database.database import get_db
from app.schemas.schemas import TravelPlanCreate, TravelPlan, TravelPlanUpdate, ExpenseCreate, Expense, User
from app.services import user_service, auth_utils, travel_service
from app.services.speech_service import speech_service

# 定义请求模型
class GeneratePlanRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
    preferences: str = ""
    travelers: int = 1

# 添加新的请求模型
class BudgetAnalysisRequest(BaseModel):
    plan_id: int
    expenses: list

router = APIRouter()

@router.get("/plans/", response_model=List[TravelPlan])
def read_travel_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    plans = user_service.get_travel_plans(db, user_id=current_user.id, skip=skip, limit=limit)
    return plans


@router.get("/plans/{plan_id}", response_model=TravelPlan)
def read_travel_plan(plan_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    db_plan = user_service.get_travel_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Travel plan not found")
    if db_plan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this plan")
    return db_plan


@router.post("/plans/", response_model=TravelPlan)
def create_travel_plan(plan: TravelPlanCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    return user_service.create_travel_plan(db=db, plan=plan, user_id=current_user.id)


@router.post("/plans/generate", response_model=TravelPlan)
async def generate_travel_plan(
    request: GeneratePlanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_utils.get_current_user)
):
    """
    通过AI大语言模型生成旅游计划
    """
    # 验证输入参数
    if not request.destination:
        raise HTTPException(
            status_code=400,
            detail="目的地不能为空"
        )
    
    if request.budget <= 0:
        raise HTTPException(
            status_code=400,
            detail="预算必须大于0"
        )
    
    if request.travelers <= 0:
        raise HTTPException(
            status_code=400,
            detail="旅行人数必须大于0"
        )
    
    try:
        # 解析日期字符串
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        
        result = await travel_service.travel_service.generate_and_save_travel_plan(
            db=db,
            user_id=current_user.id,
            destination=request.destination,
            start_date=start_date,
            end_date=end_date,
            budget=request.budget,
            preferences=request.preferences,
            travelers=request.travelers
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate travel plan: {result['error']}"
            )
        
        # 确保返回的是Pydantic模型而不是数据库模型
        plan_data = result["plan"]
        if hasattr(plan_data, '__dict__'):
            # 如果是数据库模型，转换为字典
            plan_dict = {
                "id": plan_data.id,
                "user_id": plan_data.user_id,
                "title": plan_data.title,
                "destination": plan_data.destination,
                "start_date": plan_data.start_date,
                "end_date": plan_data.end_date,
                "budget": plan_data.budget,
                "preferences": plan_data.preferences,
                "details": plan_data.details,
                "created_at": plan_data.created_at,
                "updated_at": plan_data.updated_at
            }
            return TravelPlan(**plan_dict)
        else:
            # 如果已经是Pydantic模型，直接返回
            return plan_data
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"日期格式错误: {str(e)}"
        )
    except HTTPException:
        # 重新抛出已知的HTTP异常
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"生成旅游计划时发生错误: {str(e)}"
        )

@router.put("/plans/{plan_id}", response_model=TravelPlan)
def update_travel_plan(plan_id: int, plan: TravelPlanUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    db_plan = user_service.get_travel_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Travel plan not found")
    if db_plan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this plan")
    return user_service.update_travel_plan(db=db, plan_id=plan_id, plan=plan)


@router.delete("/plans/{plan_id}")
def delete_travel_plan(plan_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    db_plan = user_service.get_travel_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Travel plan not found")
    if db_plan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this plan")
    user_service.delete_travel_plan(db=db, plan_id=plan_id)
    return {"detail": "Travel plan deleted successfully"}


@router.get("/expenses/", response_model=List[Expense])
def read_expenses(plan_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    expenses = user_service.get_expenses(db, user_id=current_user.id, plan_id=plan_id, skip=skip, limit=limit)
    return expenses


@router.post("/expenses/", response_model=Expense)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    # 验证旅行计划是否存在且属于当前用户
    db_plan = user_service.get_travel_plan(db, plan_id=expense.plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Travel plan not found")
    if db_plan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add expense to this plan")
    
    return user_service.create_expense(db=db, expense=expense, user_id=current_user.id)


# 添加新的预算分析端点
@router.post("/budget/analyze")
async def analyze_budget(
    request: BudgetAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_utils.get_current_user)
):
    """
    通过AI分析旅行预算和开销
    """
    try:
        # 获取旅行计划
        db_plan = user_service.get_travel_plan(db, plan_id=request.plan_id)
        if db_plan is None:
            raise HTTPException(status_code=404, detail="Travel plan not found")
        
        # 验证计划是否属于当前用户
        if db_plan.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to analyze budget for this plan")
        
        # 获取该计划的所有开销
        expenses = user_service.get_expenses(db, user_id=current_user.id, plan_id=request.plan_id)
        
        # 调用AI服务进行预算分析
        from app.services import llm_service
        analysis_result = await llm_service.llm_service.analyze_budget(
            plan=db_plan,
            expenses=expenses
        )
        
        if not analysis_result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze budget: {analysis_result.get('error', 'Unknown error')}"
            )
        
        return {
            "success": True,
            "analysis": analysis_result.get("analysis")
        }
        
    except HTTPException:
        # 重新抛出已知的HTTP异常
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"预算分析时发生错误: {str(e)}"
        )


# 添加语音识别端点
@router.post("/speech/recognize")
async def recognize_speech(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_utils.get_current_user)
):
    """
    语音识别端点
    """
    try:
        # 获取音频数据
        audio_data = await request.body()
        
        # 调用语音识别服务
        result = speech_service.recognize_speech(audio_data)
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )
        
        return {
            "success": True,
            "text": result["text"]
        }
        
    except HTTPException:
        # 重新抛出已知的HTTP异常
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"语音识别时发生错误: {str(e)}"
        )
