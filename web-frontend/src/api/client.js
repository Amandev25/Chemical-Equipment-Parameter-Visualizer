import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Include cookies for session authentication
});

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Get CSRF token from cookie and add to headers
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
      config.headers['X-CSRFToken'] = csrftoken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      localStorage.removeItem('isAuthenticated');
      // Only redirect if not already on login page
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// API Methods
export const api = {
  // Authentication endpoints
  login: (username, password) => apiClient.post('/auth/login/', { username, password }),
  register: (username, password, passwordConfirm, email = '') => 
    apiClient.post('/auth/register/', { username, password, password_confirm: passwordConfirm, email }),
  logout: () => apiClient.post('/auth/logout/'),
  getCurrentUser: () => apiClient.get('/auth/me/'),
  getCsrfToken: () => apiClient.get('/auth/csrf/'),

  // Health check
  healthCheck: () => apiClient.get('/health/'),

  // Equipment endpoints
  getEquipment: (params = {}) => apiClient.get('/equipment/', { params }),
  getEquipmentById: (id) => apiClient.get(`/equipment/${id}/`),
  createEquipment: (data) => apiClient.post('/equipment/', data),
  updateEquipment: (id, data) => apiClient.put(`/equipment/${id}/`, data),
  deleteEquipment: (id) => apiClient.delete(`/equipment/${id}/`),
  getEquipmentTypes: () => apiClient.get('/equipment/types/'),

  // CSV Upload endpoints
  uploadCSV: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/uploads/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getUploads: () => apiClient.get('/uploads/'),
  getUploadById: (id) => apiClient.get(`/uploads/${id}/`),
  getUploadEquipment: (id) => apiClient.get(`/uploads/${id}/equipment/`),
  getUploadSummary: (id) => apiClient.get(`/uploads/${id}/summary/`),

  // Dashboard endpoints
  getDashboardSummary: () => apiClient.get('/dashboard/summary/'),
  getFlowrateChartData: (params = {}) => apiClient.get('/dashboard/flowrate-chart/', { params }),
  getTypeDistributionData: (params = {}) => apiClient.get('/dashboard/type-distribution/', { params }),

  // Report endpoints
  generateReport: (params = {}) => {
    return apiClient.post('/reports/generate/', params, {
      responseType: 'blob',
    });
  },

  // Utility endpoints
  clearAllData: () => apiClient.delete('/clear/'),
};

export default apiClient;

