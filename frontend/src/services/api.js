/**
 * API Service - Handles all backend communication
 * 
 * Features:
 * - Axios client with default config
 * - Lead scoring endpoint
 * - Lead listing with pagination
 * - Analytics endpoint
 * - Error handling
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Request interceptor
apiClient.interceptors.request.use(
  config => {
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor
apiClient.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    throw error?.response?.data || error.message
  }
)

export const leadAPI = {
  /**
   * Score a new lead
   */
  scoreLead: async (leadData) => {
    return apiClient.post('/score-lead', leadData)
  },

  /**
   * Get list of leads with pagination
   */
  getLeads: async (page = 0, limit = 20, sortBy = 'score', intentFilter = null) => {
    const params = {
      skip: page * limit,
      limit,
      sort_by: sortBy,
    }
    if (intentFilter) {
      params.intent_filter = intentFilter
    }
    return apiClient.get('/leads', { params })
  },

  /**
   * Get single lead by ID
   */
  getLead: async (leadId) => {
    return apiClient.get(`/leads/${leadId}`)
  },

  /**
   * Get analytics
   */
  getAnalytics: async () => {
    return apiClient.get('/analytics')
  },
}

export default apiClient
