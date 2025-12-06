import { useState, useEffect } from 'react';
import { studentService } from '../services/studentService';

export const useStudentDashboardController = () => {
  const [user, setUser] = useState(null);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'in-progress', 'completed'

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [userData, coursesData] = await Promise.all([
          studentService.getStudentProfile(),
          studentService.getEnrolledCourses()
        ]);
        
        // Handle case where user data might be nested (e.g. userData.data)
        console.info("User Data:", userData);
        console.info("Courses Data:", coursesData);
        setUser(userData);
        setCourses(coursesData);
      } catch (error) {
        console.error("Failed to load dashboard data", error);
        // Optional: Redirect to login if 401, though axiosClient handles this globally
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Filter courses based on active tab
  const filteredCourses = courses.filter(course => {
    if (activeTab === 'all') return true;
    if (activeTab === 'in-progress') return course.progress < 100;
    if (activeTab === 'completed') return course.progress === 100;
    return true;
  });

  return {
    user,
    courses: filteredCourses,
    loading,
    activeTab,
    setActiveTab
  };
};