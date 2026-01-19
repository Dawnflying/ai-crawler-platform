import React from 'react';
import { Card, Typography, Empty } from 'antd';

const { Title, Paragraph } = Typography;

const DataList: React.FC = () => {
  return (
    <div>
      <Title level={2}>数据管理</Title>
      <Card>
        <Empty
          description={
            <div>
              <Paragraph>数据管理功能开发中...</Paragraph>
              <Paragraph type="secondary">
                此模块将用于查看、搜索、导出爬虫采集的数据
              </Paragraph>
            </div>
          }
        />
      </Card>
    </div>
  );
};

export default DataList;
