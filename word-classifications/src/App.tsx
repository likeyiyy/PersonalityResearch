// src/App.tsx
import { ConfigProvider, Layout, Menu } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { BrowserRouter, Route, Routes, useNavigate } from 'react-router-dom';
import WordList from './pages/WordList';
import CharacterList from './pages/CharacterList';
import { useState } from 'react';
import WordList2 from './pages/WordList2';

const { Header, Content } = Layout;

const AppLayout = () => {
  const navigate = useNavigate();
  const [current, setCurrent] = useState('personality');

  const handleMenuClick = (key: string) => {
    setCurrent(key);
    navigate(`/${key}`);
  };

  return (
    <Layout className="app-layout">
      <Header style={{ background: '#fff' }}>
        <Menu
          mode="horizontal"
          selectedKeys={[current]}
          onClick={({ key }) => handleMenuClick(key as string)}
        >
          <Menu.Item key="personality">人格词语</Menu.Item>
          <Menu.Item key="characters">汉字分析</Menu.Item>
          <Menu.Item key="words">词语分析</Menu.Item>
        </Menu>
      </Header>
      <Content style={{ padding: '24px', minHeight: 'calc(100vh - 64px)' }}>
        <Routes>
          <Route path="/personality" element={<WordList />} />
          <Route path="/characters" element={<CharacterList />} />
          <Route path="/words" element={<WordList2 />} />
          <Route path="/" element={<WordList />} />
        </Routes>
      </Content>
    </Layout>
  );
};

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <BrowserRouter>
        <AppLayout />
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App;
