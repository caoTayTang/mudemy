import { useState, useEffect } from 'react';
import { courseService } from '../services/courseService';
import { authService } from '../services/authService'; // Import Auth Service
import { useNavigate } from 'react-router-dom';

/**
 * Home Controller (Hook)
 * Manages the logic for the Home Page (Catalog).
 */
export const useHomeController = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [user, setUser] = useState(null); // NEW: Track Logged-in User
  
  const [modalState, setModalState] = useState({
    isOpen: false,
    type: null,
    data: null,
    courseId: null
  });

  useEffect(() => {
    const initData = async () => {
      setLoading(true);
      try {
        // 1. Fetch Public Courses
        const coursesData = await courseService.getFeaturedCourses();
        setCourses(coursesData);
        
        // 2. Check Login Status
        const token = localStorage.getItem('token');
        if (token) {
          try {
            const userData = await authService.getMe();
            // Handle backend response structure (response.user or direct object)
            setUser(userData.user || userData); 
          } catch (authErr) {
            console.warn("Token invalid or expired", authErr);
            // Optional: localStorage.removeItem('token');
          }
        }
        
        setError(null);
      } catch (err) {
        console.error("Failed to fetch initial data", err);
        setError("Could not load courses. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    initData();
  }, []);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const filteredCourses = courses.filter(course => 
    course.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // --- Prerequisite Check Logic ---
  const handleCheckPrerequisites = async (courseId) => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      setModalState({ isOpen: true, type: 'login_prompt', courseId });
      return;
    }

    try {
      const missing = await courseService.checkPrerequisites(courseId);
      
      if (missing && missing.length > 0) {
        setModalState({ isOpen: true, type: 'missing', data: missing, courseId });
      } else {
        setModalState({ isOpen: true, type: 'success', data: null, courseId });
      }
    } catch (err) {
      setModalState({ isOpen: true, type: 'error' });
    }
  };

  const closeModal = () => {
    setModalState(prev => ({ ...prev, isOpen: false }));
  };

  // NEW: Logout Action
  const handleLogout = async () => {
    await authService.logout();
    setUser(null);
    navigate('/');
  };

  return {
    courses: filteredCourses,
    loading,
    error,
    searchQuery,
    modalState,
    user, // Expose user state to View
    actions: {
      handleSearchChange,
      handleCheckPrerequisites,
      closeModal,
      handleLogout
    }
  };
};