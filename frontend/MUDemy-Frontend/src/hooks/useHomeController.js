import { useState, useEffect } from 'react';
import { courseService } from '../services/courseService';
import { authService } from '../services/authService';
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
  const [user, setUser] = useState(null);
  
  // --- FILTER & SORT STATE ---
  const [searchQuery, setSearchQuery] = useState("");
  const [difficulty, setDifficulty] = useState("All"); // 'All', 'Beginner', 'Intermediate', 'Advanced'
  const [sortBy, setSortBy] = useState("title_asc"); // 'title_asc', 'title_desc'

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
        const coursesData = await courseService.getFeaturedCourses();
        setCourses(coursesData);
        
        const token = localStorage.getItem('token');
        if (token) {
          try {
            const userData = await authService.getMe();
            setUser(userData.user || userData); 
          } catch (authErr) {
            console.warn("Token invalid or expired", authErr);
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

  // --- DATA PROCESSING PIPELINE ---
  const processedCourses = courses
    // 1. Filter by Search
    .filter(course => 
      course.title.toLowerCase().includes(searchQuery.toLowerCase())
    )
    // 2. Filter by Difficulty
    .filter(course => {
      if (difficulty === "All") return true;
      return course.level === difficulty;
    })
    // 3. Sort
    .sort((a, b) => {
      switch (sortBy) {
        case 'title_asc':
          return a.title.localeCompare(b.title);
        case 'title_desc':
          return b.title.localeCompare(a.title);
        default:
          return 0;
      }
    });

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

  const handleLogout = async () => {
    await authService.logout();
    setUser(null);
    navigate('/');
  };

  return {
    courses: processedCourses, // Export processed list
    loading,
    error,
    modalState,
    user,
    // Export Filter State
    filters: { searchQuery, difficulty, sortBy },
    actions: {
      setSearchQuery,
      setDifficulty,
      setSortBy,
      handleCheckPrerequisites,
      closeModal,
      handleLogout
    }
  };
};