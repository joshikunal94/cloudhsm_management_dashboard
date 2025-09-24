import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { Spinner, Box } from '@cloudscape-design/components';
import { checkHSMHealth } from '../services/hsmService';

const HSMGuard = ({ children }) => {
  const [hsmStatus, setHsmStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkHSM = async () => {
      try {
        const status = await checkHSMHealth();
        setHsmStatus(status);
      } catch (error) {
        console.error('Failed to check HSM status:', error);
        setHsmStatus({ connected: false, configured: false });
      } finally {
        setLoading(false);
      }
    };

    checkHSM();
  }, []);

  if (loading) {
    return (
      <Box textAlign="center" padding="xxl">
        <Spinner size="large" />
        <Box variant="p" color="text-body-secondary">
          Checking HSM connection...
        </Box>
      </Box>
    );
  }

  // If HSM is not configured, redirect to config page
  if (!hsmStatus?.configured || !hsmStatus?.connected) {
    return <Navigate to="/hsm-config" replace />;
  }

  return children;
};

export default HSMGuard;