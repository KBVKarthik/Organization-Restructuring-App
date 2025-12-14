import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Organization endpoints
export const organizationAPI = {
  loadMock: () => api.post('/organization/load-mock'),
  getOverview: () => api.get('/organization/overview'),
};

// Employee endpoints
export const employeeAPI = {
  getAll: () => api.get('/employees'),
  getById: (id) => api.get(`/employees/${id}`),
};

// Analysis endpoints
export const analysisAPI = {
  getCriticalEmployees: (threshold = 75) =>
    api.get('/analysis/critical-employees', { params: { threshold } }),
  getLayoffAnalysis: (reductionPercent = 10) =>
    api.get('/analysis/layoff-analysis', { params: { reduction_percent: reductionPercent } }),
  getHierarchyAnalysis: () => api.get('/analysis/hierarchy'),
  getKPIAnalysis: () => api.get('/analysis/kpis'),
  getDepartmentStats: (department) => api.get(`/department-stats/${department}`),
};

// Restructuring endpoints
export const restructuringAPI = {
  createPlan: (planData) => api.post('/restructuring/plan', planData),
  createScenarios: () => api.post('/restructuring/scenarios'),
};

// Health check
export const healthCheck = () => api.get('/health');

export default api;
