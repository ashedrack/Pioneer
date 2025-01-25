import api from './api';

export interface LoginData {
  email: string;
  password: string;
}

export interface SignUpData {
  email: string;
  password: string;
  full_name: string;
  company: string;
  region: string;
  phone?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export const login = async (data: LoginData): Promise<AuthResponse> => {
  try {
    const response = await api.post('/auth/login', data);
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  } catch (error: any) {
    console.error('Login error:', error.response?.data);
    throw error;
  }
};

export const signUp = async (data: SignUpData): Promise<AuthResponse> => {
  try {
    const response = await api.post('/auth/signup', data);
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  } catch (error: any) {
    console.error('Signup error:', error.response?.data);
    throw error;
  }
};

export const logout = () => {
  localStorage.removeItem('token');
};

export const verifyToken = async (): Promise<boolean> => {
  try {
    await api.get('/auth/verify');
    return true;
  } catch (error) {
    return false;
  }
};
