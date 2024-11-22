// src/pages/WordList.tsx
import React, { useEffect, useState } from 'react';
import { Card, Button, Table, Modal, Layout } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { WordClassification, CategoryStats } from '../types';
import type { TablePaginationConfig } from 'antd/es/table';
import { api } from '../services/api';
import CategorySidebar from '../components/CategorySidebar';

const { Sider, Content } = Layout;


const WordList: React.FC = () => {
  const [words, setWords] = useState<WordClassification[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [categoryStats, setCategoryStats] = useState<CategoryStats[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');


  const columns: ColumnsType<WordClassification> = [
    {
      title: '词语',
      dataIndex: 'word',
      key: 'word',
      width: 100,
    },
    {
      title: '主分类',
      dataIndex: 'main_category',
      key: 'main_category',
      width: 120,
    },
    {
      title: '子分类',
      dataIndex: 'sub_category',
      key: 'sub_category',
      width: 120,
    },
    {
      title: '释义',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: '置信度',
      dataIndex: 'confidence',
      key: 'confidence',
      width: 100,
      render: (value: number) => value?.toFixed(2),
    },
  ];

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await api.word.getWords({
        page: currentPage,
        pageSize: pageSize,
        category: selectedCategory,
      });
      setWords(response.data);
      setTotal(response.total);
    } catch (error) {
      console.error('Failed to fetch characters:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const stats = await api.word.getCategories();
      setCategoryStats(stats);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [currentPage, pageSize, selectedCategory]);

  useEffect(() => {
    fetchCategories();
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
    <Layout className="app-layout">
      <Sider theme="light" width={256}>
        <CategorySidebar
          categories={categoryStats}
          onSelect={handleCategorySelect}
        />
      </Sider>
      <Content className="content-layout">
        <Card>

          <Table
            columns={columns}
            dataSource={words}
            rowKey="word"
            pagination={{
              total,
              current: currentPage,
              pageSize: pageSize,
              showSizeChanger: false,
            }}
            onChange={handleTableChange}
            loading={loading}
          />
        </Card>
      </Content>
    </Layout>
  );
};

export default WordList;
