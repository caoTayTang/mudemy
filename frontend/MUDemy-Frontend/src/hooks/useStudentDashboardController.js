import { useState, useEffect } from 'react';
import { studentService } from '../services/studentService';
import { courseService } from '../services/courseService'; // Import course service

export const useStudentDashboardController = () => {
  const [user, setUser] = useState(null);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all'); 

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

  const filteredCourses = courses.filter(course => {
    if (activeTab === 'all') return true;
    if (activeTab === 'in-progress') return course.progress < 100;
    if (activeTab === 'completed') return course.progress === 100;
    return true;
  });

  // NEW: Handler for checking prerequisites
  const handleCheckPrerequisites = async (courseId) => {
    const missing = await courseService.checkPrerequisites(courseId);
    
    if (missing.length > 0) {
      const titles = missing.map(c => `• ${c.Title}`).join('\n');
      alert(`⚠️ You are missing the following prerequisites:\n\n${titles}\n\nPlease complete these before continuing.`);
    } else {
      alert("✅ All prerequisites met! You are good to go.");
    }
  };

  return {
    user,
    courses: filteredCourses,
    loading,
    activeTab,
    setActiveTab,
    actions: {
      handleCheckPrerequisites // Expose action
    }
  };
};