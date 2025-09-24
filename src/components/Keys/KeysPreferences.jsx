import React from 'react';
import { CollectionPreferences } from '@cloudscape-design/components';

const KeysPreferences = ({ pageSize, onPageSizeChange }) => {
  return (
    <CollectionPreferences
      title="Preferences"
      confirmLabel="Confirm"
      cancelLabel="Cancel"
      preferences={{
        pageSize: pageSize
      }}
      pageSizePreference={{
        title: 'Page size',
        options: [
          { value: 2, label: '2 keys' },
          { value: 5, label: '5 keys' },
          { value: 10, label: '10 keys' },
          { value: 25, label: '25 keys' },
          { value: 50, label: '50 keys' },
          { value: 100, label: '100 keys' }
        ]
      }}
      onConfirm={({ detail }) => {
        onPageSizeChange(detail.pageSize);
      }}
    />
  );
};

export default KeysPreferences;