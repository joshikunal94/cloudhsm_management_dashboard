import React, { useState } from 'react';
import { Modal, Box, SpaceBetween, Button, Alert } from '@cloudscape-design/components';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { keysService } from '../../services/keysService';

const DeleteKeyModal = ({ visible, onDismiss, selectedKeys }) => {
  const [alert, setAlert] = useState(null);
  const queryClient = useQueryClient();

  const deleteKeyMutation = useMutation({
    mutationFn: async () => {
      const deletePromises = selectedKeys.map(key => 
        keysService.deleteKey({
          label: key.label,
          key_class: key.key_class,
          key_type: key.key_type,
          key_id: key.key_id
        })
      );
      return Promise.all(deletePromises);
    },
    onSuccess: (results) => {
      const totalDeleted = results.reduce((sum, result) => sum + (result.deleted_count || 0), 0);
      setAlert({ type: 'success', message: `Successfully deleted ${totalDeleted} key(s)` });
      queryClient.invalidateQueries(['keys']);
      setTimeout(() => {
        onDismiss();
        setAlert(null);
      }, 2000);
    },
    onError: (error) => {
      setAlert({ type: 'error', message: error.response?.data?.detail || 'Failed to delete keys' });
    }
  });

  const handleDelete = () => {
    setAlert(null);
    deleteKeyMutation.mutate();
  };

  return (
    <Modal
      onDismiss={onDismiss}
      visible={visible}
      header="Delete Keys"
      footer={
        <Box float="right">
          <SpaceBetween direction="horizontal" size="xs">
            <Button variant="link" onClick={onDismiss}>
              Cancel
            </Button>
            <Button 
              variant="primary" 
              onClick={handleDelete}
              loading={deleteKeyMutation.isPending}
            >
              Delete Keys
            </Button>
          </SpaceBetween>
        </Box>
      }
    >
      <SpaceBetween size="l">
        {alert && (
          <Alert type={alert.type}>
            {alert.message}
          </Alert>
        )}
        
        <Alert type="warning">
          Are you sure you want to delete the following key(s)?
        </Alert>

        <Box>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            <ul>
              {selectedKeys.map((key, index) => (
                <li key={index}>
                  <strong>{key.label || 'Unlabeled'}</strong> ({key.key_class} - {key.key_type})
                  {key.key_id && <div style={{ fontSize: '0.9em', color: '#666' }}>ID: {key.key_id}</div>}
                </li>
              ))}
            </ul>
          </div>
        </Box>
      </SpaceBetween>
    </Modal>
  );
};

export default DeleteKeyModal;