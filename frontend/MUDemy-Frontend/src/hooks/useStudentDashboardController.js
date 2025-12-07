import { useState, useEffect } from 'react';
import { studentService } from '../services/studentService';
import { courseService } from '../services/courseService';
import { useAuth } from '../context/AuthContext';

export const useStudentDashboardController = () => {
  const { logout } = useAuth();
  
  const [user, setUser] = useState(null);
  const [courses, setCourses] = useState([]); // Raw data
  const [loading, setLoading] = useState(true);
  
  // --- FILTER & SORT STATE ---
  const [activeTab, setActiveTab] = useState('all'); 
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("recent"); // Options: 'recent', 'title_az', 'progress_desc', 'progress_asc'

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [userData, coursesData] = await Promise.all([
          studentService.getStudentProfile(),
          studentService.getEnrolledCourses()
        ]);
        
        setUser(userData.data || userData);
        setCourses(coursesData);
      } catch (error) {
        console.error("Failed to load dashboard data", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // --- DATA PROCESSING PIPELINE ---
  const processedCourses = courses
    // 1. Filter by Tab
    .filter(course => {
      if (activeTab === 'all') return true;
      // Logic: Completed if status is 'Completed' OR progress is 100%
      const isCompleted = course.status === 'Completed' || course.progress === 100;
      if (activeTab === 'in-progress') return !isCompleted;
      if (activeTab === 'completed') return isCompleted;
      return true;
    })
    // 2. Filter by Search Term (Title)
    .filter(course => 
      course.title.toLowerCase().includes(searchTerm.toLowerCase())
    )
    // 3. Sort
    .sort((a, b) => {
      switch (sortBy) {
        case 'title_az':
          return a.title.localeCompare(b.title);
        case 'progress_desc': // High to Low
          return b.progress - a.progress;
        case 'progress_asc': // Low to High
          return a.progress - b.progress;
        case 'recent':
        default:
          // Assuming higher ID = newer if no date available, or keep API order
          return 0;
      }
    });

  const handleCheckPrerequisites = async (courseId) => {
    if (!courseId) return;
    const missing = await courseService.checkPrerequisites(courseId);
    if (missing && missing.length > 0) {
      const titles = missing.map(c => `• ${c.Title}`).join('\n');
      alert(`⚠️ You are missing the following prerequisites:\n\n${titles}\n\nPlease complete these before continuing.`);
    } else {
      alert("✅ All prerequisites met! You are good to go.");
    }
  };

  const handleLogout = () => {
    logout(); 
  };

  return {
    user,
    courses: processedCourses, // Return the processed list
    rawCount: courses.length, // Useful for global stats
    loading,
    // Export State & Setters
    activeTab,
    setActiveTab,
    searchTerm,
    setSearchTerm,
    sortBy,
    setSortBy,
    actions: {
      handleCheckPrerequisites,
      handleLogout
    }
  };
};