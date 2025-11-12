import requests
import json

# 测试服务器地址
BASE_URL = "http://localhost:8080"

def register_user(username, email, password):
    """注册新用户"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "username": username,
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    return response

def login_user(username, password):
    """用户登录"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=data)
    return response

def create_travel_plan(token, plan_data):
    """创建旅行计划"""
    url = f"{BASE_URL}/api/plans/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=plan_data, headers=headers)
    return response

def create_expense(token, expense_data):
    """创建费用记录"""
    url = f"{BASE_URL}/api/expenses/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=expense_data, headers=headers)
    return response

def analyze_budget(token, plan_id):
    """分析预算"""
    url = f"{BASE_URL}/api/budget/analyze"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "plan_id": plan_id,
        "expenses": []
    }
    response = requests.post(url, json=data, headers=headers)
    return response

def main():
    # 注册新用户
    print("注册新用户...")
    reg_response = register_user("budgetuser", "budget@example.com", "password123")
    print(f"注册响应: {reg_response.status_code} - {reg_response.text}")
    
    # 登录
    print("\n用户登录...")
    login_response = login_user("budgetuser", "password123")
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data["access_token"]
        print(f"登录成功，令牌: {token}")
        
        # 创建旅行计划
        print("\n创建旅行计划...")
        plan_data = {
            "title": "预算测试计划",
            "destination": "上海",
            "start_date": "2025-12-01T00:00:00",
            "end_date": "2025-12-07T00:00:00",
            "budget": 5000.0,
            "preferences": "购物，美食"
        }
        create_response = create_travel_plan(token, plan_data)
        print(f"创建计划响应: {create_response.status_code} - {create_response.text}")
        
        if create_response.status_code == 200:
            created_plan = create_response.json()
            plan_id = created_plan["id"]
            print(f"创建的计划ID: {plan_id}")
            
            # 创建一些费用记录
            print("\n创建费用记录...")
            expenses = [
                {"plan_id": plan_id, "category": "餐饮", "amount": 150.0, "description": "午餐"},
                {"plan_id": plan_id, "category": "交通", "amount": 80.0, "description": "地铁"},
                {"plan_id": plan_id, "category": "购物", "amount": 600.0, "description": "纪念品"}
            ]
            
            for expense in expenses:
                expense_response = create_expense(token, expense)
                print(f"创建费用响应: {expense_response.status_code} - {expense_response.text}")
            
            # 分析预算
            print("\n分析预算...")
            analyze_response = analyze_budget(token, plan_id)
            print(f"预算分析响应: {analyze_response.status_code}")
            if analyze_response.status_code == 200:
                analysis_data = analyze_response.json()
                print(f"预算分析成功: {analysis_data}")
            else:
                print(f"预算分析失败: {analyze_response.text}")
    else:
        print(f"登录失败: {login_response.status_code} - {login_response.text}")

if __name__ == "__main__":
    main()