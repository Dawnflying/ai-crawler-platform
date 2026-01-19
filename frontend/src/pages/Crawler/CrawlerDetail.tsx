import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Tag,
  Button,
  Space,
  Typography,
  Tabs,
  message,
  Spin,
} from 'antd';
import { EditOutlined, DeleteOutlined, PlayCircleOutlined } from '@ant-design/icons';
import { crawlerApi } from '@/api/crawler';
import { Crawler } from '@/types';
import dayjs from 'dayjs';

const { Title } = Typography;

const CrawlerDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [crawler, setCrawler] = useState<Crawler | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchCrawler(parseInt(id));
    }
  }, [id]);

  const fetchCrawler = async (crawlerId: number) => {
    setLoading(true);
    try {
      const data = await crawlerApi.get(crawlerId);
      setCrawler(data);
    } catch (error) {
      console.error('Failed to fetch crawler:', error);
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!crawler) return;
    try {
      await crawlerApi.delete(crawler.id);
      message.success('删除成功');
      navigate('/crawlers');
    } catch (error) {
      console.error('Failed to delete crawler:', error);
    }
  };

  if (loading) {
    return <Spin size="large" style={{ display: 'flex', justifyContent: 'center', marginTop: 100 }} />;
  }

  if (!crawler) {
    return <div>爬虫不存在</div>;
  }

  const typeMap: Record<string, { text: string; color: string }> = {
    http: { text: 'HTTP 爬虫', color: 'blue' },
    api: { text: 'API 采集', color: 'green' },
    browser: { text: '浏览器自动化', color: 'purple' },
  };

  const statusMap: Record<string, { text: string; color: string }> = {
    active: { text: '活跃', color: 'success' },
    inactive: { text: '未激活', color: 'default' },
    error: { text: '错误', color: 'error' },
  };

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Title level={2}>{crawler.name}</Title>
        <Space>
          <Button
            type="primary"
            icon={<PlayCircleOutlined />}
            onClick={() => message.info('功能开发中')}
          >
            执行任务
          </Button>
          <Button
            icon={<EditOutlined />}
            onClick={() => navigate(`/crawlers/${crawler.id}/edit`)}
          >
            编辑
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={handleDelete}
          >
            删除
          </Button>
        </Space>
      </div>

      <Tabs
        items={[
          {
            key: 'info',
            label: '基本信息',
            children: (
              <Card>
                <Descriptions column={2}>
                  <Descriptions.Item label="爬虫名称">{crawler.name}</Descriptions.Item>
                  <Descriptions.Item label="爬虫类型">
                    <Tag color={typeMap[crawler.type]?.color}>
                      {typeMap[crawler.type]?.text}
                    </Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="状态">
                    <Tag color={statusMap[crawler.status]?.color}>
                      {statusMap[crawler.status]?.text}
                    </Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="版本">v{crawler.version}</Descriptions.Item>
                  <Descriptions.Item label="创建者">{crawler.creator_name}</Descriptions.Item>
                  <Descriptions.Item label="任务数">{crawler.task_count || 0}</Descriptions.Item>
                  <Descriptions.Item label="创建时间">
                    {dayjs(crawler.created_at).format('YYYY-MM-DD HH:mm:ss')}
                  </Descriptions.Item>
                  <Descriptions.Item label="更新时间">
                    {dayjs(crawler.updated_at).format('YYYY-MM-DD HH:mm:ss')}
                  </Descriptions.Item>
                  <Descriptions.Item label="描述" span={2}>
                    {crawler.description || '暂无描述'}
                  </Descriptions.Item>
                  {crawler.tags && crawler.tags.length > 0 && (
                    <Descriptions.Item label="标签" span={2}>
                      {crawler.tags.map((tag) => (
                        <Tag key={tag}>{tag}</Tag>
                      ))}
                    </Descriptions.Item>
                  )}
                </Descriptions>
              </Card>
            ),
          },
          {
            key: 'config',
            label: '配置详情',
            children: (
              <Card>
                <pre style={{ background: '#f5f5f5', padding: 16, borderRadius: 4 }}>
                  {JSON.stringify(crawler.config, null, 2)}
                </pre>
              </Card>
            ),
          },
        ]}
      />
    </Space>
  );
};

export default CrawlerDetail;
