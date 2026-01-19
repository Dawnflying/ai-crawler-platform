# 快速开始指南

本指南将帮助您在 5 分钟内启动并测试 AI 爬虫管理平台。

## 前置要求

- Docker & Docker Compose
- 或者：Python 3.11+ 和 Node.js 18+

## 方式一：使用 Docker（推荐）

### 1. 启动所有服务

```bash
# 克隆项目（如果还没有）
git clone <repository-url>
cd ai-crawler-platform

# 创建必要的目录
mkdir -p data logs

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

等待服务启动（约 1-2 分钟）。

### 2. 初始化数据库

```bash
docker-compose exec backend python init_db.py
```

您应该看到：
```
✓ Database tables created
✓ Default roles initialized
✓ Admin user initialized
  Username: admin
  Password: admin123
✓ System configurations initialized
```

### 3. 访问应用

打开浏览器访问：
- **前端界面**: http://localhost:3000
- **API 文档**: http://localhost:8000/api/docs

### 4. 登录系统

使用默认管理员账号登录：
- 用户名：`admin`
- 密码：`admin123`

⚠️ **重要**：首次登录后请立即修改默认密码！

### 5. 创建第一个爬虫

#### 选择爬虫类型
1. 点击左侧菜单"爬虫管理"
2. 点击"创建爬虫"
3. 选择"HTTP 爬虫"

#### 填写基本信息
- 爬虫名称：`名言爬虫测试`
- 描述：`爬取quotes.toscrape.com的名言数据`
- 标签：`测试`

#### 配置参数
- 目标 URL：`http://quotes.toscrape.com/page/1/`
- 请求方法：`GET`

点击"创建爬虫"。

### 6. 执行爬虫任务

#### 方式 A：在爬虫详情页执行
1. 在爬虫列表中找到刚创建的爬虫
2. 点击"详情"
3. 点击"执行任务"按钮

#### 方式 B：通过任务管理
1. 点击左侧菜单"任务管理"
2. 点击"创建任务"
3. 选择刚创建的爬虫
4. 输入任务名称
5. 点击"创建并执行"

### 7. 查看结果

任务执行后，您可以：
- 在任务详情页查看执行日志
- 在数据管理页查看爬取的数据
- 在 Dashboard 查看统计信息

## 方式二：本地开发模式

### 1. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动后端服务
python run.py
```

后端将在 http://localhost:8000 启动。

### 2. 启动前端

新开一个终端：

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3000 启动。

### 3. 测试爬虫引擎

```bash
cd backend
python test_crawler.py
```

这将运行一个独立的爬虫测试，无需启动完整服务。

## 快速测试爬虫功能

### 使用测试脚本（最简单）

```bash
cd backend
python test_crawler.py
```

该脚本会：
1. 检查测试网站是否可访问
2. 爬取 3 页名言数据
3. 打印爬取结果
4. 保存到 `crawler_test_results.json`

预期输出：
```
检查目标网站状态...
✅ 网站可访问 (状态码: 200)

============================================================
测试爬虫：爬取名言网站 (quotes.toscrape.com)
============================================================

Crawling page 1: http://quotes.toscrape.com/page/1/
Crawling page 2: http://quotes.toscrape.com/page/2/
Crawling page 3: http://quotes.toscrape.com/page/3/

✅ 爬取完成！共获取 30 条数据

数据 1:
  名言: "The world as we have created it..."
  作者: Albert Einstein
  标签: change, deep-thoughts, thinking, world
  来源: http://quotes.toscrape.com/page/1/
...

📁 完整数据已保存到: crawler_test_results.json
```

## 常见问题

### Q1: Docker 服务启动失败？

```bash
# 查看日志
docker-compose logs backend
docker-compose logs frontend

# 重启服务
docker-compose restart
```

### Q2: 前端无法连接后端？

检查：
1. 后端服务是否正常运行
2. 浏览器控制台是否有错误
3. 确认后端运行在 http://localhost:8000

### Q3: 爬虫执行失败？

检查：
1. 目标网站是否可访问
2. 查看任务日志中的详细错误
3. 确认爬虫配置是否正确

### Q4: 数据库初始化失败？

```bash
# 删除旧数据库
rm data/crawler_platform.db

# 重新初始化
docker-compose exec backend python init_db.py
```

## 下一步

现在您已经成功运行了爬虫平台，可以：

1. **学习更多配置选项**
   - 查看 `test_example.md` 了解详细配置
   - 阅读 `docs/` 目录中的设计文档

2. **尝试不同的网站**
   - http://books.toscrape.com - 图书数据
   - https://news.ycombinator.com - 新闻数据

3. **探索高级功能**
   - 配置分页爬取
   - 设置数据提取规则
   - 配置反爬虫策略
   - 设置定时任务

4. **贡献代码**
   - 实现 API 采集爬虫
   - 实现浏览器自动化爬虫
   - 添加数据导出功能
   - 改进 UI 界面

## 获取帮助

- 查看 API 文档：http://localhost:8000/api/docs
- 查看项目 README：[README.md](README.md)
- 查看设计文档：`docs/` 目录
- 提交 Issue：GitHub Issues

祝您使用愉快！🎉
