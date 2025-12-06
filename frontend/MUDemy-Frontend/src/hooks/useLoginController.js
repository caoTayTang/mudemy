import { useState } from 'react';
import { authService } from '../services/authService';
import { useNavigate } from 'react-router-dom';

export const useLoginController = () => {
  const navigate = useNavigate();
  const [authMode, setAuthMode] = useState('login'); 

  const [formData, setFormData] = useState({
    username: '',
    password: '',
    fullName: '',
    role: 'tutee' // Default to 'tutee' to match API requirements
  });

  const [status, setStatus] = useState({
    loading: false,
    error: null,
    success: false
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
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
        // Now passing the role correctly from form data
        const data = await authService.login(formData.username, formData.password, formData.role);
        
        // Handle Token from your specific API response structure
        // Assuming your backend might return token in headers or body
        // Adjust if your API returns { status: "Login successful" } but sets cookie
        const token = data.access_token || data.token; 
        
        if (token) {
          localStorage.setItem('token', token);
        } else {
          // If using cookies, we might just assume success
          console.log("No token in body, assuming cookie set.");
        }

        // Redirect based on role
        if (formData.role === 'tutor') {
          navigate('/instructor/courses');
        } else {
          navigate('/');
        }
        
        setStatus({ loading: false, error: null, success: true });
      } else {
        // Register Logic placeholder
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