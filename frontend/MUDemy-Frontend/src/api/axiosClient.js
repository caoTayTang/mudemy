import axios from 'axios';

// Create an Axios instance with default configuration
const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- REQUEST INTERCEPTOR ---
// Automatically adds the Authorization token to every request if it exists
axiosClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// --- RESPONSE INTERCEPTOR ---
// Handles global responses and errors
axiosClient.interceptors.response.use(
  (response) => {
    // Return the data directly to simplify usage in services
    return response.data;
  },
  (error) => {
    // specific error handling
    if (error.response) {
      // 401: Unauthorized (Token expired or invalid)
      if (error.response.status === 401) {
        // Only redirect if we aren't already on the login page to avoid loops
        if (window.location.pathname !== '/login') {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
      }
      
      // Return the error message from the backend if available
      return Promise.reject(error.response.data);
    }
    
    // Network or other errors
    return Promise.reject(error);
  }
);

export default axiosClient;