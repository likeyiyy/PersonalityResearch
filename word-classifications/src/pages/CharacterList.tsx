import React from 'react';
import { Character } from '../types/character';
import BaseList from '../components/BaseList';
import { api } from '../services/api';

const CharacterList: React.FC = () => {
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

  return (
    <BaseList<Character>
      columns={columns}
      fetchData={api.character.getCharacters}
      fetchCategories={api.character.getCategories}
      rowKey="id"
    />
  );
};

export default CharacterList; 