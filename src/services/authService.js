import api from './api';
import { API_CONFIG } from '../config/api';

export const authService = {
  login: async (username, password) => {
    const response = await api.post(API_CONFIG.ENDPOINTS.LOGIN, {
      username,
      password
    });
    return response.data;
  },

  logout: async () => {
    const response = await api.post(API_CONFIG.ENDPOINTS.LOGOUT);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get(API_CONFIG.ENDPOINTS.ME);
    return response.data;
  }
};