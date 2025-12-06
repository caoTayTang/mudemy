import axiosClient from '../api/axiosClient';

export const authService = {
  /**
   * Logs in the user.
   * Endpoint: POST /api/auth/login
   */
  login: async (username, password, role) => {
    const response = await axiosClient.post('/api/auth/login', { 
      username, 
      password,
      role // Now dynamic based on user selection
    });
    return response; 
  },

  getMe: async () => {
    return await axiosClient.get('/api/users/me');
  },

  getRoles: async () => {
    return await axiosClient.get('/api/auth/roles');
  },

  logout: async () => {
    try {
      await axiosClient.post('/api/auth/logout');
    } finally {
      localStorage.removeItem('token');
    }
  }
};