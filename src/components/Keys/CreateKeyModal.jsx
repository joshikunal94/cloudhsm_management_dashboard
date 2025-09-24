import React, { useState } from 'react';
import { Modal, Box, SpaceBetween, Form, FormField, Input, Select, Button, Alert } from '@cloudscape-design/components';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { keysService } from '../../services/keysService';

const CreateKeyModal = ({ visible, onDismiss }) => {
  const [formData, setFormData] = useState({
    label: '',
    key_class: 'SECRET_KEY',
    key_type: 'AES',
    key_size: 32
  });
  const [alert, setAlert] = useState(null);

  const queryClient = useQueryClient();

  const createKeyMutation = useMutation({
    mutationFn: (keyData) => keysService.createKey(keyData),
    onSuccess: (data) => {
      setAlert({ type: 'success', message: data.message });
      queryClient.invalidateQueries(['keys']);
      setTimeout(() => {
        onDismiss();
        setAlert(null);
        setFormData({ label: '', key_class: 'SECRET_KEY', key_type: 'AES', key_size: 32 });
      }, 2000);
    },
    onError: (error) => {
      setAlert({ type: 'error', message: error.response?.data?.detail || 'Failed to create key' });
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setAlert(null);
    createKeyMutation.mutate(formData);
  };

  const keyClassOptions = [
    { label: 'Secret Key', value: 'SECRET_KEY' },
    { label: 'Private Key', value: 'PRIVATE_KEY' }
  ];

  const keyTypeOptions = [
    { label: 'AES', value: 'AES' },
    { label: 'RSA', value: 'RSA' }
  ];

  const isAES = formData.key_type === 'AES';

  return (
    <Modal
      onDismiss={onDismiss}
      visible={visible}
      header="Create Key"
      footer={
        <Box float="right">
          <SpaceBetween direction="horizontal" size="xs">
            <Button variant="link" onClick={onDismiss}>
              Cancel
            </Button>
            <Button 
              variant="primary" 
              onClick={handleSubmit}
              loading={createKeyMutation.isPending}
            >
              Create Key
            </Button>
          </SpaceBetween>
        </Box>
      }
    >
      <form onSubmit={handleSubmit}>
        <SpaceBetween size="l">
          {alert && (
            <Alert type={alert.type}>
              {alert.message}
            </Alert>
          )}
          
          <FormField label="Label" constraintText="Required">
            <Input
              value={formData.label}
              onChange={({ detail }) => setFormData({ ...formData, label: detail.value })}
              placeholder="Enter key label"
              required
            />
          </FormField>

          <FormField label="Key Class">
            <Select
              selectedOption={{ label: keyClassOptions.find(o => o.value === formData.key_class)?.label, value: formData.key_class }}
              onChange={({ detail }) => setFormData({ ...formData, key_class: detail.selectedOption.value })}
              options={keyClassOptions}
            />
          </FormField>

          <FormField label="Key Type" constraintText="Required">
            <Select
              selectedOption={{ label: keyTypeOptions.find(o => o.value === formData.key_type)?.label, value: formData.key_type }}
              onChange={({ detail }) => setFormData({ ...formData, key_type: detail.selectedOption.value })}
              options={keyTypeOptions}
            />
          </FormField>

          <FormField 
            label="Key Size" 
            constraintText={isAES ? "Required for AES keys (bytes)" : "Optional for RSA keys (bits)"}
          >
            <Input
              value={formData.key_size?.toString() || ''}
              onChange={({ detail }) => setFormData({ ...formData, key_size: parseInt(detail.value) || null })}
              placeholder={isAES ? "32 (256-bit)" : "2048"}
              type="number"
            />
          </FormField>
        </SpaceBetween>
      </form>
    </Modal>
  );
};

export default CreateKeyModal;