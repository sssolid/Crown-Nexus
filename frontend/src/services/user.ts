// frontend/src/services/user.ts
/**
 * User API service.
 *
 * This service provides methods for interacting with the user management API:
 * - Fetching, creating, updating, and deleting users
 * - Managing user preferences and settings
 * - Handling company associations
 * - Managing user permissions
 *
 * It builds on the base API service and adds user-specific functionality.
 */

import api, {ApiService} from '@/services/api';
import { User, UserRole } from '@/types/user';

// User list response interface
export interface UserListResponse {
  items: User[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

// User filter parameters
export interface UserFilters {
  search?: string;
  role?: UserRole;
  is_active?: boolean;
  company_id?: string;
  page?: number;
  page_size?: number;
}

// Company interface (simplified)
export interface Company {
  id: string;
  name: string;
  account_number: string;
  account_type: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// User create/update payload
export interface UserPayload {
  email: string;
  full_name: string;
  password?: string;
  role: UserRole;
  is_active: boolean;
  company_id?: string | null;
}

// User preferences payload
export interface UserPreferences {
  theme?: 'light' | 'dark' | 'system';
  dashboard_widgets?: string[];
  notifications_enabled?: boolean;
  language?: string;
  timezone?: string;
}

/**
 * User service for API interactions.
 */
export class UserService extends ApiService  {
  /**
   * Get a paginated list of users with optional filtering.
   *
   * @param filters - Optional filter parameters
   * @returns Promise with user list response
   */
  async getUsers(filters?: UserFilters): Promise<UserListResponse> {
    return api.get<UserListResponse>('/users', { params: filters });
  }

  /**
   * Get a single user by ID.
   *
   * @param id - User ID
   * @returns Promise with user details
   */
  async getUser(id: string): Promise<User> {
    return api.get<User>(`/users/${id}`);
  }

  /**
   * Create a new user.
   *
   * @param userData - User data
   * @returns Promise with created user
   */
  async createUser(userData: UserPayload): Promise<User> {
    return api.post<User>('/users', userData);
  }

  /**
   * Update an existing user.
   *
   * @param id - User ID
   * @param userData - Updated user data
   * @returns Promise with updated user
   */
  async updateUser(id: string, userData: Partial<UserPayload>): Promise<User> {
    return api.put<User>(`/users/${id}`, userData);
  }

  /**
   * Delete a user.
   *
   * @param id - User ID
   * @returns Promise with deletion response
   */
  async deleteUser(id: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/users/${id}`);
  }

  /**
   * Get a list of all companies.
   *
   * @returns Promise with list of companies
   */
  async getCompanies(): Promise<Company[]> {
    return api.get<Company[]>('/companies');
  }

  /**
   * Get a single company by ID.
   *
   * @param id - Company ID
   * @returns Promise with company details
   */
  async getCompany(id: string): Promise<Company> {
    return api.get<Company>(`/companies/${id}`);
  }

  /**
   * Update user preferences.
   *
   * @param id - User ID
   * @param preferences - User preferences
   * @returns Promise with updated preferences
   */
  async updateUserPreferences(id: string, preferences: UserPreferences): Promise<UserPreferences> {
    return api.put<UserPreferences>(`/users/${id}/preferences`, preferences);
  }

  /**
   * Get user preferences.
   *
   * @param id - User ID
   * @returns Promise with user preferences
   */
  async getUserPreferences(id: string): Promise<UserPreferences> {
    return api.get<UserPreferences>(`/users/${id}/preferences`);
  }

  /**
   * Change user password.
   *
   * @param id - User ID
   * @param currentPassword - Current password for verification
   * @param newPassword - New password
   * @returns Promise with result
   */
  async changePassword(id: string, currentPassword: string, newPassword: string): Promise<{message: string}> {
    return api.post<{message: string}>(`/users/${id}/change-password`, {
      current_password: currentPassword,
      new_password: newPassword
    });
  }

  /**
   * Send password reset email to user.
   *
   * @param email - User email
   * @returns Promise with result
   */
  async sendPasswordReset(email: string): Promise<{message: string}> {
    return api.post<{message: string}>('/users/reset-password', { email });
  }

  /**
   * Reset password with token from email.
   *
   * @param token - Reset token
   * @param newPassword - New password
   * @returns Promise with result
   */
  async resetPassword(token: string, newPassword: string): Promise<{message: string}> {
    return api.post<{message: string}>('/users/reset-password/confirm', {
      token,
      new_password: newPassword
    });
  }

  /**
   * Get user activity logs.
   *
   * @param id - User ID
   * @param page - Page number
   * @param pageSize - Items per page
   * @returns Promise with activity logs
   */
  async getUserActivityLogs(id: string, page: number = 1, pageSize: number = 10): Promise<any> {
    return api.get(`/users/${id}/activity`, {
      params: { page, page_size: pageSize }
    });
  }
}

// Create and export a singleton instance
export const userService = new UserService();
export default userService;
