import api from './api';
import { API_CONFIG } from '../config/api';

export const keysService = {
  listKeys: async () => {
    const response = await api.get(API_CONFIG.ENDPOINTS.KEYS_LIST);
    return response.data;
  },

  filterKeys: async (filters) => {
    const response = await api.post(API_CONFIG.ENDPOINTS.KEYS_FILTER, filters);
    return response.data;
  },

  findKey: async (filters) => {
    const response = await api.post(API_CONFIG.ENDPOINTS.KEYS_FIND, filters);
    return response.data;
  },

  createKey: async (keyData) => {
    const response = await api.post('/keys/create', keyData);
    return response.data;
  },

  deleteKey: async (deleteData) => {
    const response = await api.post('/keys/delete', deleteData);
    return response.data;
  }
};