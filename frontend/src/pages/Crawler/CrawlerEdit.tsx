import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Form,
  Input,
  Select,
  Button,
  Space,
  Typography,
  message,
  Spin,
} from 'antd';
import { crawlerApi } from '@/api/crawler';
import { Crawler } from '@/types';

const { Title } = Typography;
const { TextArea } = Input;

const CrawlerEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [crawler, setCrawler] = useState<Crawler | null>(null);

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
      form.setFieldsValue({
        name: data.name,
        description: data.description,
        status: data.status,
        tags: data.tags,
      });
    } catch (error) {
      console.error('Failed to fetch crawler:', error);
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  const onFinish = async (values: any) => {
    if (!crawler) return;
    setSubmitting(true);
    try {
      await crawlerApi.update(crawler.id, {
        name: values.name,
        description: values.description,
        status: values.status,
        tags: values.tags,
      });
      message.success('更新成功');
      navigate(`/crawlers/${crawler.id}`);
    } catch (error) {
      console.error('Failed to update crawler:', error);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <Spin size="large" style={{ display: 'flex', justifyContent: 'center', marginTop: 100 }} />;
  }

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <Title level={2}>编辑爬虫</Title>

      <Card>
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
        >
          <Form.Item
            label="爬虫名称"
            name="name"
            rules={[{ required: true, message: '请输入爬虫名称' }]}
          >
            <Input placeholder="请输入爬虫名称" />
          </Form.Item>

          <Form.Item
            label="描述"
            name="description"
          >
            <TextArea rows={4} placeholder="请输入爬虫描述" />
          </Form.Item>

          <Form.Item
            label="状态"
            name="status"
            rules={[{ required: true, message: '请选择状态' }]}
          >
            <Select>
              <Select.Option value="active">活跃</Select.Option>
              <Select.Option value="inactive">未激活</Select.Option>
              <Select.Option value="error">错误</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="标签"
            name="tags"
          >
            <Select
              mode="tags"
              placeholder="输入标签后按回车添加"
              style={{ width: '100%' }}
            />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={submitting}>
                保存
              </Button>
              <Button onClick={() => navigate(`/crawlers/${id}`)}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </Space>
  );
};

export default CrawlerEdit;
