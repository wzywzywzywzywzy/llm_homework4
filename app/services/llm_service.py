import httpx
import json
from typing import Dict, Any, Optional
from app.core.config import settings


class LLMService:
    """
    大语言模型服务类，用于与AI API通信生成旅游计划
    """
    
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.api_endpoint = settings.AI_API_ENDPOINT
        self.client = httpx.AsyncClient()
    
    async def generate_travel_plan(self, 
                                 destination: str, 
                                 start_date: str,
                                 end_date: str, 
                                 budget: float, 
                                 preferences: str,
                                 travelers: int = 1) -> Dict[str, Any]:
        """
        生成旅游计划
        
        Args:
            destination: 目的地
            start_date: 开始日期
            end_date: 结束日期
            budget: 预算
            preferences: 偏好
            travelers: 旅行人数
            
        Returns:
            包含旅游计划详细信息的字典
        """
        # 如果没有配置API密钥，返回模拟数据
        if not self.api_key or not self.api_endpoint or "example.com" in self.api_endpoint:
            return self._generate_mock_plan(destination, start_date, end_date, budget, preferences, travelers)
        
        # 构建提示词
        prompt = self._build_travel_prompt(
            destination, start_date, end_date, budget, preferences, travelers
        )
        
        # 构建API请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",  # 可根据实际API调整
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的旅游规划师，能够根据用户需求生成详细的旅游计划。请用中文回复，提供结构化和易读的旅游计划。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            # 发送请求到AI API
            response = await self.client.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            plan_content = result["choices"][0]["message"]["content"]
            
            return {
                "success": True,
                "plan": plan_content,
                "raw_response": result
            }
            
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "请求AI服务超时，请稍后重试",
                "plan": None
            }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"网络请求错误: {str(e)}",
                "plan": None
            }
        except KeyError as e:
            return {
                "success": False,
                "error": f"AI服务返回格式错误: {str(e)}",
                "plan": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"生成旅游计划时发生未知错误: {str(e)}",
                "plan": None
            }
    
    async def generate_travel_plan_with_dashscope(self,
                                                destination: str,
                                                start_date: str,
                                                end_date: str,
                                                budget: float,
                                                preferences: str,
                                                travelers: int = 1) -> Dict[str, Any]:
        """
        针对阿里云百炼平台的旅游计划生成方法
        
        Args:
            destination: 目的地
            start_date: 开始日期
            end_date: 结束日期
            budget: 预算
            preferences: 偏好
            travelers: 旅行人数
            
        Returns:
            包含旅游计划详细信息的字典
        """
        # 如果没有配置API密钥，返回模拟数据
        if not self.api_key or not self.api_endpoint or "example.com" in self.api_endpoint:
            return self._generate_mock_plan(destination, start_date, end_date, budget, preferences, travelers)
        
        # 构建提示词
        prompt = self._build_travel_prompt(
            destination, start_date, end_date, budget, preferences, travelers
        )
        
        # 构建API请求（阿里云百炼平台格式）
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "qwen-turbo",  # 阿里云百炼平台模型
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的旅游规划师，能够根据用户需求生成详细的旅游计划。请用中文回复，提供结构化和易读的旅游计划。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }
        
        try:
            # 发送请求到阿里云百炼平台
            response = await self.client.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            plan_content = result["output"]["text"]
            
            return {
                "success": True,
                "plan": plan_content,
                "raw_response": result
            }
            
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "请求AI服务超时，请稍后重试",
                "plan": None
            }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"网络请求错误: {str(e)}",
                "plan": None
            }
        except KeyError as e:
            return {
                "success": False,
                "error": f"AI服务返回格式错误: {str(e)}",
                "plan": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"生成旅游计划时发生未知错误: {str(e)}",
                "plan": None
            }
    
    def _generate_mock_plan(self, 
                         destination: str, 
                         start_date: str,
                         end_date: str, 
                         budget: float, 
                         preferences: str,
                         travelers: int) -> Dict[str, Any]:
        """
        生成模拟旅游计划（用于测试）
        """
        mock_plan = f"""
# {destination}旅行计划 ({start_date} - {end_date})

## 行程概览
- 目的地: {destination}
- 旅行日期: {start_date} 至 {end_date}
- 预算: {budget}元
- 旅行人数: {travelers}人
- 特殊偏好: {preferences or "无"}

## 每日行程安排

### 第一天: 抵达与适应
- 上午: 抵达{destination}，入住酒店
- 下午: 附近轻松游览，适应时差
- 晚上: 品尝当地特色美食

### 第二天: 经典景点游览
- 上午: 参观主要景点A
- 下午: 游览景点B
- 晚上: 自由活动或观看表演

### 第三天: 深度体验
- 上午: 参加当地文化体验活动
- 下午: 购物或休闲
- 晚上: 特色餐厅用餐

### 第四天: 自然风光
- 全天: 前往自然景区游览
- 晚上: 返回市区休息

### 第五天: 离别准备
- 上午: 自由活动，购买纪念品
- 下午: 前往机场，结束愉快旅程

## 住宿推荐
- 市中心商务酒店（方便出行）
- 特色民宿体验（如需要）

## 美食推荐
- 必尝当地特色菜
- 推荐餐厅列表

## 预算分配建议
- 住宿: {budget * 0.4:.0f}元
- 餐饮: {budget * 0.25:.0f}元
- 门票交通: {budget * 0.25:.0f}元
- 购物及其他: {budget * 0.1:.0f}元

## 实用小贴士
- 最佳旅行季节
- 当地风俗习惯
- 紧急联系方式
        """
        
        return {
            "success": True,
            "plan": mock_plan,
            "raw_response": {"mock": True}
        }
    
    def _build_travel_prompt(self, 
                           destination: str, 
                           start_date: str,
                           end_date: str, 
                           budget: float, 
                           preferences: str,
                           travelers: int) -> str:
        """
        构建旅游计划生成提示词
        """
        prompt = f"""
        请为以下旅行需求生成一份详细的旅游计划：
        
        目的地：{destination}
        旅行日期：{start_date} 至 {end_date}
        预算：{budget}元
        旅行人数：{travelers}人
        特殊偏好：{preferences or "无特殊偏好"}
        
        请提供以下信息：
        1. 每日行程安排（包括景点、交通方式、时间安排）
        2. 推荐住宿（类型和区域）
        3. 美食推荐（当地特色餐厅和小吃）
        4. 预算分配建议
        5. 实用小贴士（最佳旅行时间、注意事项等）
        
        要求：
        - 请用中文回复
        - 请提供结构化和易读的旅游计划
        - 请确保内容实用且符合预算
        - 如有日期信息，请具体到日期
        """
        
        return prompt
    
    async def close(self):
        """
        关闭HTTP客户端
        """
        await self.client.aclose()

    async def analyze_budget(self, plan, expenses) -> Dict[str, Any]:
        """
        分析旅行预算和开销
        
        Args:
            plan: 旅行计划对象
            expenses: 开销列表
            
        Returns:
            包含预算分析结果的字典
        """
        # 如果没有配置API密钥，返回模拟数据
        if not self.api_key or not self.api_endpoint or "example.com" in self.api_endpoint:
            return self._generate_mock_budget_analysis(plan, expenses)
        
        # 构建预算分析提示词
        prompt = self._build_budget_analysis_prompt(plan, expenses)
        
        # 根据API端点判断使用哪种服务
        api_endpoint = self.api_endpoint or ""  # 确保不是None
        if "dashscope" in api_endpoint or "aliyuncs" in api_endpoint:
            # 使用阿里云百炼平台
            return await self._analyze_budget_with_dashscope(prompt)
        else:
            # 默认使用OpenAI格式
            return await self._analyze_budget_with_openai(prompt)
    
    async def _analyze_budget_with_openai(self, prompt: str) -> Dict[str, Any]:
        """
        使用OpenAI格式API进行预算分析
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的财务分析师，专门分析旅行预算。请用中文回复，提供结构化和易读的预算分析报告。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1500
        }
        
        try:
            response = await self.client.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            result = response.json()
            analysis_content = result["choices"][0]["message"]["content"]
            
            return {
                "success": True,
                "analysis": analysis_content,
                "raw_response": result
            }
            
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "请求AI服务超时，请稍后重试",
                "analysis": None
            }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"网络请求错误: {str(e)}",
                "analysis": None
            }
        except KeyError as e:
            return {
                "success": False,
                "error": f"AI服务返回格式错误: {str(e)}",
                "analysis": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"预算分析时发生未知错误: {str(e)}",
                "analysis": None
            }
    
    async def _analyze_budget_with_dashscope(self, prompt: str) -> Dict[str, Any]:
        """
        使用阿里云百炼平台进行预算分析
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "qwen-turbo",
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的财务分析师，专门分析旅行预算。请用中文回复，提供结构化和易读的预算分析报告。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            "parameters": {
                "temperature": 0.3,
                "max_tokens": 1500
            }
        }
        
        try:
            response = await self.client.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            result = response.json()
            analysis_content = result["output"]["text"]
            
            return {
                "success": True,
                "analysis": analysis_content,
                "raw_response": result
            }
            
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "请求AI服务超时，请稍后重试",
                "analysis": None
            }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"网络请求错误: {str(e)}",
                "analysis": None
            }
        except KeyError as e:
            return {
                "success": False,
                "error": f"AI服务返回格式错误: {str(e)}",
                "analysis": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"预算分析时发生未知错误: {str(e)}",
                "analysis": None
            }
    
    def _generate_mock_budget_analysis(self, plan, expenses) -> Dict[str, Any]:
        """
        生成模拟预算分析（用于测试）
        """
        total_expenses = sum(expense.amount for expense in expenses)
        remaining_budget = plan.budget - total_expenses
        
        mock_analysis = f"""
# 旅行预算分析报告

## 预算概况
- 计划总预算: {plan.budget:.2f}元
- 已花费金额: {total_expenses:.2f}元
- 剩余预算: {remaining_budget:.2f}元
- 预算使用率: {(total_expenses / plan.budget * 100):.1f}%

## 开销分类分析
"""
        
        # 按类别统计开销
        category_totals = {}
        for expense in expenses:
            if expense.category in category_totals:
                category_totals[expense.category] += expense.amount
            else:
                category_totals[expense.category] = expense.amount
        
        for category, amount in category_totals.items():
            percentage = (amount / plan.budget * 100)
            mock_analysis += f"- {category}: {amount:.2f}元 ({percentage:.1f}%)\n"
        
        mock_analysis += "\n## 分析建议\n"
        
        if remaining_budget < 0:
            mock_analysis += "⚠️ 警告：您已超出预算，请注意控制开销！\n"
        elif remaining_budget < plan.budget * 0.2:
            mock_analysis += "⚠️ 提醒：您的预算余额较低，请合理安排剩余开销。\n"
        else:
            mock_analysis += "✅ 良好：您的预算使用情况正常。\n"
        
        # 根据类别提供具体建议
        if "餐饮" in category_totals and category_totals["餐饮"] > plan.budget * 0.3:
            mock_analysis += "- 餐饮开销占比过高，建议尝试性价比更高的餐厅或减少外出就餐次数。\n"
        
        if "购物" in category_totals and category_totals["购物"] > plan.budget * 0.2:
            mock_analysis += "- 购物开销较大，建议制定购物清单，避免冲动消费。\n"
        
        if remaining_budget > plan.budget * 0.3:
            mock_analysis += f"- 您的剩余预算较为充足({remaining_budget:.2f}元)，可以考虑增加一些体验项目。\n"
        
        mock_analysis += "\n## 优化建议\n"
        mock_analysis += "1. 使用记账应用实时记录开销\n"
        mock_analysis += "2. 设置每日开销提醒\n"
        mock_analysis += "3. 寻找免费或低成本的替代活动\n"
        mock_analysis += "4. 提前预订门票和交通以获取折扣\n"
        
        return {
            "success": True,
            "analysis": mock_analysis,
            "raw_response": {"mock": True}
        }
    
    def _build_budget_analysis_prompt(self, plan, expenses) -> str:
        """
        构建预算分析提示词
        """
        prompt = f"""
        请为以下旅行计划和开销记录生成一份详细的预算分析报告：
        
        旅行计划：
        - 目的地：{plan.destination}
        - 总预算：{plan.budget}元
        - 旅行日期：{plan.start_date} 至 {plan.end_date}
        
        开销记录：
        """
        
        total_expenses = 0
        category_totals = {}
        
        for expense in expenses:
            prompt += f"- {expense.category}: {expense.amount}元 ({expense.description})\n"
            total_expenses += expense.amount
            if expense.category in category_totals:
                category_totals[expense.category] += expense.amount
            else:
                category_totals[expense.category] = expense.amount
        
        prompt += f"\n总计开销：{total_expenses}元\n"
        prompt += f"剩余预算：{plan.budget - total_expenses}元\n\n"
        
        prompt += """
        请提供以下信息：
        1. 预算概况（总预算、已花费、剩余预算、使用率）
        2. 开销分类分析（各类别开销占比）
        3. 预算使用情况评估
        4. 具体的优化建议和提醒
        
        要求：
        - 请用中文回复
        - 请提供结构化和易读的分析报告
        - 如有预算超支风险，请给出明确警告
        - 提供实用的预算管理建议
        """
        
        return prompt

# 创建全局实例
llm_service = LLMService()