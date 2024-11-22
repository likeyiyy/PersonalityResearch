import React from 'react';
import { Menu } from 'antd';
import type { MenuProps } from 'antd';
import { CategoryStats } from '../types';

interface CategorySidebarProps {
  categories: CategoryStats[];
  onSelect: (category: string) => void;
}

const CategorySidebar: React.FC<CategorySidebarProps> = ({ categories, onSelect }) => {
  const items: MenuProps['items'] = categories.map(cat => ({
    key: cat.main_category,
    label: `${cat.main_category} (${cat.total_count})`,
    children: cat.sub_categories.map(sub => ({
      key: `${cat.main_category}/${sub.name}`,
      label: `${sub.name} (${sub.count})`,
      children: sub.sub_categories?.map(level3 => ({
        key: `${cat.main_category}/${sub.name}/${level3.name}`,
        label: `${level3.name} (${level3.count})`
      }))
    }))
  }));

  const handleSelect: MenuProps['onSelect'] = ({ key }) => {
    onSelect(key);
  };

  return (
    <Menu
      mode="inline"
      style={{ width: 256 }}
      items={items}
      onSelect={handleSelect}
    />
  );
};

export default CategorySidebar;
