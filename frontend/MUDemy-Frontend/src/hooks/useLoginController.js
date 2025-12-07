import { useState } from 'react';
import { useAuth } from '../context/AuthContext'; // Use Context
import { useNavigate, useLocation } from 'react-router-dom';

export const useLoginController = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth(); // Destructure login from context
  
  const [authMode, setAuthMode] = useState('login'); 

  const [formData, setFormData] = useState({
    username: '',
    password: '',
    fullName: '',
    role: 'tutee' 
  });

  const [status, setStatus] = useState({
    loading: false,
    error: null,
    success: false
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (status.error) setStatus(prev => ({ ...prev, error: null }));
  };

  const toggleAuthMode = (mode) => {
    setAuthMode(mode);
    setStatus({ loading: false, error: null, success: false });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus({ loading: true, error: null, success: false });

    try {
      if (authMode === 'login') {
        // Use Global Login
        await login(formData.username, formData.password, formData.role);
        
        setStatus({ loading: false, error: null, success: true });
        
        // Redirect Logic
        // 1. Check if redirected from a protected page (e.g. they tried to visit /dashboard)
        const origin = location.state?.from?.pathname;
        if (origin) {
          navigate(origin);
        } 
        // 2. Else go to role-specific home
        else if (formData.role === 'tutor') {
          navigate('/instructor/courses');
        } else {
          navigate('/');
        }
      } else {
        console.log("Registering:", formData);
        await new Promise(resolve => setTimeout(resolve, 1000));
        navigate('/'); 
      }
    } catch (err) {
      console.error("Login Error:", err);
      const errorMessage = err.detail || err.message || "Login failed. Please check your credentials.";
      setStatus({ loading: false, error: errorMessage, success: false });
    }
  };

  return {
    authMode,
    toggleAuthMode,
    formData,
    status,
    handleInputChange,
    handleSubmit
  };
};