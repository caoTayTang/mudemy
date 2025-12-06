import { useState, useEffect } from 'react';
import { courseService } from '../services/courseService';

/**
 * Home Controller (Hook)
 * Manages the logic for the Home Page, including data fetching
 * and search state.
 */
export const useHomeController = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true);
        const data = await courseService.getFeaturedCourses();
        setCourses(data);
      } catch (error) {
        console.error("Failed to fetch courses", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  // Basic filtering logic for the view
  const filteredCourses = courses.filter(course => 
    course.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return {
    courses: filteredCourses,
    loading,
    searchQuery,
    handleSearchChange
  };
};