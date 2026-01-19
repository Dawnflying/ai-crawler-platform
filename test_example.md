# 爬虫测试示例

本文档提供一个完整的测试示例，演示如何使用平台爬取数据。

## 测试网站

我们使用 `http://quotes.toscrape.com` 作为测试网站。这是一个专门用于学习爬虫的网站，包含名人名言数据。

## 方法一：通过平台界面创建爬虫

### 步骤 1：登录平台

访问 `http://localhost:3000` 并使用以下凭据登录：
- 用户名：`admin`
- 密码：`admin123`

### 步骤 2：创建爬虫

1. 点击左侧菜单"爬虫管理"
2. 点击右上角"创建爬虫"按钮
3. 选择"HTTP 爬虫"类型
4. 填写基本信息：
   - 爬虫名称：`名言爬虫测试`
   - 描述：`爬取quotes.toscrape.com网站的名言数据`
   - 标签：`测试`, `名言`

5. 配置参数：
   - 目标 URL：`http://quotes.toscrape.com/page/1/`
   - 请求方法：`GET`

6. 点击"创建爬虫"

### 步骤 3：创建任务并执行

1. 在爬虫列表中找到刚创建的爬虫
2. 点击"详情"进入爬虫详情页
3. 点击"执行任务"按钮（或在任务管理中创建新任务）
4. 等待任务执行完成
5. 查看任务详情和执行日志

## 方法二：使用API创建和执行

### 1. 获取 Token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

响应示例：
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 2. 创建爬虫

```bash
curl -X POST "http://localhost:8000/api/crawlers" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "名言爬虫测试",
    "description": "爬取quotes.toscrape.com网站的名言数据",
    "type": "http",
    "config": {
      "type": "http",
      "base_url": "http://quotes.toscrape.com/page/1/",
      "method": "GET",
      "extract_rules": [
        {
          "field": "quote",
          "type": "css",
          "selector": ".quote .text",
          "multiple": false
        },
        {
          "field": "author",
          "type": "css",
          "selector": ".quote .author",
          "multiple": false
        },
        {
          "field": "tags",
          "type": "css",
          "selector": ".quote .tags .tag",
          "multiple": true
        }
      ],
      "pagination": {
        "enabled": true,
        "type": "url_path",
        "param": "page",
        "start": 1,
        "end": 3
      },
      "anti_crawl": {
        "delay": {
          "min": 0.5,
          "max": 1.5
        }
      }
    },
    "tags": ["测试", "名言"]
  }'
```

### 3. 创建任务

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "crawler_id": 1,
    "name": "名言爬虫任务",
    "schedule_type": "manual"
  }'
```

### 4. 执行任务

```bash
curl -X POST "http://localhost:8000/api/tasks/1/execute" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. 查看任务详情

```bash
curl -X GET "http://localhost:8000/api/tasks/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 6. 查看任务日志

```bash
curl -X GET "http://localhost:8000/api/tasks/1/logs" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 方法三：使用测试脚本

在后端目录运行测试脚本：

```bash
cd backend
python test_crawler.py
```

该脚本会：
1. 检查目标网站是否可访问
2. 使用 HTTP 爬虫引擎爬取数据
3. 打印爬取结果
4. 将完整数据保存到 `crawler_test_results.json`

## 预期结果

成功执行后，您应该能看到：

### 控制台输出
```
============================================================
测试爬虫：爬取名言网站 (quotes.toscrape.com)
============================================================

✅ 爬取完成！共获取 30 条数据

数据 1:
  名言: "The world as we have created it is a process..."
  作者: Albert Einstein
  标签: change, deep-thoughts, thinking, world
  来源: http://quotes.toscrape.com/page/1/

...
```

### 数据库记录
- 任务状态更新为"completed"
- crawl_data 表中插入爬取的数据
- task_logs 表中记录执行日志

### JSON 文件
生成 `crawler_test_results.json` 文件，包含所有爬取的数据。

## 配置说明

### extract_rules（提取规则）

每个规则包含：
- `field`: 字段名称
- `type`: 选择器类型（css/xpath）
- `selector`: 选择器表达式
- `multiple`: 是否提取多个值
- `attribute`: 提取元素的属性（可选，不填则提取文本）

### pagination（分页配置）

- `enabled`: 是否启用分页
- `type`: 分页类型（url_param/url_path）
- `param`: 参数名称
- `start`: 起始页码
- `end`: 结束页码

### anti_crawl（反爬虫策略）

- `delay`: 请求延迟
  - `min`: 最小延迟（秒）
  - `max`: 最大延迟（秒）
- `concurrent`: 并发数（默认1）

## 故障排除

### 1. 网站无法访问

如果 `quotes.toscrape.com` 无法访问，可以使用其他测试网站：
- `http://books.toscrape.com` - 图书数据
- `https://httpbin.org` - HTTP 测试服务

### 2. 提取不到数据

检查：
- CSS 选择器是否正确
- 网站HTML结构是否有变化
- 是否需要等待JavaScript加载（考虑使用浏览器自动化）

### 3. 任务执行失败

查看：
- 任务日志中的详细错误信息
- 后端服务日志
- 网络连接是否正常

## 下一步

- 尝试爬取其他网站
- 实现更复杂的提取规则
- 配置定时任务
- 导出数据到文件
