import React from 'react';
import { Character } from '../types';
import BaseList from '../components/BaseList';
import { api } from '../services/api';

const DerogatoryTerm: React.FC = () => {
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
  ];

  return (
    <BaseList<Character>
      columns={columns}
      fetchData={api.derogatoryTerm.getDerogatoryTerms}
      fetchCategories={api.derogatoryTerm.getCategories}
      rowKey="id"
    />
  );
};

export default DerogatoryTerm; 
