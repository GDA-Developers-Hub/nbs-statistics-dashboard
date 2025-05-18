import React, { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import axios from 'axios';

// API base URL - should be moved to environment config in production
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

interface User {
  id: string;
  email: string;
  role: string;
  full_name: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

// Authentication refresh interval (1 minute)
const REFRESH_INTERVAL = 60 * 1000;

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);
  const [initialCheckDone, setInitialCheckDone] = useState<boolean>(false);

  // Memoize the checkAuth function to prevent re-creation on each render
  const checkAuth = useCallback(async (): Promise<boolean> => {
    const token = localStorage.getItem('accessToken');
    
    if (!token) {
      setIsAuthenticated(false);
      setUser(null);
      return false;
    }
    
    try {
      // Verify token by fetching user data
      const response = await axios.get(`${API_BASE_URL}/users/me/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setUser(response.data);
      setIsAuthenticated(true);
      return true;
    } catch (error) {
      // If token verification fails, try to refresh
      const refreshToken = localStorage.getItem('refreshToken');
      
      if (!refreshToken) {
        logout();
        return false;
      }
      
      try {
        const refreshResponse = await axios.post(`${API_BASE_URL}/token/refresh/`, {
          refresh: refreshToken
        });
        
        localStorage.setItem('accessToken', refreshResponse.data.access);
        
        // Retry user info
        const userResponse = await axios.get(`${API_BASE_URL}/users/me/`, {
          headers: {
            'Authorization': `Bearer ${refreshResponse.data.access}`
          }
        });
        
        setUser(userResponse.data);
        setIsAuthenticated(true);
        return true;
      } catch (refreshError) {
        // If refresh fails, clear auth
        logout();
        return false;
      }
    }
  }, []);

  // Set up axios interceptor for adding token to requests
  useEffect(() => {
    const requestInterceptor = axios.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('accessToken');
        if (token) {
          config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Set up response interceptor for handling token expiration
    const responseInterceptor = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        
        // If error is 401 and we haven't already tried to refresh the token
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            // Attempt to refresh the token
            const refreshToken = localStorage.getItem('refreshToken');
            if (!refreshToken) {
              // No refresh token, force logout
              await logout();
              return Promise.reject(error);
            }
            
            const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
              refresh: refreshToken
            });
            
            const { access } = response.data;
            localStorage.setItem('accessToken', access);
            
            // Retry original request with new token
            originalRequest.headers['Authorization'] = `Bearer ${access}`;
            return axios(originalRequest);
          } catch (refreshError) {
            // Refresh token failed, force logout
            await logout();
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );

    // Clean up
    return () => {
      axios.interceptors.request.eject(requestInterceptor);
      axios.interceptors.response.eject(responseInterceptor);
    };
  }, []);

  // Initial auth check on component mount
  useEffect(() => {
    if (!initialCheckDone) {
      checkAuth().finally(() => {
        setInitialCheckDone(true);
      });
    }
  }, [checkAuth, initialCheckDone]);
  
  // Set up interval to check auth token expiration
  useEffect(() => {
    // Skip setting up interval if not authenticated yet
    if (!isAuthenticated) return;
    
    const interval = setInterval(checkAuth, REFRESH_INTERVAL);
    
    // Clean up
    return () => {
      clearInterval(interval);
    };
  }, [isAuthenticated, checkAuth]);

  const login = async (email: string, password: string) => {
    try {
      // Authenticate with backend
      const response = await axios.post(`${API_BASE_URL}/token/`, {
        email,
        password,
      });
      
      // Extract tokens
      const { access, refresh } = response.data;
      
      // Store tokens
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      localStorage.setItem('isAuthenticated', 'true');
      
      // Get user information
      const userResponse = await axios.get(`${API_BASE_URL}/users/me/`, {
        headers: {
          'Authorization': `Bearer ${access}`
        }
      });
      
      // Store user details
      const userData = userResponse.data;
      localStorage.setItem('userRole', userData.role);
      localStorage.setItem('userEmail', userData.email);
      
      setUser(userData);
      setIsAuthenticated(true);
      
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      // Call the backend logout endpoint if we're authenticated
      const token = localStorage.getItem('accessToken');
      if (token) {
        await axios.post(`${API_BASE_URL}/users/logout/`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
      }
    } catch (error) {
      console.error('Error during logout:', error);
      // Continue with logout even if the server call fails
    } finally {
      // Clear all auth data
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userRole');
      localStorage.removeItem('userEmail');
      
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const value = {
    isAuthenticated,
    user,
    login,
    logout,
    checkAuth
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext; 