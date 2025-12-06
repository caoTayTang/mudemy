import { useState, useEffect } from 'react';
import { instructorService } from '../services/instructorService';

export const useInstructorCourseController = () => {
  const [profile, setProfile] = useState(null);
  const [coursesList, setCoursesList] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // NEW: State for Related Data (Multi-table requirement)
  const [courseModules, setCourseModules] = useState([]);
  const [courseEnrollments, setCourseEnrollments] = useState([]);

  // State for Filtering & Sorting
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("title");

  // State for Forms
  const [isEditing, setIsEditing] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({ Title: "", Description: "", Difficulty: "Beginner", Language: "English" });
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
    
    // Clear previous related data
    setCourseModules([]);
    setCourseEnrollments([]);

    try {
      // Fetch Master (Course) + Details (Modules, Enrollments) in parallel
      const [detail, modules, enrollments] = await Promise.all([
        instructorService.getCourseDetails(courseId),
        instructorService.getModules(courseId),
        instructorService.getEnrollments(courseId)
      ]);

      const courseObj = detail.course || detail; 
      setSelectedCourse(courseObj);
      setCourseModules(modules);
      setCourseEnrollments(enrollments);

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

  // ... (Create/Edit/Delete/Validation handlers remain mostly same)
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
    setSubmitting(true);
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
      setSubmitting(false);
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
    relatedData: { modules: courseModules, enrollments: courseEnrollments }, // Export related data
    loading,
    formState: { isEditing, isCreating, formData, error, submitting },
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