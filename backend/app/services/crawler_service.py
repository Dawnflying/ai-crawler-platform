"""
Crawler Service - 爬虫服务层
"""
import json
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.task import Task, TaskLog
from app.models.data import CrawlData
from app.models.crawler import Crawler
from app.engines.http_crawler import HTTPCrawler


class CrawlerService:
    """爬虫服务"""

    def __init__(self, db: Session):
        self.db = db

    def execute_crawler(self, task_id: int) -> Dict[str, Any]:
        """
        执行爬虫任务

        Args:
            task_id: 任务ID

        Returns:
            执行结果
        """
        # 获取任务
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return {'success': False, 'error': 'Task not found'}

        # 获取爬虫配置
        crawler = self.db.query(Crawler).filter(Crawler.id == task.crawler_id).first()
        if not crawler:
            return {'success': False, 'error': 'Crawler not found'}

        # 更新任务状态
        task.status = 'running'
        task.started_at = datetime.utcnow()
        self.db.commit()

        # 记录日志
        self.log(task_id, 'INFO', f'开始执行爬虫任务: {task.name}')

        try:
            # 解析配置
            config = json.loads(crawler.config)
            crawler_type = config.get('type', crawler.type)

            # 根据类型执行爬虫
            if crawler_type == 'http':
                result = self._execute_http_crawler(task, config)
            elif crawler_type == 'api':
                result = self._execute_api_crawler(task, config)
            elif crawler_type == 'browser':
                result = self._execute_browser_crawler(task, config)
            else:
                raise ValueError(f'Unknown crawler type: {crawler_type}')

            # 更新任务状态
            task.status = 'completed'
            task.completed_at = datetime.utcnow()
            task.duration = int((task.completed_at - task.started_at).total_seconds())

            self.db.commit()

            self.log(task_id, 'INFO', f'任务执行完成，成功: {task.success_items}, 失败: {task.failed_items}')

            return {
                'success': True,
                'total_items': task.total_items,
                'success_items': task.success_items,
                'failed_items': task.failed_items
            }

        except Exception as e:
            # 更新任务状态为失败
            task.status = 'failed'
            task.error_message = str(e)
            task.completed_at = datetime.utcnow()
            if task.started_at:
                task.duration = int((task.completed_at - task.started_at).total_seconds())
            self.db.commit()

            self.log(task_id, 'ERROR', f'任务执行失败: {str(e)}')

            return {'success': False, 'error': str(e)}

    def _execute_http_crawler(self, task: Task, config: Dict[str, Any]) -> bool:
        """执行HTTP爬虫"""
        self.log(task.id, 'INFO', '启动HTTP爬虫引擎')

        # 创建爬虫实例
        crawler = HTTPCrawler(config)

        # 获取起始URL
        base_url = config.get('base_url')
        if not base_url:
            raise ValueError('Missing base_url in config')

        # 执行爬取
        try:
            results = crawler.crawl(base_url, max_pages=10)

            # 保存数据
            success_count = 0
            failed_count = 0

            for data in results:
                try:
                    # 生成数据哈希
                    data_hash = crawler.generate_hash(data)

                    # 保存到数据库
                    crawl_data = CrawlData(
                        crawler_id=task.crawler_id,
                        task_id=task.id,
                        data=json.dumps(data, ensure_ascii=False),
                        data_hash=data_hash,
                        url=data.get('_url'),
                        status='success'
                    )
                    self.db.add(crawl_data)
                    success_count += 1

                except Exception as e:
                    self.log(task.id, 'ERROR', f'保存数据失败: {str(e)}')
                    failed_count += 1

            # 更新任务统计
            task.total_items = len(results)
            task.success_items = success_count
            task.failed_items = failed_count

            self.db.commit()

            self.log(task.id, 'INFO', f'HTTP爬虫完成，共爬取 {len(results)} 条数据')

            return True

        finally:
            crawler.close()

    def _execute_api_crawler(self, task: Task, config: Dict[str, Any]) -> bool:
        """执行API采集爬虫"""
        self.log(task.id, 'INFO', 'API采集功能开发中...')
        # TODO: 实现API采集
        return True

    def _execute_browser_crawler(self, task: Task, config: Dict[str, Any]) -> bool:
        """执行浏览器自动化爬虫"""
        self.log(task.id, 'INFO', '浏览器自动化功能开发中...')
        # TODO: 实现浏览器自动化
        return True

    def log(self, task_id: int, level: str, message: str, details: Dict[str, Any] = None):
        """
        记录任务日志

        Args:
            task_id: 任务ID
            level: 日志级别
            message: 日志消息
            details: 详细信息
        """
        log = TaskLog(
            task_id=task_id,
            level=level,
            message=message,
            details=json.dumps(details) if details else None
        )
        self.db.add(log)
        self.db.commit()
