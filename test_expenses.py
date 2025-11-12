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

def get_expenses(token, plan_id=None):
    """获取费用记录"""
    url = f"{BASE_URL}/api/expenses/"
    if plan_id:
        url += f"?plan_id={plan_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response

def main():
    # 注册新用户
    print("注册新用户...")
    reg_response = register_user("expenseuser", "expense@example.com", "password123")
    print(f"注册响应: {reg_response.status_code} - {reg_response.text}")
    
    # 登录
    print("\n用户登录...")
    login_response = login_user("expenseuser", "password123")
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data["access_token"]
        print(f"登录成功，令牌: {token}")
        
        # 创建旅行计划
        print("\n创建旅行计划...")
        plan_data = {
            "title": "费用测试计划",
            "destination": "北京",
            "start_date": "2025-12-01T00:00:00",
            "end_date": "2025-12-07T00:00:00",
            "budget": 3000.0,
            "preferences": "历史文化，美食"
        }
        create_response = create_travel_plan(token, plan_data)
        print(f"创建计划响应: {create_response.status_code} - {create_response.text}")
        
        if create_response.status_code == 200:
            created_plan = create_response.json()
            plan_id = created_plan["id"]
            print(f"创建的计划ID: {plan_id}")
            
            # 创建费用记录
            print("\n创建费用记录...")
            expense_data = {
                "plan_id": plan_id,
                "category": "餐饮",
                "amount": 128.50,
                "description": "午餐 - 烤鸭"
            }
            expense_response = create_expense(token, expense_data)
            print(f"创建费用响应: {expense_response.status_code} - {expense_response.text}")
            
            if expense_response.status_code == 200:
                expense_result = expense_response.json()
                print(f"费用记录创建成功: {expense_result}")
                
                # 获取费用记录
                print("\n获取费用记录...")
                get_expense_response = get_expenses(token, plan_id)
                print(f"获取费用响应: {get_expense_response.status_code} - {get_expense_response.text}")
                
                if get_expense_response.status_code == 200:
                    expenses = get_expense_response.json()
                    print(f"获取到 {len(expenses)} 条费用记录")
                    for expense in expenses:
                        print(f"  - {expense['category']}: {expense['amount']}元 ({expense['description']})")
            else:
                print("费用记录创建失败")
        else:
            print("旅行计划创建失败")
    else:
        print(f"登录失败: {login_response.status_code} - {login_response.text}")

if __name__ == "__main__":
    main()