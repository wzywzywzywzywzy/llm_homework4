# AI Travel Planner

一个基于AI的旅行规划Web应用程序，支持语音输入、智能行程规划和预算管理。

## 功能特性

1. 智能行程规划 - 通过语音或文字输入旅行需求，AI自动生成个性化旅行路线
2. 费用预算与管理 - AI进行预算分析，记录旅行开销
3. 用户管理系统 - 注册登录，云端行程同步

## 技术栈

- 后端: FastAPI (Python)
- 前端: HTML, CSS, JavaScript
- 数据库: SQLite (可替换为其他数据库)
- 认证: JWT
- 语音识别: 科大讯飞API或其他语音识别服务
- 地图服务: 高德地图API或百度地图API
- AI服务: 阿里云百炼平台或其他大语言模型API

## 项目结构

```
.
├── app/                    # 后端应用目录
│   ├── api/               # API路由
│   │   ├── auth_routes.py # 用户认证相关路由
│   │   └── travel_routes.py # 旅行计划相关路由
│   ├── core/              # 核心配置和安全模块
│   │   ├── config.py      # 配置文件
│   │   └── security.py    # 安全相关功能
│   ├── database/          # 数据库配置
│   │   └── database.py    # 数据库连接配置
│   ├── models/            # 数据模型
│   │   └── models.py      # 用户、旅行计划、费用等模型
│   ├── schemas/           # 数据验证模式
│   │   └── schemas.py     # Pydantic模型
│   ├── services/          # 业务逻辑层
│   │   ├── auth_service.py # 认证服务
│   │   ├── auth_utils.py  # 认证工具函数
│   │   ├── user_service.py # 用户相关服务
│   │   ├── travel_service.py # 旅行服务
│   │   └── llm_service.py # 大语言模型服务
│   └── main.py            # 应用入口
├── frontend/              # 前端静态文件
│   └── index.html         # 主页
├── .github/
│   └── workflows/         # GitHub Actions工作流
│       └── docker.yml     # Docker镜像构建流程
├── requirements.txt       # Python依赖
├── Dockerfile             # Docker配置
├── docker-compose.yml     # Docker Compose配置
├── .env.example           # 环境变量示例
├── init_db.py             # 数据库初始化脚本
├── run.py                 # 应用运行入口
└── README.md              # 项目说明
```

## 安装与运行

1. 克隆项目到本地:
   ```
   git clone &lt;repo-url&gt;
   cd ai-travel-planner
   ```

2. 创建虚拟环境并激活:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

4. 配置环境变量:
   复制 `.env.example` 到 `.env` 并填写相应配置

5. 初始化数据库:
   ```
   python init_db.py
   ```

6. 运行应用:
   ```
   python run.py
   ```
   或者使用uvicorn直接运行:
   ```
   uvicorn app.main:app --host localhost --port 8080 --reload
   ```

7. 访问应用:
   打开浏览器访问 http://localhost:8080

## API接口

### 认证接口
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录

### 旅行计划接口
- `GET /api/plans/` - 获取用户的所有旅行计划
- `POST /api/plans/` - 创建新的旅行计划
- `POST /api/plans/generate` - 通过AI生成旅行计划
- `PUT /api/plans/{plan_id}` - 更新旅行计划
- `DELETE /api/plans/{plan_id}` - 删除旅行计划

### 费用管理接口
- `GET /api/expenses/` - 获取用户的费用记录
- `POST /api/expenses/` - 创建新的费用记录

## Docker部署

使用Docker Compose运行:
```
docker-compose up -d
```

或者构建并运行Docker镜像:
```
docker build -t ai-travel-planner .
docker run -p 8080:8080 ai-travel-planner
```

## GitHub Actions

项目包含一个GitHub Actions工作流，用于在推送代码时自动构建Docker镜像并推送到阿里云容器镜像服务。

要使用此功能，请执行以下操作：
1. 在阿里云容器镜像服务控制台创建命名空间和镜像仓库
2. 在GitHub仓库设置中添加以下Secrets:
   - ALIYUN_USERNAME: 你的阿里云账号
   - ALIYUN_PASSWORD: 你的阿里云密码或访问凭证
