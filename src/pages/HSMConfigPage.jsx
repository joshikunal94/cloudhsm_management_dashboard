import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Header,
  SpaceBetween,
  Form,
  FormField,
  Input,
  FileUpload,
  Button,
  Alert,
  Box
} from '@cloudscape-design/components';
import { configureHSM, testHSMConnection } from '../services/hsmService';

const HSMConfigPage = () => {
  const navigate = useNavigate();
  const [ipAddress, setIpAddress] = useState('');
  const [certificate, setCertificate] = useState([]);
  const [loading, setLoading] = useState(false);
  const [testing, setTesting] = useState(false);
  const [alert, setAlert] = useState(null);

  const handleTestConnection = async () => {
    setTesting(true);
    setAlert(null);
    
    try {
      const result = await testHSMConnection();
      if (result.success) {
        setAlert({ type: 'success', content: result.message });
      } else {
        setAlert({ type: 'error', content: result.message });
      }
    } catch (error) {
      setAlert({ type: 'error', content: 'Failed to test connection' });
    } finally {
      setTesting(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!ipAddress || certificate.length === 0) {
      setAlert({ type: 'error', content: 'Please provide both IP address and certificate file' });
      return;
    }

    setLoading(true);
    setAlert(null);

    try {
      const result = await configureHSM(ipAddress, certificate[0]);
      
      if (result.success) {
        setAlert({ type: 'success', content: result.message });
        // Redirect to login after successful configuration
        setTimeout(() => navigate('/login'), 2000);
      } else {
        setAlert({ type: 'error', content: result.message });
      }
    } catch (error) {
      setAlert({ type: 'error', content: 'Failed to configure HSM' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <SpaceBetween size="l">
        <Header variant="h1">
          CloudHSM Configuration
        </Header>
        
        <Box>
          <p>Configure your CloudHSM connection by providing the HSM IP address and customer CA certificate.</p>
        </Box>

        {alert && (
          <Alert type={alert.type} dismissible onDismiss={() => setAlert(null)}>
            {alert.content}
          </Alert>
        )}

        <Form
          actions={
            <SpaceBetween direction="horizontal" size="xs">
              <Button 
                variant="normal" 
                onClick={handleTestConnection}
                loading={testing}
                disabled={loading}
              >
                Test Connection
              </Button>
              <Button 
                variant="primary" 
                onClick={handleSubmit}
                loading={loading}
                disabled={testing}
              >
                Configure HSM
              </Button>
            </SpaceBetween>
          }
        >
          <SpaceBetween direction="vertical" size="l">
            <FormField
              label="HSM IP Address"
              description="Enter the IP address of your CloudHSM cluster"
            >
              <Input
                value={ipAddress}
                onChange={({ detail }) => setIpAddress(detail.value)}
                placeholder="10.0.0.100"
                disabled={loading}
              />
            </FormField>

            <FormField
              label="Customer CA Certificate"
              description="Upload the customerCA.crt file for your CloudHSM cluster"
            >
              <FileUpload
                onChange={({ detail }) => setCertificate(detail.value)}
                value={certificate}
                i18nStrings={{
                  uploadButtonText: e => e ? "Choose files" : "Choose file",
                  dropzoneText: e => e ? "Drop files to upload" : "Drop file to upload",
                  removeFileAriaLabel: e => `Remove file ${e + 1}`,
                  limitShowFewer: "Show fewer files",
                  limitShowMore: "Show more files",
                  errorIconAriaLabel: "Error"
                }}
                showFileLastModified
                showFileSize
                showFileThumbnail
                tokenLimit={3}
                accept=".crt,.pem"
                disabled={loading}
              />
            </FormField>
          </SpaceBetween>
        </Form>
      </SpaceBetween>
    </Container>
  );
};

export default HSMConfigPage;