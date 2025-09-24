import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import '@cloudscape-design/global-styles/index.css';
import LoginPage from './pages/LoginPage';
import KeysPage from './pages/KeysPage';
import HSMConfigPage from './pages/HSMConfigPage';
import AppTopNavigation from './components/Layout/AppTopNavigation';
import HSMGuard from './components/HSMGuard';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
    },
  },
});

const AppContent = () => {
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';
  const isConfigPage = location.pathname === '/hsm-config';

  return (
    <>
      {!isLoginPage && !isConfigPage && <AppTopNavigation />}
      <Routes>
        <Route path="/hsm-config" element={<HSMConfigPage />} />
        <Route path="/login" element={
          <HSMGuard>
            <LoginPage />
          </HSMGuard>
        } />
        <Route path="/keys" element={
          <HSMGuard>
            <KeysPage />
          </HSMGuard>
        } />
        <Route path="/" element={<Navigate to="/keys" replace />} />
      </Routes>
    </>
  );
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AppContent />
      </Router>
    </QueryClientProvider>
  );
}

export default App;