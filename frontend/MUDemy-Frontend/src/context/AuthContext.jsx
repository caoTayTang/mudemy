import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // 1. Check for existing session on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await authService.getMe();
          setUser(userData.user || userData);
        } catch (error) {
          console.error("Session expired or invalid:", error);
          localStorage.removeItem('token');
          setUser(null);
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  // 2. Global Login Action
  const login = async (username, password, role) => {
    try {
      const data = await authService.login(username, password, role);
      const token = data.access_token || data.token;
      
      if (token) {
        localStorage.setItem('token', token);
        // Fetch user immediately to update UI
        const userData = await authService.getMe();
        setUser(userData.user || userData);
        return true;
      }
      return false;
    } catch (error) {
      throw error;
    }
  };

  // 3. Global Logout Action
  const logout = async () => {
    await authService.logout();
    setUser(null);
    navigate('/');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context easily
export const useAuth = () => useContext(AuthContext);