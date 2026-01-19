import request from '@/utils/request';
import { User, LoginRequest, RegisterRequest, AuthToken } from '@/types';

export const authApi = {
  // Login
  login: (data: LoginRequest) => {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);
    return request.post<any, AuthToken>('/auth/login', formData);
  },

  // Register
  register: (data: RegisterRequest) => {
    return request.post<any, User>('/auth/register', data);
  },

  // Get current user info
  getCurrentUser: () => {
    return request.get<any, User>('/auth/me');
  },

  // Change password
  changePassword: (data: { old_password: string; new_password: string }) => {
    return request.post<any, { message: string }>('/auth/change-password', data);
  },
};
