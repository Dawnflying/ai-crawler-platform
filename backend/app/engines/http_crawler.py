"""
HTTP Crawler Engine
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import time
import random
import hashlib
import json
from urllib.parse import urljoin, urlparse


class HTTPCrawler:
    """HTTP 爬虫引擎"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化HTTP爬虫

        Args:
            config: 爬虫配置字典
        """
        self.config = config
        self.session = requests.Session()
        self.results: List[Dict[str, Any]] = []

        # 设置默认请求头
        self.session.headers.update({
            'User-Agent': config.get('user_agent',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        })

        # 添加自定义请求头
        if 'headers' in config:
            self.session.headers.update(config['headers'])

        # 设置代理
        if config.get('proxy', {}).get('enabled'):
            proxy_url = config['proxy'].get('url')
            if proxy_url:
                self.session.proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }

    def fetch_page(self, url: str) -> Optional[str]:
        """
        获取网页内容

        Args:
            url: 目标URL

        Returns:
            网页HTML内容，失败返回None
        """
        method = self.config.get('method', 'GET').upper()
        timeout = self.config.get('timeout', 30)

        try:
            if method == 'GET':
                response = self.session.get(url, timeout=timeout)
            elif method == 'POST':
                data = self.config.get('data', {})
                response = self.session.post(url, data=data, timeout=timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            response.encoding = response.apparent_encoding or 'utf-8'
            return response.text

        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def extract_data(self, html: str, url: str) -> Dict[str, Any]:
        """
        从HTML中提取数据

        Args:
            html: HTML内容
            url: 源URL

        Returns:
            提取的数据字典
        """
        soup = BeautifulSoup(html, 'html.parser')
        data = {'_url': url}

        # 获取提取规则
        extract_rules = self.config.get('extract_rules', [])

        for rule in extract_rules:
            field_name = rule.get('field')
            selector_type = rule.get('type', 'css')
            selector = rule.get('selector')
            attribute = rule.get('attribute')
            multiple = rule.get('multiple', False)

            if not field_name or not selector:
                continue

            try:
                if selector_type == 'css':
                    if multiple:
                        elements = soup.select(selector)
                        values = []
                        for elem in elements:
                            if attribute:
                                values.append(elem.get(attribute, ''))
                            else:
                                values.append(elem.get_text(strip=True))
                        data[field_name] = values
                    else:
                        element = soup.select_one(selector)
                        if element:
                            if attribute:
                                data[field_name] = element.get(attribute, '')
                            else:
                                data[field_name] = element.get_text(strip=True)
                        else:
                            data[field_name] = None

                elif selector_type == 'xpath':
                    # XPath需要lxml支持，这里使用CSS选择器作为替代
                    # 实际项目中可以添加lxml依赖并使用xpath
                    pass

            except Exception as e:
                print(f"Error extracting field {field_name}: {str(e)}")
                data[field_name] = None

        return data

    def generate_hash(self, data: Dict[str, Any]) -> str:
        """
        生成数据哈希值用于去重

        Args:
            data: 数据字典

        Returns:
            MD5哈希值
        """
        # 使用URL和主要字段生成哈希
        hash_fields = [data.get('_url', '')]

        # 添加其他字段
        for key, value in data.items():
            if key != '_url' and value:
                hash_fields.append(str(value))

        hash_string = '|'.join(hash_fields)
        return hashlib.md5(hash_string.encode()).hexdigest()

    def crawl(self, start_url: str, max_pages: int = 10) -> List[Dict[str, Any]]:
        """
        执行爬取

        Args:
            start_url: 起始URL
            max_pages: 最大页数

        Returns:
            爬取的数据列表
        """
        self.results = []
        seen_hashes = set()

        # 获取分页配置
        pagination = self.config.get('pagination', {})
        enabled = pagination.get('enabled', False)

        if not enabled:
            # 不分页，只爬取单个页面
            html = self.fetch_page(start_url)
            if html:
                data = self.extract_data(html, start_url)
                data_hash = self.generate_hash(data)

                if data_hash not in seen_hashes:
                    seen_hashes.add(data_hash)
                    self.results.append(data)
        else:
            # 分页爬取
            page_type = pagination.get('type', 'url_param')
            param_name = pagination.get('param', 'page')
            start_page = pagination.get('start', 1)
            end_page = min(pagination.get('end', max_pages), start_page + max_pages - 1)

            for page_num in range(start_page, end_page + 1):
                # 构造分页URL
                if page_type == 'url_param':
                    separator = '&' if '?' in start_url else '?'
                    page_url = f"{start_url}{separator}{param_name}={page_num}"
                elif page_type == 'url_path':
                    page_url = f"{start_url.rstrip('/')}/{page_num}"
                else:
                    page_url = start_url

                print(f"Crawling page {page_num}: {page_url}")

                # 获取页面
                html = self.fetch_page(page_url)
                if not html:
                    break

                # 提取数据
                data = self.extract_data(html, page_url)
                data_hash = self.generate_hash(data)

                # 去重
                if data_hash not in seen_hashes:
                    seen_hashes.add(data_hash)
                    self.results.append(data)

                # 延迟控制
                delay = self.config.get('anti_crawl', {}).get('delay', {})
                if delay:
                    min_delay = delay.get('min', 1)
                    max_delay = delay.get('max', 3)
                    sleep_time = random.uniform(min_delay, max_delay)
                    time.sleep(sleep_time)

        return self.results

    def close(self):
        """关闭会话"""
        self.session.close()
