import React from 'react';
import { Character } from '../types';
import BaseList from '../components/BaseList';
import { api } from '../services/api';

const WordList2: React.FC = () => {
  const columns = [
    {
      title: '词语',
      dataIndex: 'word',
      key: 'word',
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

  return (
    <BaseList<Character>
      columns={columns}
      fetchData={api.word2.getWords}
      fetchCategories={api.word2.getCategories}
      rowKey="id"
    />
  );
};

export default WordList2; 