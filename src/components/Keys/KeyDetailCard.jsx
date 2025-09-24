import React from 'react';
import { Container, Header, SpaceBetween, ColumnLayout, Box, Spinner } from '@cloudscape-design/components';

const KeyDetailCard = ({ keyDetail, loading }) => {
  if (loading) {
    return (
      <Container>
        <Box textAlign="center" padding="xl">
          <SpaceBetween size="m" alignItems="center">
            <Spinner size="large" />
            <Box>Loading key details...</Box>
          </SpaceBetween>
        </Box>
      </Container>
    );
  }

  if (!keyDetail) {
    return (
      <Container>
        <Box textAlign="center">No key details available</Box>
      </Container>
    );
  }

  return (
    <Container header={<Header variant="h2">Key Information</Header>}>
      <SpaceBetween size="l">
        <ColumnLayout columns={2} variant="text-grid">
          <div>
            <Box variant="awsui-key-label">Label</Box>
            <div>{keyDetail.label || '-'}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Class</Box>
            <div>{keyDetail.key_class}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Type</Box>
            <div>{keyDetail.key_type}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Key ID</Box>
            <div>{keyDetail.key_id || '-'}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Token</Box>
            <div>{keyDetail.token ? 'Yes' : 'No'}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Private</Box>
            <div>{keyDetail.private ? 'Yes' : 'No'}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Sensitive</Box>
            <div>{keyDetail.sensitive ? 'Yes' : 'No'}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Extractable</Box>
            <div>{keyDetail.extractable ? 'Yes' : 'No'}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Local</Box>
            <div>{keyDetail.local ? 'Yes' : 'No'}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Modifiable</Box>
            <div>{keyDetail.modifiable ? 'Yes' : 'No'}</div>
          </div>
          <div>
            <Box variant="awsui-key-label">Destroyable</Box>
            <div>{keyDetail.destroyable ? 'Yes' : 'No'}</div>
          </div>
        </ColumnLayout>
      </SpaceBetween>
    </Container>
  );
};

export default KeyDetailCard;