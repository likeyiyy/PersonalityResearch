// src/pages/WordList.tsx
import React from 'react';
import { WordClassification } from '../types';
import BaseList from '../components/BaseList';
import { api } from '../services/api';

const WordList: React.FC = () => {
  const columns = [
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

  return (
    <BaseList<WordClassification>
      columns={columns}
      fetchData={api.word.getWords}
      fetchCategories={api.word.getCategories}
      rowKey="word"
    />
  );
};

export default WordList;
