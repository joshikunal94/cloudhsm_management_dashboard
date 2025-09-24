import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import {
  Container,
  Header,
  Form,
  FormField,
  Input,
  Button,
  SpaceBetween,
  Alert
} from '@cloudscape-design/components';
import { authService } from '../services/authService';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const loginMutation = useMutation({
    mutationFn: ({ username, password }) => authService.login(username, password),
    onSuccess: () => {
      navigate('/keys');
    },
    onError: (error) => {
      console.error('Login failed:', error);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username && password) {
      loginMutation.mutate({ username, password });
    }
  };

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      backgroundColor: '#f2f3f3'
    }}>
      <Container>
        <form onSubmit={handleSubmit}>
          <SpaceBetween size="l">
            <Header variant="h1">CloudHSM Dashboard Login</Header>
            
            {loginMutation.isError && (
              <Alert type="error">
                Login failed. Please check your credentials.
              </Alert>
            )}

            <FormField label="Username">
              <Input
                value={username}
                onChange={({ detail }) => setUsername(detail.value)}
                placeholder="Enter username"
                disabled={loginMutation.isPending}
              />
            </FormField>

            <FormField label="Password">
              <Input
                value={password}
                onChange={({ detail }) => setPassword(detail.value)}
                placeholder="Enter password"
                type="password"
                disabled={loginMutation.isPending}
              />
            </FormField>

            <Button
              variant="primary"
              loading={loginMutation.isPending}
              onClick={handleSubmit}
              fullWidth
            >
              Login
            </Button>
          </SpaceBetween>
        </form>
      </Container>
    </div>
  );
};

export default LoginPage;