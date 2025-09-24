import axios from 'axios';
import { API_CONFIG } from '../config/api';

// Create axios instance
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  withCredentials: true, // Include cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for handling 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login on 401
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;