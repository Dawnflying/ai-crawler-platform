"""
测试爬虫功能的脚本
爬取示例网站：http://quotes.toscrape.com (一个专门用于学习爬虫的网站)
"""
import requests
import json
from app.engines.http_crawler import HTTPCrawler


def test_quotes_crawler():
    """测试爬取名言网站"""
    print("=" * 60)
    print("测试爬虫：爬取名言网站 (quotes.toscrape.com)")
    print("=" * 60)

    # 配置爬虫
    config = {
        "type": "http",
        "base_url": "http://quotes.toscrape.com",
        "method": "GET",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "extract_rules": [
            {
                "field": "quote",
                "type": "css",
                "selector": ".quote .text",
                "multiple": False
            },
            {
                "field": "author",
                "type": "css",
                "selector": ".quote .author",
                "multiple": False
            },
            {
                "field": "tags",
                "type": "css",
                "selector": ".quote .tags .tag",
                "multiple": True
            }
        ],
        "pagination": {
            "enabled": True,
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
    }

    # 创建爬虫
    crawler = HTTPCrawler(config)

    try:
        # 执行爬取
        results = crawler.crawl("http://quotes.toscrape.com/page/1/", max_pages=3)

        # 打印结果
        print(f"\n✅ 爬取完成！共获取 {len(results)} 条数据\n")

        # 显示前5条数据
        for i, data in enumerate(results[:5], 1):
            print(f"数据 {i}:")
            print(f"  名言: {data.get('quote', 'N/A')}")
            print(f"  作者: {data.get('author', 'N/A')}")
            print(f"  标签: {', '.join(data.get('tags', []))}")
            print(f"  来源: {data.get('_url', 'N/A')}")
            print()

        # 保存结果到文件
        with open('crawler_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"📁 完整数据已保存到: crawler_test_results.json")

        return True

    except Exception as e:
        print(f"❌ 爬取失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        crawler.close()


def test_http_status():
    """测试目标网站是否可访问"""
    print("\n检查目标网站状态...")
    try:
        response = requests.get("http://quotes.toscrape.com", timeout=10)
        print(f"✅ 网站可访问 (状态码: {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ 网站不可访问: {str(e)}")
        return False


if __name__ == "__main__":
    # 先测试网站是否可访问
    if test_http_status():
        # 执行爬虫测试
        test_quotes_crawler()
    else:
        print("\n⚠️  目标网站不可访问，无法进行测试")
