import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Typography, Space, Table } from 'antd';
import {
  BugOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { crawlerApi } from '@/api/crawler';
import { taskApi } from '@/api/task';
import { Crawler, Task } from '@/types';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import 'dayjs/locale/zh-cn';

dayjs.extend(relativeTime);
dayjs.locale('zh-cn');

const { Title } = Typography;

const Dashboard: React.FC = () => {
  const [crawlers, setCrawlers] = useState<Crawler[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [crawlersData, tasksData] = await Promise.all([
        crawlerApi.list({ page: 1, page_size: 100 }),
        taskApi.list({ page: 1, page_size: 10 }),
      ]);
      setCrawlers(crawlersData);
      setTasks(tasksData);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate statistics
  const totalCrawlers = crawlers.length;
  const activeCrawlers = crawlers.filter((c) => c.status === 'active').length;
  const totalTasks = tasks.length;
  const runningTasks = tasks.filter((t) => t.status === 'running').length;
  const completedTasks = tasks.filter((t) => t.status === 'completed').length;
  const failedTasks = tasks.filter((t) => t.status === 'failed').length;

  // Recent tasks table columns
  const taskColumns = [
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '爬虫',
      dataIndex: 'crawler_name',
      key: 'crawler_name',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const statusMap: Record<string, { text: string; color: string }> = {
          pending: { text: '待执行', color: 'blue' },
          running: { text: '运行中', color: 'orange' },
          completed: { text: '已完成', color: 'green' },
          failed: { text: '失败', color: 'red' },
          cancelled: { text: '已取消', color: 'gray' },
        };
        const { text, color } = statusMap[status] || { text: status, color: 'default' };
        return <span style={{ color }}>{text}</span>;
      },
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (time: string) => dayjs(time).fromNow(),
    },
  ];

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <Title level={2}>控制台</Title>

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="总爬虫数"
              value={totalCrawlers}
              prefix={<BugOutlined />}
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="活跃爬虫"
              value={activeCrawlers}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#3f8600' }}
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="运行中任务"
              value={runningTasks}
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#1890ff' }}
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="失败任务"
              value={failedTasks}
              prefix={<CloseCircleOutlined />}
              valueStyle={{ color: '#cf1322' }}
              loading={loading}
            />
          </Card>
        </Col>
      </Row>

      <Card title="最近任务" loading={loading}>
        <Table
          dataSource={tasks}
          columns={taskColumns}
          rowKey="id"
          pagination={false}
        />
      </Card>
    </Space>
  );
};

export default Dashboard;
