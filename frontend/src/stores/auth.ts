// frontend/src/stores/auth.ts
/**
 * Authentication store.
 *
 * This store manages authentication state and provides methods for:
 * - User login and logout
 * - Token management
 * - Profile management
 * - Authorization checks
 *
 * It serves as the central source of truth for all authentication-related
 * functionality in the application.
 */

import { defineStore } from 'pinia';
import api from '@/services/api';
import router from '@/router';
import { User, UserRole } from '@/types/user';

// Authentication state interface
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  tokenExpiration: number | null;
}

// Login request interface
interface LoginCredentials {
  username: string;
  password: string;
  rememberMe?: boolean;
}

// Login response interface
interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Token payload interface (decoded JWT)
interface TokenPayload {
  sub: string; // User ID
  exp: number; // Expiration timestamp
  role: UserRole; // User role
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('access_token'),
    isAuthenticated: !!localStorage.getItem('access_token'),
    loading: false,
    error: null,
    tokenExpiration: getTokenExpiration(localStorage.getItem('access_token')),
  }),

  getters: {
    /**
     * Get the current authenticated user.
     *
     * @returns The current user or null if not authenticated
     */
    getUser: (state) => state.user,

    /**
     * Check if the user is logged in.
     *
     * @returns True if authenticated, false otherwise
     */
    isLoggedIn: (state) => state.isAuthenticated,

    /**
     * Check if the user has a specific role.
     *
     * @param role - The role to check
     * @returns True if user has the role, false otherwise
     */
    hasRole: (state) => (role: UserRole) => {
      return state.user?.role === role;
    },

    /**
     * Check if the user has admin privileges.
     *
     * @returns True if user is an admin, false otherwise
     */
    isAdmin: (state) => {
      return state.user?.role === UserRole.ADMIN;
    },

    /**
     * Check if the token is valid and not expired.
     *
     * @returns True if token is valid, false otherwise
     */
    isTokenValid: (state) => {
      if (!state.token || !state.tokenExpiration) return false;
      // Check if token is expired (with 10 second buffer)
      return state.tokenExpiration > Math.floor(Date.now() / 1000) + 10;
    },
  },

  actions: {
    /**
     * Log a user in with credentials.
     *
     * @param credentials - Login credentials
     * @returns Promise with login response
     */
    async login(credentials: LoginCredentials) {
      this.loading = true;
      this.error = null;

      try {
        // Get token from API
        const response = await api.post<LoginResponse>('/auth/login',
          new URLSearchParams({
            username: credentials.username,
            password: credentials.password,
          }),
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          }
        );

        // Store token
        this.token = response.access_token;
        this.isAuthenticated = true;
        this.tokenExpiration = getTokenExpiration(response.access_token);

        // Store token in localStorage if rememberMe is true
        if (credentials.rememberMe) {
          localStorage.setItem('access_token', response.access_token);
        } else {
          // Use sessionStorage for session-only authentication
          sessionStorage.setItem('access_token', response.access_token);
          localStorage.removeItem('access_token');
        }

        // Fetch user profile
        await this.fetchUserProfile();

        // Redirect to originally requested page if available
        const redirectPath = localStorage.getItem('redirectPath') || '/';
        localStorage.removeItem('redirectPath');
        await router.push(redirectPath);

        return response;
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'Login failed';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Log the current user out.
     */
    logout() {
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
      this.tokenExpiration = null;

      // Clear stored tokens
      localStorage.removeItem('access_token');
      sessionStorage.removeItem('access_token');

      // Redirect to login page
      router.push('/login');
    },

    /**
     * Fetch the user profile for the authenticated user.
     *
     * @returns Promise with the user profile
     */
    async fetchUserProfile() {
      if (!this.isAuthenticated || !this.isTokenValid) {
        this.logout();
        return null;
      }

      this.loading = true;

      try {
        const user = await api.get<User>('/auth/me');
        this.user = user;
        return user;
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'Failed to fetch user profile';

        // If 401, token is invalid - logout
        if (error.response?.status === 401) {
          this.logout();
        }
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Initialize the auth store on application start.
     *
     * This checks for an existing token and verifies it,
     * then loads the user profile if valid.
     */
    async initializeAuth() {
      const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');

      if (token) {
        this.token = token;
        this.tokenExpiration = getTokenExpiration(token);
        this.isAuthenticated = true;

        // Check if token is valid
        if (this.isTokenValid) {
          try {
            await this.fetchUserProfile();
          } catch (error) {
            console.error('Failed to initialize auth:', error);
            this.logout();
          }
        } else {
          this.logout();
        }
      }
    },
  },
});

/**
 * Parse and extract the expiration time from a JWT token.
 *
 * @param token - The JWT token
 * @returns The expiration timestamp or null if invalid
 */
function getTokenExpiration(token: string | null): number | null {
  if (!token) return null;

  try {
    // Split token and get payload part
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    // Decode payload
    const payload = JSON.parse(atob(parts[1]));
    return payload.exp || null;
  } catch (error) {
    console.error('Error parsing token:', error);
    return null;
  }
}
