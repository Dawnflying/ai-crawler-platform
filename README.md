# AI 爬虫管理平台

一个企业级的前后端分离爬虫管理、数据采集平台，支持 HTTP 爬虫、API 采集、浏览器自动化三种爬虫类型。

## 功能特性

- ✅ **三种爬虫类型**
  - HTTP 爬虫：适用于静态网页数据采集
  - API 采集：直接调用第三方 API 接口
  - 浏览器自动化：处理 JavaScript 渲染的动态网页

- ✅ **可视化配置**：友好的配置界面，降低使用门槛

- ✅ **任务调度**：支持立即执行和定时任务

- ✅ **实时监控**：WebSocket 实时推送任务状态

- ✅ **数据管理**：数据查看、搜索、导出

- ✅ **权限管理**：基于角色的访问控制

## 技术栈

### 后端
- **框架**：Python FastAPI
- **数据库**：SQLite
- **任务队列**：Celery + Redis
- **爬虫引擎**：Scrapy / Playwright / Requests

### 前端
- **框架**：React 18 + TypeScript
- **UI 库**：Ant Design 5.x
- **状态管理**：Zustand
- **构建工具**：Vite

## 快速开始

### 前置要求

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (可选)

### 使用 Docker Compose (推荐)

1. 克隆项目
```bash
git clone <repository-url>
cd ai-crawler-platform
```

2. 创建数据目录
```bash
mkdir -p data logs
```

3. 启动服务
```bash
docker-compose up -d
```

4. 初始化数据库
```bash
docker-compose exec backend python init_db.py
```

5. 访问应用
- API 文档: http://localhost:8000/api/docs
- 前端界面: http://localhost:3000 (待实现)

### 本地开发

#### 后端开发

1. 创建虚拟环境
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 安装依赖
```bash
pip install -r requirements.txt
playwright install chromium
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的参数
```

4. 初始化数据库
```bash
python init_db.py
```

5. 启动开发服务器
```bash
python run.py
```

API 文档将在 http://localhost:8000/api/docs 可用

#### 前端开发 (待实现)

```bash
cd frontend
npm install
npm run dev
```

## 默认账号

初始化数据库后，系统会创建默认管理员账号：

- **用户名**: admin
- **密码**: admin123
- **邮箱**: admin@example.com

⚠️ 首次登录后请立即修改默认密码！

## API 文档

启动后端服务后，访问以下地址查看完整的 API 文档：

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 项目结构

```
ai-crawler-platform/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # 业务逻辑
│   │   ├── engines/        # 爬虫引擎
│   │   └── main.py         # 主应用
│   ├── requirements.txt    # Python 依赖
│   └── Dockerfile
├── frontend/               # 前端代码 (待实现)
├── docs/                   # 设计文档
├── data/                   # 数据库文件
├── logs/                   # 日志文件
├── docker-compose.yml      # Docker 编排
└── README.md
```

## 开发进度

### 已完成 ✅

- [x] 项目基础架构搭建
- [x] 数据库设计与模型创建
- [x] 用户认证模块 (注册/登录/权限控制)
- [x] 爬虫管理模块 (CRUD API)
- [x] 任务管理模块 (CRUD API)
- [x] Docker 配置

### 进行中 🚧

- [ ] 爬虫引擎实现 (HTTP/API/Browser)
- [ ] 前端项目初始化
- [ ] 前端页面开发

### 待开发 📋

- [ ] Celery 任务调度
- [ ] WebSocket 实时通信
- [ ] 数据导出功能
- [ ] 告警通知
- [ ] 爬虫模板库
- [ ] 监控 Dashboard

## 参考文档

详细的设计文档请查看 `docs/` 目录：

- [产品设计文档总览](docs/README.md)
- [数据库设计文档](docs/数据库设计文档.md)
- [产品功能清单](docs/产品功能清单.md)
- [爬虫管理模块详细设计](docs/爬虫管理模块详细设计.md)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
