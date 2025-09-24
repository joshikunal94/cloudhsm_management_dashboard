import React from 'react';
import { TopNavigation } from '@cloudscape-design/components';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';

const AppTopNavigation = () => {
  const navigate = useNavigate();

  // Get current user
  const { data: user } = useQuery({
    queryKey: ['currentUser'],
    queryFn: authService.getCurrentUser,
    retry: false
  });

  // Logout mutation
  const logoutMutation = useMutation({
    mutationFn: authService.logout,
    onSuccess: () => {
      navigate('/login');
    }
  });

  const handleLogout = () => {
    logoutMutation.mutate();
  };

  const utilities = [
    {
      type: 'menu-dropdown',
      text: user?.username || 'User',
      iconName: 'user-profile',
      items: [
        {
          id: 'logout',
          text: 'Logout'
        }
      ],
      onItemClick: ({ detail }) => {
        if (detail.id === 'logout') {
          handleLogout();
        }
      }
    }
  ];

  return (
    <div id="top-nav">
      <TopNavigation
        identity={{
          href: '/',
          title: 'CloudHSM Dashboard'
        }}
        utilities={utilities}
      />
    </div>
  );
};

export default AppTopNavigation;