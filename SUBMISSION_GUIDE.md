# 作业提交指南

## 提交内容

1. GitHub仓库地址
2. 可直接运行的Docker镜像文件
3. 详细运行说明文档

## GitHub仓库要求

请将项目代码提交到GitHub，并确保提交历史完整详细。仓库应包含：

1. 完整的源代码
2. 配置文件模板 (.env.example)
3. 依赖清单 (requirements.txt)
4. Docker配置文件 (Dockerfile, docker-compose.yml)
5. GitHub Actions配置 (.github/workflows/)
6. 测试文件
7. 详细的README文档

## Docker镜像部署

项目通过GitHub Actions自动构建Docker镜像并推送到阿里云镜像仓库。

### 镜像拉取方式

助教可以通过以下命令拉取最新镜像：

```bash
docker pull registry.cn-hangzhou.aliyuncs.com/your-namespace/ai-travel-planner:latest
```

### 本地运行方式

1. 直接运行:
```bash
docker run -p 8080:8080 registry.cn-hangzhou.aliyuncs.com/your-namespace/ai-travel-planner:latest
```

2. 使用Docker Compose运行:
```bash
docker-compose up -d
```

## API Key配置

对于作业评估，使用助教提供的阿里云百炼平台API Key。该Key已在README.md中说明配置方法。

## 提交前检查清单

- [ ] 代码已推送到GitHub，且提交历史完整
- [ ] GitHub Actions配置正确，能够自动构建镜像
- [ ] README文档详细说明了运行方法
- [ ] 包含助教使用的API Key配置说明
- [ ] Docker镜像可以成功构建和运行
- [ ] 应用功能完整，符合作业要求

## 评估注意事项

1. 应用将在3个月内被评估，请确保相关服务在此期间可用
2. API Key由助教提供，学生需在文档中明确指出配置位置
3. 应用应能通过Docker直接运行，无需额外复杂配置