3. 修改`.github/workflows/docker.yml`文件中的镜像仓库地址为你自己的地址

## 配置说明

在 `.env` 文件中配置以下参数:

- `DATABASE_URL` - 数据库连接URL
- `SECRET_KEY` - JWT密钥
- `SPEECH_API_KEY` - 语音识别API密钥
- `MAP_API_KEY` - 地图API密钥
- `AI_API_KEY` - AI大语言模型API密钥
- `AI_API_ENDPOINT` - AI大语言模型API端点

## 连接大语言模型

本项目支持通过API连接各种大语言模型服务，如阿里云百炼平台、OpenAI等。

### 配置步骤

1. 在 `.env` 文件中设置 `AI_API_KEY` 和 `AI_API_ENDPOINT`
2. 确保API端点格式正确（如：`https://api.openai.com/v1/chat/completions`）
3. 根据使用的API调整 [llm_service.py](file:///C:/Users/34884/Desktop/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E8%BE%85%E5%8A%A9%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B%E4%BD%9C%E4%B8%9A/homework4/app/services/llm_service.py) 中的请求格式

### 支持的模型

- OpenAI GPT系列
- 阿里云通义千问系列
- 百度文心一言
- 其他兼容OpenAI API格式的模型

### 使用方法

通过前端界面或API调用 `/api/plans/generate` 接口，系统将自动调用配置的大语言模型生成个性化旅行计划。

#### OpenAI/GPT配置示例：
```
AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AI_API_ENDPOINT=https://api.openai.com/v1/chat/completions
```

#### 阿里云百炼平台配置示例：
```
AI_API_KEY=your-dashscope-api-key
AI_API_ENDPOINT=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

### 作业提交说明

对于课程作业提交，请使用助教提供的阿里云百炼平台API Key：

```
AI_API_KEY=YOUR_ASSIGNED_API_KEY
AI_API_ENDPOINT=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

此API Key由助教提供，在接下来的3个月内保持有效，确保助教能够正常评估作业。

### API调用示例

#### 生成旅行计划
```bash
curl -X POST "http://localhost:8080/api/plans/generate" \
     -H "Content-Type: application/json" \
     -d '{
           "destination": "日本",
           "start_date": "2025-11-12",
           "end_date": "2025-11-20",
           "budget": 10000,
           "travelers": 1,
           "preferences": "喜欢美食和动漫，带孩子"
         }'
```

### 工作原理

1. 用户通过前端表单输入旅行需求（目的地、日期、预算、偏好等）
2. 前端通过POST请求将数据发送到 `/api/plans/generate` 端点
3. 后端 [travel_service.py](file:///C:/Users/34884/Desktop/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E8%BE%85%E5%8A%A9%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B%E4%BD%9C%E4%B8%9A/homework4/app/services/travel_service.py) 调用 [llm_service.py](file:///C:/Users/34884/Desktop/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E8%BE%85%E5%8A%A9%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B%E4%BD%9C%E4%B8%9A/homework4/app/services/llm_service.py) 生成旅游计划
4. 根据配置的API端点自动选择合适的请求格式
5. AI生成的计划保存到数据库并返回给用户

### 错误处理

系统包含完善的错误处理机制：
- 网络超时处理
- API格式错误处理
- 参数验证
- 缺失配置提醒
- 异常捕获和用户友好的错误信息

## 前端界面

前端界面包含以下功能模块:

1. 语音输入区域 - 通过麦克风输入旅行需求
2. 文字输入区域 - 手动输入旅行需求
3. 地图展示区域 - 展示旅行路线
4. 旅行计划展示区域 - 显示已生成的旅行计划
5. 费用管理区域 - 记录和管理旅行开销

## 扩展功能

项目设计支持以下扩展功能:

1. 集成科大讯飞等语音识别API
2. 集成高德地图或百度地图API
3. 集成阿里云百炼平台等大语言模型API
4. 添加更多个性化推荐算法
5. 实现多设备数据同步
6. 添加更多费用分类和统计功能