import { defineStore } from 'pinia';
import api from '@/services/api';
import { User } from '@/types/user';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

interface LoginCredentials {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('access_token'),
    isAuthenticated: !!localStorage.getItem('access_token'),
    loading: false,
    error: null,
  }),
  
  getters: {
    getUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated,
  },
  
  actions: {
    async login(credentials: LoginCredentials) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await api.post<LoginResponse>('/auth/login', credentials);
        this.user = response.user;
        this.token = response.access_token;
        this.isAuthenticated = true;
        
        localStorage.setItem('access_token', response.access_token);
        
        return response;
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'Login failed';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    logout() {
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem('access_token');
    },
    
    async fetchUserProfile() {
      if (!this.isAuthenticated) return;
      
      this.loading = true;
      
      try {
        const user = await api.get<User>('/users/me');
        this.user = user;
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'Failed to fetch user profile';
        
        // If 401, token is invalid - logout
        if (error.response?.status === 401) {
          this.logout();
        }
      } finally {
        this.loading = false;
      }
    },
  },
});
