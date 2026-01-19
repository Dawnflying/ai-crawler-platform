import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Form,
  Input,
  Select,
  Button,
  Space,
  Typography,
  message,
  Steps,
  Radio,
} from 'antd';
import { crawlerApi } from '@/api/crawler';
import { CrawlerCreate as CrawlerCreateType } from '@/types';

const { Title, Paragraph } = Typography;
const { TextArea } = Input;

const CrawlerCreate: React.FC = () => {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [crawlerType, setCrawlerType] = useState<'http' | 'api' | 'browser'>('http');

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      const crawlerData: CrawlerCreateType = {
        name: values.name,
        description: values.description,
        type: crawlerType,
        config: {
          type: crawlerType,
          ...values.config,
        },
        tags: values.tags,
      };

      await crawlerApi.create(crawlerData);
      message.success('爬虫创建成功');
      navigate('/crawlers');
    } catch (error) {
      console.error('Failed to create crawler:', error);
    } finally {
      setLoading(false);
    }
  };

  const typeOptions = [
    {
      value: 'http',
      label: 'HTTP 爬虫',
      description: '适用于静态网页数据采集',
    },
    {
      value: 'api',
      label: 'API 采集',
      description: '直接调用第三方 API 接口',
    },
    {
      value: 'browser',
      label: '浏览器自动化',
      description: 'JavaScript 渲染的动态网页',
    },
  ];

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <div>
        <Title level={2}>创建爬虫</Title>
        <Paragraph type="secondary">
          选择爬虫类型并配置基本信息
        </Paragraph>
      </div>

      <Card>
        <Steps
          current={currentStep}
          items={[
            { title: '选择类型' },
            { title: '基本信息' },
            { title: '配置参数' },
          ]}
          style={{ marginBottom: 32 }}
        />

        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
        >
          {currentStep === 0 && (
            <div>
              <Title level={4}>选择爬虫类型</Title>
              <Radio.Group
                value={crawlerType}
                onChange={(e) => setCrawlerType(e.target.value)}
                style={{ width: '100%' }}
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  {typeOptions.map((option) => (
                    <Card
                      key={option.value}
                      hoverable
                      style={{
                        border: crawlerType === option.value ? '2px solid #1890ff' : '1px solid #d9d9d9',
                      }}
                      onClick={() => setCrawlerType(option.value as any)}
                    >
                      <Radio value={option.value}>
                        <Space direction="vertical" size={0}>
                          <strong>{option.label}</strong>
                          <span style={{ color: '#8c8c8c', fontSize: 12 }}>
                            {option.description}
                          </span>
                        </Space>
                      </Radio>
                    </Card>
                  ))}
                </Space>
              </Radio.Group>
              <div style={{ marginTop: 24 }}>
                <Button type="primary" onClick={() => setCurrentStep(1)}>
                  下一步
                </Button>
              </div>
            </div>
          )}

          {currentStep === 1 && (
            <div>
              <Title level={4}>基本信息</Title>
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
                label="标签"
                name="tags"
              >
                <Select
                  mode="tags"
                  placeholder="输入标签后按回车添加"
                  style={{ width: '100%' }}
                />
              </Form.Item>

              <Space>
                <Button onClick={() => setCurrentStep(0)}>
                  上一步
                </Button>
                <Button type="primary" onClick={() => setCurrentStep(2)}>
                  下一步
                </Button>
              </Space>
            </div>
          )}

          {currentStep === 2 && (
            <div>
              <Title level={4}>配置参数</Title>
              <Paragraph type="secondary">
                配置爬虫的详细参数（此处为简化版本，实际应根据爬虫类型显示不同的配置项）
              </Paragraph>

              {crawlerType === 'http' && (
                <>
                  <Form.Item
                    label="目标 URL"
                    name={['config', 'base_url']}
                    rules={[{ required: true, message: '请输入目标 URL' }]}
                  >
                    <Input placeholder="https://example.com" />
                  </Form.Item>

                  <Form.Item
                    label="请求方法"
                    name={['config', 'method']}
                    initialValue="GET"
                  >
                    <Select>
                      <Select.Option value="GET">GET</Select.Option>
                      <Select.Option value="POST">POST</Select.Option>
                    </Select>
                  </Form.Item>
                </>
              )}

              {crawlerType === 'api' && (
                <>
                  <Form.Item
                    label="API 地址"
                    name={['config', 'url']}
                    rules={[{ required: true, message: '请输入 API 地址' }]}
                  >
                    <Input placeholder="https://api.example.com/v1/data" />
                  </Form.Item>

                  <Form.Item
                    label="请求方法"
                    name={['config', 'method']}
                    initialValue="GET"
                  >
                    <Select>
                      <Select.Option value="GET">GET</Select.Option>
                      <Select.Option value="POST">POST</Select.Option>
                    </Select>
                  </Form.Item>
                </>
              )}

              {crawlerType === 'browser' && (
                <>
                  <Form.Item
                    label="目标 URL"
                    name={['config', 'url']}
                    rules={[{ required: true, message: '请输入目标 URL' }]}
                  >
                    <Input placeholder="https://example.com" />
                  </Form.Item>

                  <Form.Item
                    label="浏览器类型"
                    name={['config', 'browser']}
                    initialValue="chrome"
                  >
                    <Select>
                      <Select.Option value="chrome">Chrome</Select.Option>
                      <Select.Option value="firefox">Firefox</Select.Option>
                    </Select>
                  </Form.Item>

                  <Form.Item
                    label="无头模式"
                    name={['config', 'headless']}
                    initialValue={true}
                  >
                    <Radio.Group>
                      <Radio value={true}>是</Radio>
                      <Radio value={false}>否</Radio>
                    </Radio.Group>
                  </Form.Item>
                </>
              )}

              <Space>
                <Button onClick={() => setCurrentStep(1)}>
                  上一步
                </Button>
                <Button type="primary" htmlType="submit" loading={loading}>
                  创建爬虫
                </Button>
                <Button onClick={() => navigate('/crawlers')}>
                  取消
                </Button>
              </Space>
            </div>
          )}
        </Form>
      </Card>
    </Space>
  );
};

export default CrawlerCreate;
