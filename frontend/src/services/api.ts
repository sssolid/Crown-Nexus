// frontend/src/services/api.ts
/**
 * API service module.
 *
 * This module provides a unified interface for making API requests with:
 * - Automatic authentication token handling
 * - Type-safe responses
 * - Centralized error handling
 * - Request/response interceptors
 *
 * All API communication should go through this service to ensure
 * consistent behavior throughout the application.
 */

import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import router from '@/router';

// API response types
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

// Error response structure
export interface ApiError {
  detail: string;
  status: number;
  title?: string;
  type?: string;
}

// Default API configuration
const apiConfig: AxiosRequestConfig = {
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 30000, // 30 second timeout
};

// Create axios instance
const apiClient: AxiosInstance = axios.create(apiConfig);

// Request interceptor for API calls
apiClient.interceptors.request.use(
  (config) => {
    // Set auth token if available
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('API request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for API calls
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config;
    if (!originalRequest) {
      return Promise.reject(error);
    }

    // Handle 401 (Unauthorized)
    if (error.response?.status === 401) {
      // If we're not on the login page, redirect to login
      if (router.currentRoute.value.path !== '/login') {
        localStorage.removeItem('access_token');

        // Store the current location to redirect back after login
        localStorage.setItem('redirectPath', router.currentRoute.value.fullPath);

        router.push('/login');
        return Promise.reject(error);
      }
    }

    // Handle 403 (Forbidden)
    if (error.response?.status === 403) {
      // Could redirect to a permission denied page or show a notification
      console.error('Permission denied:', error.response.data);
    }

    // Handle 404 (Not Found)
    if (error.response?.status === 404) {
      console.error('Resource not found:', error.response.data);
    }

    // Handle 422 (Validation Error)
    if (error.response?.status === 422) {
      console.error('Validation error:', error.response.data);
    }

    // Handle 500 (Server Error)
    if (error.response?.status === 500) {
      console.error('Server error:', error.response.data);
    }

    return Promise.reject(error);
  }
);

// Generic API service with typed responses
const api = {
  /**
   * Send a GET request to the API.
   *
   * @param url - API endpoint URL
   * @param config - Optional Axios config
   * @returns Promise with the response data
   */
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await apiClient.get(url, config);
      return response.data;
    } catch (error) {
      handleApiError(error);
      throw error;
    }
  },

  /**
   * Send a POST request to the API.
   *
   * @param url - API endpoint URL
   * @param data - Request payload
   * @param config - Optional Axios config
   * @returns Promise with the response data
   */
  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await apiClient.post(url, data, config);
      return response.data;
    } catch (error) {
      handleApiError(error);
      throw error;
    }
  },

  /**
   * Send a PUT request to the API.
   *
   * @param url - API endpoint URL
   * @param data - Request payload
   * @param config - Optional Axios config
   * @returns Promise with the response data
   */
  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await apiClient.put(url, data, config);
      return response.data;
    } catch (error) {
      handleApiError(error);
      throw error;
    }
  },

  /**
   * Send a DELETE request to the API.
   *
   * @param url - API endpoint URL
   * @param config - Optional Axios config
   * @returns Promise with the response data
   */
  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await apiClient.delete(url, config);
      return response.data;
    } catch (error) {
      handleApiError(error);
      throw error;
    }
  },

  /**
   * Send a multipart form data request (for file uploads).
   *
   * @param url - API endpoint URL
   * @param formData - FormData object with the file and additional data
   * @param config - Optional Axios config
   * @returns Promise with the response data
   */
  async uploadFile<T>(url: string, formData: FormData, config?: AxiosRequestConfig): Promise<T> {
    try {
      const defaultConfig: AxiosRequestConfig = {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      };

      const mergedConfig = { ...defaultConfig, ...config };
      const response: AxiosResponse<T> = await apiClient.post(url, formData, mergedConfig);
      return response.data;
    } catch (error) {
      handleApiError(error);
      throw error;
    }
  },

  // Export the axios instance for advanced use cases
  client: apiClient,
};

/**
 * Handle API errors centrally.
 *
 * @param error - The error object from Axios
 */
function handleApiError(error: any): void {
  // Get the response error details
  const errorResponse = error.response?.data;

  // Log the error for debugging
  console.error('API Error:', {
    status: error.response?.status,
    url: error.config?.url,
    method: error.config?.method,
    data: errorResponse,
  });

  // Here you could implement application-wide error handling:
  // - Show notifications
  // - Log to error tracking service
  // - Format error messages for display
}

/**
 * Base API service class that can be extended by domain-specific services
 */
export class ApiService {
  protected apiClient: AxiosInstance;

  constructor() {
    this.apiClient = apiClient;
  }

  /**
   * Execute a GET request
   * @param url The endpoint URL
   * @param config Optional Axios request configuration
   * @returns Promise with the response data
   */
  protected async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.apiClient.get(url, config);
    return response.data;
  }

  /**
   * Execute a POST request
   * @param url The endpoint URL
   * @param data The data to send
   * @param config Optional Axios request configuration
   * @returns Promise with the response data
   */
  protected async post<T>(url: string, data: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.apiClient.post(url, data, config);
    return response.data;
  }

  /**
   * Execute a PUT request
   * @param url The endpoint URL
   * @param data The data to send
   * @param config Optional Axios request configuration
   * @returns Promise with the response data
   */
  protected async put<T>(url: string, data: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.apiClient.put(url, data, config);
    return response.data;
  }

  /**
   * Execute a DELETE request
   * @param url The endpoint URL
   * @param config Optional Axios request configuration
   * @returns Promise with the response data
   */
  protected async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.apiClient.delete(url, config);
    return response.data;
  }

  /**
   * Build query parameters for API requests
   * @param params Object containing parameters
   * @returns URL query string
   */
  protected buildQueryParams(params: Record<string, any>): string {
    const queryParams = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (Array.isArray(value)) {
          value.forEach(item => {
            queryParams.append(`${key}`, String(item));
          });
        } else {
          queryParams.append(key, String(value));
        }
      }
    });

    const queryString = queryParams.toString();
    return queryString ? `?${queryString}` : '';
  }
}

export default api;
