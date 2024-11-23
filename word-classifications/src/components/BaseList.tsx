import React, { useEffect, useState } from 'react';
import { Card, Table, Layout } from 'antd';
import type { TablePaginationConfig } from 'antd/es/table';
import type { ColumnsType } from 'antd/es/table';
import CategorySidebar from './CategorySidebar';
const { Content, Sider } = Layout;

interface BaseListProps<T> {
  columns: ColumnsType<T>;
  fetchData: (params: { page: number; pageSize: number; category?: string }) => Promise<{
    data: T[];
    total: number;
  }>;
  fetchCategories: () => Promise<any[]>;
  rowKey: string;
}

function BaseList<T>({ columns, fetchData, fetchCategories, rowKey }: BaseListProps<T>) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [categoryStats, setCategoryStats] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  const loadData = async () => {
    setLoading(true);
    try {
      const response = await fetchData({
        page: currentPage,
        pageSize,
        category: selectedCategory,
      });
      setData(response.data);
      setTotal(response.total);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const stats = await fetchCategories();
      setCategoryStats(stats);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  useEffect(() => {
    loadData();
  }, [currentPage, pageSize, selectedCategory]);

  useEffect(() => {
    loadCategories();
  }, []);

  const handleTableChange = (pagination: TablePaginationConfig) => {
    setCurrentPage(pagination.current || 1);
    setPageSize(pagination.pageSize || 10);
  };

  const handleCategorySelect = (category: string) => {
    setSelectedCategory(category);
    setCurrentPage(1);
  };

  return (
    <Layout style={{ minHeight: '100%' }}>
      <Sider theme="light" width={256} className="category-sidebar">
        <CategorySidebar
          categories={categoryStats}
          onSelect={handleCategorySelect}
        />
      </Sider>
      <Content className="content-layout">
        <Card>
          <Table
            columns={columns}
            dataSource={data}
            rowKey={rowKey}
            pagination={{
              current: currentPage,
              pageSize: pageSize,
              total: total,
              showSizeChanger: true,
            }}
            onChange={handleTableChange}
            loading={loading}
          />
        </Card>
      </Content>
    </Layout>
  );
}

export default BaseList; 