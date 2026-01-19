import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Space,
  Table,
  Button,
  Tag,
  message,
  Select,
  Card,
  Typography,
  Modal,
  Form,
  Input,
} from 'antd';
import { PlusOutlined, EyeOutlined, StopOutlined } from '@ant-design/icons';
import { taskApi } from '@/api/task';
import { crawlerApi } from '@/api/crawler';
import { Task, Crawler } from '@/types';
import dayjs from 'dayjs';
import type { ColumnsType } from 'antd/es/table';

const { Title } = Typography;

const TaskList: React.FC = () => {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [crawlers, setCrawlers] = useState<Crawler[]>([]);
  const [loading, setLoading] = useState(false);
  const [createModalVisible, setCreateModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [filters, setFilters] = useState({
    crawler_id: undefined as number | undefined,
    status: undefined as string | undefined,
  });

  useEffect(() => {
    fetchTasks();
    fetchCrawlers();
  }, [filters]);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const data = await taskApi.list({
        crawler_id: filters.crawler_id,
        status: filters.status,
        page: 1,
        page_size: 100,
      });
      setTasks(data);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCrawlers = async () => {
    try {
      const data = await crawlerApi.list({ page: 1, page_size: 100 });
      setCrawlers(data);
    } catch (error) {
      console.error('Failed to fetch crawlers:', error);
    }
  };

  const handleCreateTask = async (values: any) => {
    try {
      await taskApi.create({
        crawler_id: values.crawler_id,
        name: values.name,
        schedule_type: 'manual',
      });
      message.success('任务创建成功');
      setCreateModalVisible(false);
      form.resetFields();
      fetchTasks();
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleCancelTask = async (id: number) => {
    try {
      await taskApi.cancel(id);
      message.success('任务已取消');
      fetchTasks();
    } catch (error) {
      console.error('Failed to cancel task:', error);
    }
  };

  const columns: ColumnsType<Task> = [
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <a onClick={() => navigate(`/tasks/${record.id}`)}>{text}</a>
      ),
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
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '进度',
      key: 'progress',
      render: (_, record) => {
        if (record.total_items === 0) return '-';
        const successRate = ((record.success_items / record.total_items) * 100).toFixed(1);
        return `${record.success_items}/${record.total_items} (${successRate}%)`;
      },
    },
    {
      title: '执行时间',
      dataIndex: 'started_at',
      key: 'started_at',
      render: (time: string) => (time ? dayjs(time).format('YYYY-MM-DD HH:mm:ss') : '-'),
    },
    {
      title: '耗时',
      dataIndex: 'duration',
      key: 'duration',
      render: (duration: number) => (duration ? `${duration}s` : '-'),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (time: string) => dayjs(time).format('YYYY-MM-DD HH:mm'),
    },
    {
      title: '操作',
      key: 'action',
      fixed: 'right',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => navigate(`/tasks/${record.id}`)}
          >
            详情
          </Button>
          {(record.status === 'pending' || record.status === 'running') && (
            <Button
              type="link"
              size="small"
              danger
              icon={<StopOutlined />}
              onClick={() => handleCancelTask(record.id)}
            >
              取消
            </Button>
          )}
        </Space>
      ),
    },
  ];

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Title level={2} style={{ margin: 0 }}>任务管理</Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setCreateModalVisible(true)}
        >
          创建任务
        </Button>
      </div>

      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Select
            placeholder="选择爬虫"
            style={{ width: 200 }}
            allowClear
            value={filters.crawler_id}
            onChange={(value) => setFilters({ ...filters, crawler_id: value })}
          >
            {crawlers.map((crawler) => (
              <Select.Option key={crawler.id} value={crawler.id}>
                {crawler.name}
              </Select.Option>
            ))}
          </Select>
          <Select
            placeholder="选择状态"
            style={{ width: 120 }}
            allowClear
            value={filters.status}
            onChange={(value) => setFilters({ ...filters, status: value })}
          >
            <Select.Option value="pending">待执行</Select.Option>
            <Select.Option value="running">运行中</Select.Option>
            <Select.Option value="completed">已完成</Select.Option>
            <Select.Option value="failed">失败</Select.Option>
            <Select.Option value="cancelled">已取消</Select.Option>
          </Select>
        </Space>

        <Table
          columns={columns}
          dataSource={tasks}
          rowKey="id"
          loading={loading}
          scroll={{ x: 1200 }}
        />
      </Card>

      <Modal
        title="创建任务"
        open={createModalVisible}
        onCancel={() => {
          setCreateModalVisible(false);
          form.resetFields();
        }}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreateTask}
        >
          <Form.Item
            label="选择爬虫"
            name="crawler_id"
            rules={[{ required: true, message: '请选择爬虫' }]}
          >
            <Select placeholder="请选择爬虫">
              {crawlers.map((crawler) => (
                <Select.Option key={crawler.id} value={crawler.id}>
                  {crawler.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            label="任务名称"
            name="name"
            rules={[{ required: true, message: '请输入任务名称' }]}
          >
            <Input placeholder="请输入任务名称" />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                创建并执行
              </Button>
              <Button onClick={() => {
                setCreateModalVisible(false);
                form.resetFields();
              }}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </Space>
  );
};

export default TaskList;
