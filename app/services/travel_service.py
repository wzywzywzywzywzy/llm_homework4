from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.services import llm_service, user_service
from app.schemas.schemas import TravelPlanCreate
from app.core.config import settings


class TravelService:
    """
    旅行服务类，整合LLM服务与数据库操作
    """
    
    async def generate_and_save_travel_plan(
        self, 
        db: Session,
        user_id: int,
        destination: str, 
        start_date: datetime,
        end_date: datetime, 
        budget: float, 
        preferences: str,
        travelers: int = 1
    ) -> Dict[str, Any]:
        """
        生成并保存旅游计划
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            destination: 目的地
            start_date: 开始日期 (datetime对象)
            end_date: 结束日期 (datetime对象)
            budget: 预算
            preferences: 偏好
            travelers: 旅行人数
            
        Returns:
            包含旅游计划信息的字典
        """
        # 调用LLM服务生成旅游计划
        # 将datetime对象转换为字符串传递给LLM服务
        llm_result = await self._call_llm_service(
            destination, 
            start_date.strftime("%Y-%m-%d"), 
            end_date.strftime("%Y-%m-%d"), 
            budget, 
            preferences, 
            travelers
        )
        
        # 检查LLM服务是否成功返回结果
        if not llm_result.get("success", False):
            return {
                "success": False,
                "error": llm_result.get("error", "未知错误")
            }
        
        # 获取生成的计划内容
        plan_content = llm_result.get("plan")
        if not plan_content:
            return {
                "success": False,
                "error": "未能生成有效的旅行计划内容"
            }
        
        # 创建旅行计划对象
        plan_title = f"{destination}旅行计划 ({start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')})"
        plan_data = TravelPlanCreate(
            title=plan_title,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            preferences=preferences,
            details=plan_content  # 使用正确的字段
        )
        
        # 保存到数据库
        db_plan = user_service.create_travel_plan(db=db, plan=plan_data, user_id=user_id)
        
        # 确保计划内容被正确保存
        if db_plan:
            db_plan.details = plan_content
            db.commit()
            db.refresh(db_plan)
        
        return {
            "success": True,
            "plan": db_plan,
            "ai_response": plan_content
        }
    
    async def _call_llm_service(self,
                             destination: str,
                             start_date: str,
                             end_date: str,
                             budget: float,
                             preferences: str,
                             travelers: int) -> Dict[str, Any]:
        """
        调用适当的LLM服务
        
        Args:
            destination: 目的地
            start_date: 开始日期 (字符串格式 YYYY-MM-DD)
            end_date: 结束日期 (字符串格式 YYYY-MM-DD)
            budget: 预算
            preferences: 偏好
            travelers: 旅行人数
            
        Returns:
            LLM服务返回的结果
        """
        # 检查是否配置了AI API
        if not settings.AI_API_KEY or not settings.AI_API_ENDPOINT:
            # 如果没有配置API密钥，使用模拟模式
            return await llm_service.llm_service.generate_travel_plan(
                destination, start_date, end_date, budget, preferences, travelers
            )
        
        # 根据API端点判断使用哪种服务
        api_endpoint = settings.AI_API_ENDPOINT or ""  # 确保不是None
        if "dashscope" in api_endpoint or "aliyuncs" in api_endpoint:
            # 使用阿里云百炼平台
            return await llm_service.llm_service.generate_travel_plan_with_dashscope(
                destination, start_date, end_date, budget, preferences, travelers
            )
        else:
            # 默认使用OpenAI格式
            return await llm_service.llm_service.generate_travel_plan(
                destination, start_date, end_date, budget, preferences, travelers
            )
    
    def parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """
        解析AI响应为结构化数据
        
        Args:
            ai_response: AI生成的文本响应
            
        Returns:
            结构化的旅游计划数据
        """
        # 这里可以实现更复杂的解析逻辑
        # 目前我们直接返回原始响应
        return {
            "raw_plan": ai_response
        }


# 创建全局实例
travel_service = TravelService()