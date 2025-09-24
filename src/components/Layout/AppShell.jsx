import React from 'react';
import { AppLayout, SideNavigation } from '@cloudscape-design/components';
import { useNavigate, useLocation } from 'react-router-dom';

const AppShell = ({ children, splitPanel, splitPanelOpen, onSplitPanelToggle }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const navigationItems = [
    {
      type: 'link',
      text: 'Keys',
      href: '/keys'
    }
  ];

  return (
    <AppLayout
      navigation={
        <SideNavigation
          header={{ text: 'CloudHSM Dashboard', href: '/' }}
          items={navigationItems}
          activeHref={location.pathname}
          onFollow={(event) => {
            if (!event.detail.external) {
              event.preventDefault();
              navigate(event.detail.href);
            }
          }}
        />
      }
      toolsHide={true}
      content={children}
      headerSelector="#top-nav"
      splitPanel={splitPanel}
      splitPanelOpen={splitPanelOpen}
      onSplitPanelToggle={onSplitPanelToggle}
    />
  );
};

export default AppShell;