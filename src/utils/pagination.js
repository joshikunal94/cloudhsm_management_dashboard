export const paginateData = (data, currentPage, pageSize) => {
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  return data.slice(startIndex, endIndex);
};

export const getTotalPages = (totalItems, pageSize) => {
  return Math.ceil(totalItems / pageSize);
};