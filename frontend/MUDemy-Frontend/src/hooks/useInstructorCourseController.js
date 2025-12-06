import { useState, useEffect } from 'react';
import { instructorService } from '../services/instructorService';

export const useInstructorCourseController = () => {
  const [profile, setProfile] = useState(null);
  const [coursesList, setCoursesList] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // State for Filtering & Sorting
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("title");

  // State for Forms
  const [isEditing, setIsEditing] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [submitting, setSubmitting] = useState(false); // NEW: Track submission status
  const [formData, setFormData] = useState({ Title: "", Description: "", Difficulty: "Beginner", Language: "English" });
  
  // ERROR HANDLING STATE
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const profileData = await instructorService.getProfile();
      setProfile(profileData);

      const userId = profileData.UserID || profileData.id;
      if (userId) {
        const coursesData = await instructorService.getCourses(userId);
        setCoursesList(coursesData);
      }
    } catch (err) {
      console.error("Load failed", err);
    } finally {
      setLoading(false);
    }
  };

  const filteredAndSortedCourses = coursesList
    .filter(course => 
      (course.Title || "").toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      const titleA = a.Title || "";
      const titleB = b.Title || "";
      const diffA = a.Difficulty || "";
      const diffB = b.Difficulty || "";

      if (sortBy === 'title') return titleA.localeCompare(titleB);
      if (sortBy === 'difficulty') return diffA.localeCompare(diffB);
      return 0;
    });

  const handleSelectCourse = async (courseId) => {
    setIsCreating(false);
    setIsEditing(false);
    setLoading(true);
    try {
      const detail = await instructorService.getCourseDetails(courseId);
      const courseObj = detail.course || detail; 
      setSelectedCourse(courseObj);
      setFormData({
        Title: courseObj.Title || "",
        Description: courseObj.Description || "",
        Difficulty: courseObj.Difficulty || "Beginner",
        Language: courseObj.Language || "English"
      });
    } catch (err) {
      console.error("Select failed", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateInit = () => {
    setSelectedCourse(null);
    setFormData({ Title: "", Description: "", Difficulty: "Beginner", Language: "English" });
    setIsCreating(true);
    setIsEditing(false);
    setError(null);
  };

  const handleEditInit = () => {
    setIsEditing(true);
    setIsCreating(false);
    setError(null);
  };

  const handleDelete = async (courseId) => {
    if (!window.confirm("Are you sure you want to delete this course? This action cannot be undone.")) return;
    
    try {
      await instructorService.deleteCourse(courseId);
      await loadData();
      setSelectedCourse(null);
    } catch (err) {
      const msg = err.detail || err.message || "Failed to delete course.";
      alert(`Error: ${msg}`);
    }
  };

  const validateForm = () => {
    if (!formData.Title.trim()) return "Course Title is required.";
    if (!formData.Description.trim()) return "Course Description is required.";
    if (formData.Title.length < 5) return "Title must be at least 5 characters.";
    return null;
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setError(null);

    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    setSubmitting(true); // START LOADING

    try {
      if (isCreating) {
        await instructorService.createCourse(formData);
      } else if (isEditing && selectedCourse) {
        const cId = selectedCourse.CourseID || selectedCourse.id;
        await instructorService.updateCourse(cId, formData);
      }
      
      setIsCreating(false);
      setIsEditing(false);
      await loadData();
      
      if (isEditing && selectedCourse) {
        const cId = selectedCourse.CourseID || selectedCourse.id;
        handleSelectCourse(cId);
      }
    } catch (err) {
      console.error("Save failed", err);
      const backendMsg = err.detail || err.message || "An unexpected database error occurred.";
      setError(backendMsg);
    } finally {
      setSubmitting(false); // STOP LOADING
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return {
    profile,
    courses: filteredAndSortedCourses,
    selectedCourse,
    loading,
    formState: { isEditing, isCreating, formData, error, submitting }, // Export submitting state
    filterState: { searchTerm, sortBy },
    actions: {
      setSearchTerm,
      setSortBy,
      handleSelectCourse,
      handleCreateInit,
      handleEditInit,
      handleDelete,
      handleSave,
      handleInputChange,
      cancelForm: () => { setIsEditing(false); setIsCreating(false); }
    }
  };
};