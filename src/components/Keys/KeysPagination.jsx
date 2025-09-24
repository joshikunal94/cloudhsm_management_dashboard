import React from 'react';
import { Pagination } from '@cloudscape-design/components';

const KeysPagination = ({ currentPage, totalPages, onPageChange }) => {
  if (totalPages <= 1) return null;

  return (
    <Pagination
      currentPageIndex={currentPage}
      pagesCount={totalPages}
      onChange={({ detail }) => onPageChange(detail.currentPageIndex)}
    />
  );
};

export default KeysPagination;