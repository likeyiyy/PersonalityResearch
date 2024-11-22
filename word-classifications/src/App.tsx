// src/App.tsx
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import WordList from './pages/WordList';

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <WordList />
    </ConfigProvider>
  );
}

export default App;
