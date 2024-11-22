// src/pages/WordList.tsx
import React, { useEffect, useState } from 'react';
import { Card, Select, Form, Button, Table, Modal, Space, Layout } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { WordClassification, CategoryData, CategoryStats } from '../types';
import { api } from '../services/api';
import CategorySidebar from '../components/CategorySidebar';

const { Sider, Content } = Layout;

const PAGE_SIZE = 100;

const WordList: React.FC = () => {
  const [categories, setCategories] = useState<CategoryData>({});
  const [subCategories, setSubCategories] = useState<string[]>([]);
  const [words, setWords] = useState<WordClassification[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedWord, setSelectedWord] = useState<WordClassification | null>(null);
  const [form] = Form.useForm();
  const [categoryStats, setCategoryStats] = useState<CategoryStats[]>([]);

  useEffect(() => {
    fetchCategories();
    fetchWords();
    fetchCategoryStats();
  }, []);

  const fetchCategories = async () => {
    try {
      const data = await api.getCategories();
      setCategories(data);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  const fetchWords = async (page = currentPage) => {
    setLoading(true);
    try {
      const values = await form.validateFields();
      const params = {
        ...values,
        page,
        page_size: PAGE_SIZE
      };
      const data = await api.getWords(params);
      setWords(data.items);
      setTotal(data.total);
      setCurrentPage(page);
    } catch (error) {
      console.error('Failed to fetch words:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategoryStats = async () => {
    try {
      const stats = await api.getCategoryStats();
      setCategoryStats(stats);
    } catch (error) {
      console.error('Failed to fetch category stats:', error);
    }
  };

  const handleMainCategoryChange = (value: string) => {
    setSubCategories(categories[value] || []);
    form.setFieldValue('sub_category', undefined);
  };

  const handleCategorySelect = (main: string, sub?: string) => {
    form.setFieldsValue({
      main_category: main,
      sub_category: sub
    });
    fetchWords(1);
  };

  const columns: ColumnsType<WordClassification> = [
    {
      title: '词语',
      dataIndex: 'word',
      width: 100,
    },
    {
      title: '主分类',
      dataIndex: 'main_category',
      width: 120,
    },
    {
      title: '子分类',
      dataIndex: 'sub_category',
      width: 120,
    },
    {
      title: '释义',
      dataIndex: 'description',
      ellipsis: true,
    },
    {
      title: '置信度',
      dataIndex: 'confidence',
      width: 100,
      render: (value: number) => value?.toFixed(2),
    },
    {
      title: '操作',
      width: 100,
      render: (_, record) => (
        <Button type="link" onClick={() => setSelectedWord(record)}>
          详情
        </Button>
      ),
    },
  ];

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
          <Form
            form={form}
            layout="inline"
            onFinish={() => fetchWords(1)}
            style={{ marginBottom: 24 }}
          >
            <Form.Item name="main_category" label="主分类">
              <Select
                style={{ width: 200 }}
                onChange={handleMainCategoryChange}
                allowClear
                placeholder="选择主分类"
              >
                {Object.keys(categories).map(category => (
                  <Select.Option key={category} value={category}>
                    {category}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item name="sub_category" label="子分类">
              <Select
                style={{ width: 200 }}
                allowClear
                placeholder="选择子分类"
                disabled={!subCategories.length}
              >
                {subCategories.map(category => (
                  <Select.Option key={category} value={category}>
                    {category}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item name="is_human_descriptive" label="是否形容人">
              <Select style={{ width: 120 }} allowClear>
                <Select.Option value={true}>是</Select.Option>
                <Select.Option value={false}>否</Select.Option>
              </Select>
            </Form.Item>

            <Form.Item>
              <Space>
                <Button type="primary" htmlType="submit">
                  查询
                </Button>
                <Button onClick={() => form.resetFields()}>
                  重置
                </Button>
              </Space>
            </Form.Item>
          </Form>

          <Table
            columns={columns}
            dataSource={words}
            rowKey="word"
            loading={loading}
            pagination={{
              total,
              current: currentPage,
              pageSize: PAGE_SIZE,
              onChange: fetchWords,
              showSizeChanger: false,
            }}
          />
        </Card>

        <Modal
          title="词语详情"
          open={!!selectedWord}
          onCancel={() => setSelectedWord(null)}
          footer={null}
        >
          {selectedWord && (
            <div>
              <p><strong>词语：</strong>{selectedWord.word}</p>
              <p><strong>释义：</strong>{selectedWord.description}</p>
              <p><strong>理由：</strong>{selectedWord.reason}</p>
              <p><strong>示例：</strong>{selectedWord.example}</p>
            </div>
          )}
        </Modal>
      </Content>
    </Layout>
  );
};

export default WordList;
