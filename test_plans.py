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
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=plan_data, headers=headers)
    return response

def get_travel_plans(token):
    """获取旅行计划列表"""
    url = f"{BASE_URL}/api/plans/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response

def delete_travel_plan(token, plan_id):
    """删除旅行计划"""
    url = f"{BASE_URL}/api/plans/{plan_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers)
    return response

def main():
    # 注册新用户
    print("注册新用户...")
    reg_response = register_user("testuser", "test@example.com", "password123")
    print(f"注册响应: {reg_response.status_code} - {reg_response.text}")
    
    # 登录
    print("\n用户登录...")
    login_response = login_user("testuser", "password123")
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data["access_token"]
        print(f"登录成功，令牌: {token}")
        
        # 创建旅行计划
        print("\n创建旅行计划...")
        plan_data = {
            "title": "测试旅行计划",
            "destination": "北京",
            "start_date": "2025-12-01T00:00:00",
            "end_date": "2025-12-07T00:00:00",
            "budget": 5000.0,
            "preferences": "历史文化，美食"
        }
        create_response = create_travel_plan(token, plan_data)
        print(f"创建计划响应: {create_response.status_code} - {create_response.text}")
        
        if create_response.status_code == 200:
            created_plan = create_response.json()
            plan_id = created_plan["id"]
            print(f"创建的计划ID: {plan_id}")
            
            # 获取旅行计划列表
            print("\n获取旅行计划列表...")
            get_response = get_travel_plans(token)
            print(f"获取计划响应: {get_response.status_code} - {get_response.text}")
            
            # 删除旅行计划
            print("\n删除旅行计划...")
            delete_response = delete_travel_plan(token, plan_id)
            print(f"删除计划响应: {delete_response.status_code} - {delete_response.text}")
    else:
        print(f"登录失败: {login_response.status_code} - {login_response.text}")

if __name__ == "__main__":
    main()