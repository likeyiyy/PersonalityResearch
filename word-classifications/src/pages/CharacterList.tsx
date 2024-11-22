import React, { useEffect, useState } from 'react';
import { Card, Table, Layout } from 'antd';
import type { TablePaginationConfig } from 'antd/es/table';
import { Character, CategoryStats } from '../types/character';
import CategorySidebar from '../components/CategorySidebar';
import { api } from '../services/api';
const { Content, Sider } = Layout;

const CharacterList: React.FC = () => {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [categoryStats, setCategoryStats] = useState<CategoryStats[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  const columns = [
    {
      title: '汉字',
      dataIndex: 'character',
      key: 'character',
    },
    {
      title: '一级分类',
      dataIndex: 'level_1_category',
      key: 'level_1_category',
    },
    {
      title: '二级分类',
      dataIndex: 'level_2_category',
      key: 'level_2_category',
    },
    {
      title: '三级分类',
      dataIndex: 'level_3_category',
      key: 'level_3_category',
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: '置信度',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (confidence: number) => `${(confidence * 100).toFixed(1)}%`,
    },
  ];

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await api.character.getCharacters({
        page: currentPage,
        pageSize: pageSize,
        category: selectedCategory,
      });
      setCharacters(response.data);
      setTotal(response.total);
    } catch (error) {
      console.error('Failed to fetch characters:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const stats = await api.character.getCategories();
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
            dataSource={characters}
            rowKey="id"
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
};

export default CharacterList; 