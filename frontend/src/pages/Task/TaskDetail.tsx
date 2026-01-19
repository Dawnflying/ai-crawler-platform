import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Tag,
  Typography,
  Tabs,
  Table,
  Spin,
  message,
  Space,
  Button,
} from 'antd';
import { taskApi } from '@/api/task';
import { Task, TaskLog } from '@/types';
import dayjs from 'dayjs';
import type { ColumnsType } from 'antd/es/table';

const { Title } = Typography;

const TaskDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [task, setTask] = useState<Task | null>(null);
  const [logs, setLogs] = useState<TaskLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [logsLoading, setLogsLoading] = useState(false);

  useEffect(() => {
    if (id) {
      fetchTask(parseInt(id));
      fetchLogs(parseInt(id));
    }
  }, [id]);

  const fetchTask = async (taskId: number) => {
    setLoading(true);
    try {
      const data = await taskApi.get(taskId);
      setTask(data);
    } catch (error) {
      console.error('Failed to fetch task:', error);
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchLogs = async (taskId: number) => {
    setLogsLoading(true);
    try {
      const data = await taskApi.getLogs(taskId, { page: 1, page_size: 100 });
      setLogs(data);
    } catch (error) {
      console.error('Failed to fetch logs:', error);
    } finally {
      setLogsLoading(false);
    }
  };

  if (loading) {
    return <Spin size="large" style={{ display: 'flex', justifyContent: 'center', marginTop: 100 }} />;
  }

  if (!task) {
    return <div>任务不存在</div>;
  }

  const statusMap: Record<string, { text: string; color: string }> = {
    pending: { text: '待执行', color: 'blue' },
    running: { text: '运行中', color: 'orange' },
    completed: { text: '已完成', color: 'green' },
    failed: { text: '失败', color: 'red' },
    cancelled: { text: '已取消', color: 'gray' },
  };

  const logColumns: ColumnsType<TaskLog> = [
    {
      title: '时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (time: string) => dayjs(time).format('YYYY-MM-DD HH:mm:ss'),
    },
    {
      title: '级别',
      dataIndex: 'level',
      key: 'level',
      width: 100,
      render: (level: string) => {
        const colorMap: Record<string, string> = {
          DEBUG: 'blue',
          INFO: 'green',
          WARNING: 'orange',
          ERROR: 'red',
        };
        return <Tag color={colorMap[level]}>{level}</Tag>;
      },
    },
    {
      title: '消息',
      dataIndex: 'message',
      key: 'message',
    },
  ];

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Title level={2}>{task.name}</Title>
        <Button onClick={() => navigate('/tasks')}>返回列表</Button>
      </div>

      <Tabs
        items={[
          {
            key: 'info',
            label: '基本信息',
            children: (
              <Card>
                <Descriptions column={2}>
                  <Descriptions.Item label="任务名称">{task.name}</Descriptions.Item>
                  <Descriptions.Item label="状态">
                    <Tag color={statusMap[task.status]?.color}>
                      {statusMap[task.status]?.text}
                    </Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="爬虫">{task.crawler_name}</Descriptions.Item>
                  <Descriptions.Item label="创建者">{task.creator_name}</Descriptions.Item>
                  <Descriptions.Item label="总数据量">{task.total_items}</Descriptions.Item>
                  <Descriptions.Item label="成功数量">{task.success_items}</Descriptions.Item>
                  <Descriptions.Item label="失败数量">{task.failed_items}</Descriptions.Item>
                  <Descriptions.Item label="执行时长">
                    {task.duration ? `${task.duration}秒` : '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="开始时间">
                    {task.started_at ? dayjs(task.started_at).format('YYYY-MM-DD HH:mm:ss') : '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="完成时间">
                    {task.completed_at ? dayjs(task.completed_at).format('YYYY-MM-DD HH:mm:ss') : '-'}
                  </Descriptions.Item>
                  <Descriptions.Item label="创建时间">
                    {dayjs(task.created_at).format('YYYY-MM-DD HH:mm:ss')}
                  </Descriptions.Item>
                  <Descriptions.Item label="更新时间">
                    {dayjs(task.updated_at).format('YYYY-MM-DD HH:mm:ss')}
                  </Descriptions.Item>
                  {task.error_message && (
                    <Descriptions.Item label="错误信息" span={2}>
                      <span style={{ color: 'red' }}>{task.error_message}</span>
                    </Descriptions.Item>
                  )}
                </Descriptions>
              </Card>
            ),
          },
          {
            key: 'logs',
            label: '执行日志',
            children: (
              <Card>
                <Table
                  columns={logColumns}
                  dataSource={logs}
                  rowKey="id"
                  loading={logsLoading}
                  pagination={{ pageSize: 50 }}
                />
              </Card>
            ),
          },
        ]}
      />
    </Space>
  );
};

export default TaskDetail;
