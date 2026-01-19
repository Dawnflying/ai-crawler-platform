import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Space,
  Table,
  Button,
  Tag,
  Popconfirm,
  message,
  Input,
  Select,
  Card,
  Typography,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  PlayCircleOutlined,
  EyeOutlined,
} from '@ant-design/icons';
import { crawlerApi } from '@/api/crawler';
import { Crawler } from '@/types';
import dayjs from 'dayjs';
import type { ColumnsType } from 'antd/es/table';

const { Search } = Input;
const { Title } = Typography;

const CrawlerList: React.FC = () => {
  const navigate = useNavigate();
  const [crawlers, setCrawlers] = useState<Crawler[]>([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    type: undefined as string | undefined,
    status: undefined as string | undefined,
    search: '',
  });

  useEffect(() => {
    fetchCrawlers();
  }, [filters]);

  const fetchCrawlers = async () => {
    setLoading(true);
    try {
      const data = await crawlerApi.list({
        type: filters.type,
        status: filters.status,
        search: filters.search || undefined,
        page: 1,
        page_size: 100,
      });
      setCrawlers(data);
    } catch (error) {
      console.error('Failed to fetch crawlers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await crawlerApi.delete(id);
      message.success('删除成功');
      fetchCrawlers();
    } catch (error) {
      console.error('Failed to delete crawler:', error);
    }
  };

  const columns: ColumnsType<Crawler> = [
    {
      title: '爬虫名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <a onClick={() => navigate(`/crawlers/${record.id}`)}>{text}</a>
      ),
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => {
        const typeMap: Record<string, { text: string; color: string }> = {
          http: { text: 'HTTP 爬虫', color: 'blue' },
          api: { text: 'API 采集', color: 'green' },
          browser: { text: '浏览器自动化', color: 'purple' },
        };
        const { text, color } = typeMap[type] || { text: type, color: 'default' };
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const statusMap: Record<string, { text: string; color: string }> = {
          active: { text: '活跃', color: 'success' },
          inactive: { text: '未激活', color: 'default' },
          error: { text: '错误', color: 'error' },
        };
        const { text, color } = statusMap[status] || { text: status, color: 'default' };
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '任务数',
      dataIndex: 'task_count',
      key: 'task_count',
      render: (count) => count || 0,
    },
    {
      title: '创建者',
      dataIndex: 'creator_name',
      key: 'creator_name',
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
      width: 200,
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => navigate(`/crawlers/${record.id}`)}
          >
            详情
          </Button>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => navigate(`/crawlers/${record.id}/edit`)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个爬虫吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button
              type="link"
              size="small"
              danger
              icon={<DeleteOutlined />}
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Title level={2} style={{ margin: 0 }}>爬虫管理</Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => navigate('/crawlers/create')}
        >
          创建爬虫
        </Button>
      </div>

      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Select
            placeholder="选择类型"
            style={{ width: 150 }}
            allowClear
            value={filters.type}
            onChange={(value) => setFilters({ ...filters, type: value })}
          >
            <Select.Option value="http">HTTP 爬虫</Select.Option>
            <Select.Option value="api">API 采集</Select.Option>
            <Select.Option value="browser">浏览器自动化</Select.Option>
          </Select>
          <Select
            placeholder="选择状态"
            style={{ width: 120 }}
            allowClear
            value={filters.status}
            onChange={(value) => setFilters({ ...filters, status: value })}
          >
            <Select.Option value="active">活跃</Select.Option>
            <Select.Option value="inactive">未激活</Select.Option>
            <Select.Option value="error">错误</Select.Option>
          </Select>
          <Search
            placeholder="搜索爬虫名称或描述"
            style={{ width: 300 }}
            onSearch={(value) => setFilters({ ...filters, search: value })}
            allowClear
          />
        </Space>

        <Table
          columns={columns}
          dataSource={crawlers}
          rowKey="id"
          loading={loading}
          scroll={{ x: 1200 }}
        />
      </Card>
    </Space>
  );
};

export default CrawlerList;
