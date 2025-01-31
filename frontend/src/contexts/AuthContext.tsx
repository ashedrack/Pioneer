import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { login as loginApi, signUp as signUpApi, checkSession } from '../api/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signUp: (data: any) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

const getStoredToken = () => {
  try {
    return localStorage.getItem('token');
  } catch (error) {
    console.error('Error accessing localStorage:', error);
    return null;
  }
};

const setStoredToken = (token: string) => {
  try {
    localStorage.setItem('token', token);
    return true;
  } catch (error) {
    console.error('Error setting token in localStorage:', error);
    return false;
  }
};

const removeStoredToken = () => {
  try {
    localStorage.removeItem('token');
    return true;
  } catch (error) {
    console.error('Error removing token from localStorage:', error);
    return false;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  useEffect(() => {
    const validateSession = async () => {
      const token = getStoredToken();
      if (token) {
        try {
          const isValid = await checkSession();
          setIsAuthenticated(isValid);
          if (!isValid) {
            removeStoredToken();
            navigate('/login');
          }
        } catch (error) {
          console.error('Session validation error:', error);
          setIsAuthenticated(false);
          removeStoredToken();
          navigate('/login');
        }
      } else {
        setIsAuthenticated(false);
      }
      setLoading(false);
    };

    validateSession();
  }, [navigate]);

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      const response = await loginApi({ email, password });
      const success = setStoredToken(response.access_token);
      if (success) {
        setIsAuthenticated(true);
        navigate('/dashboard');
      } else {
        throw new Error('Failed to store authentication token');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signUp = async (data: any) => {
    try {
      setLoading(true);
      const response = await signUpApi(data);
      const success = setStoredToken(response.access_token);
      if (success) {
        setIsAuthenticated(true);
        navigate('/dashboard');
      } else {
        throw new Error('Failed to store authentication token');
      }
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    removeStoredToken();
    setIsAuthenticated(false);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, loading, login, signUp, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
