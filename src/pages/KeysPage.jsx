import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ContentLayout, SplitPanel, Header, Table, Pagination, CollectionPreferences, Button, SpaceBetween } from '@cloudscape-design/components';
import AppShell from '../components/Layout/AppShell';
import KeyDetailCard from '../components/Keys/KeyDetailCard';
import CreateKeyModal from '../components/Keys/CreateKeyModal';
import DeleteKeyModal from '../components/Keys/DeleteKeyModal';
import { keysService } from '../services/keysService';
import { paginateData, getTotalPages } from '../utils/pagination';
import KeysPropertiesFilter from '../components/Keys/KeysPropertiesFilter';

const KeysPage = () => {
  const [keys, setKeys] = useState([]);
  const [selectedItems, setSelectedItems] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(5);
  const [splitPanelOpen, setSplitPanelOpen] = useState(false);
  const [selectedKey, setSelectedKey] = useState(null);
  const [filterQuery, setFilterQuery] = useState({ tokens: [], operation: 'and' });
  const [createModalVisible, setCreateModalVisible] = useState(false);
  const [deleteModalVisible, setDeleteModalVisible] = useState(false);

  // Convert PropertyFilter query to API filters
  const getApiFilters = (query) => {
    const filters = {};
    query.tokens?.forEach(token => {
      if (token.operator === '=') {
        filters[token.propertyKey] = token.value;
      } else if (token.operator === '!=') {
        filters[`${token.propertyKey}__not`] = token.value;
      }
    });
    return filters;
  };

  const apiFilters = getApiFilters(filterQuery);
  const hasFilters = Object.keys(apiFilters).length > 0;

  // Fetch keys with filtering
  const { data: keysData, isLoading, error } = useQuery({
    queryKey: ['keys', apiFilters],
    queryFn: () => {
      if (hasFilters) {
        return keysService.filterKeys(apiFilters);
      }
      return keysService.listKeys();
    },
    retry: false
  });

  // Fetch key details
  const keyDetailMutation = useMutation({
    mutationFn: (keyFilters) => keysService.findKey(keyFilters)
  });

  useEffect(() => {
    if (keysData?.keys) {
      setKeys(keysData.keys);
    }
  }, [keysData]);

  // Reset to first page when filter changes
  useEffect(() => {
    setCurrentPage(1);
    setSelectedItems([]);
  }, [filterQuery]);

  const totalPages = getTotalPages(keys.length, pageSize);
  const paginatedKeys = paginateData(keys, currentPage, pageSize);

  const columnDefinitions = [
    {
      id: 'label',
      header: 'Label',
      cell: (item) => (
        <Button 
          variant="inline-link"
          onClick={() => handleKeyClick(item)}
        >
          {item.label || '-'}
        </Button>
      )
    },
    {
      id: 'key_class',
      header: 'Class',
      cell: (item) => item.key_class
    },
    {
      id: 'key_type',
      header: 'Type',
      cell: (item) => item.key_type
    },
    {
      id: 'key_id',
      header: 'Key ID',
      cell: (item) => item.key_id || '-'
    }
  ];

  const handleSelectionChange = ({ detail }) => {
    setSelectedItems(detail.selectedItems);
  };

  const handlePageChange = ({ detail }) => {
    setCurrentPage(detail.currentPageIndex);
  };

  const handleFilterChange = (query) => {
    setFilterQuery(query);
  };

  const queryClient = useQueryClient();
  
  const handleRefresh = () => {
    queryClient.invalidateQueries(['keys']);
  };

  const handleKeyClick = (key) => {
    setSelectedKey(key);
    setSplitPanelOpen(true);
    keyDetailMutation.mutate({
      key_class: key.key_class,
      key_type: key.key_type,
      label: key.label,
      key_id: key.key_id || null
    });
  };

  const handleSplitPanelToggle = ({ detail }) => {
    setSplitPanelOpen(detail.open);
  };

  if (error) {
    return (
      <AppShell>
        <ContentLayout>
          <div>Error loading keys: {error.message}</div>
        </ContentLayout>
      </AppShell>
    );
  }

  return (
    <AppShell
      splitPanel={
        <SplitPanel
          header={
            <Header variant="h3">
              Key Details: {selectedKey?.label || 'No key selected'}
            </Header>
          }
        >
          <KeyDetailCard 
            keyDetail={keyDetailMutation.data}
            loading={keyDetailMutation.isPending}
          />
        </SplitPanel>
      }
      splitPanelOpen={splitPanelOpen}
      onSplitPanelToggle={handleSplitPanelToggle}
    >
      <ContentLayout>
        <Table
          columnDefinitions={columnDefinitions}
          items={paginatedKeys}
          loading={isLoading}
          loadingText="Loading keys..."
          selectionType="multi"
          selectedItems={selectedItems}
          onSelectionChange={handleSelectionChange}
          stickyHeader
          header={
            <Header
              counter={selectedItems.length ? `(${selectedItems.length} selected)` : `(${keys.length})`}
              variant="h1"
              actions={
                <SpaceBetween direction="horizontal" size="xs">
                  <Button 
                    variant="primary"
                    onClick={() => setCreateModalVisible(true)}
                  >
                    Create Key
                  </Button>
                  <Button 
                    onClick={() => setDeleteModalVisible(true)}
                    disabled={selectedItems.length === 0}
                  >
                    Delete
                  </Button>
                  <Button 
                    iconName="refresh"
                    onClick={handleRefresh}
                    loading={isLoading}
                  / >
                </SpaceBetween>
              }
            >
              Keys
            </Header>
          }
          pagination={
            <Pagination
              currentPageIndex={currentPage}
              pagesCount={totalPages}
              onChange={handlePageChange}
            />
          }
          preferences={
            <CollectionPreferences
              title="Preferences"
              confirmLabel="Confirm"
              cancelLabel="Cancel"
              preferences={{ pageSize }}
              pageSizePreference={{
                title: 'Page size',
                options: [
                  { value: 5, label: '5 keys' },
                  { value: 10, label: '10 keys' },
                  { value: 25, label: '25 keys' },
                  { value: 50, label: '50 keys' }
                ]
              }}
              onConfirm={({ detail }) => setPageSize(detail.pageSize)}
            />
          }
          filter={
            <KeysPropertiesFilter onFilterChange={handleFilterChange}/>
          }
        />
        
        <CreateKeyModal
          visible={createModalVisible}
          onDismiss={() => setCreateModalVisible(false)}
        />
        
        <DeleteKeyModal
          visible={deleteModalVisible}
          onDismiss={() => setDeleteModalVisible(false)}
          selectedKeys={selectedItems}
        />
      </ContentLayout>
    </AppShell>
  );
};

export default KeysPage;