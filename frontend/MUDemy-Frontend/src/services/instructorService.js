import axiosClient from '../api/axiosClient';

/**
 * Instructor Service (Model)
 * Performs CRUD operations for Courses and fetches related Modules/Enrollments.
 */
export const instructorService = {
  // --- READ ---
  getProfile: async () => {
    const response = await axiosClient.get('/api/users/me');
    return response.user;
  },

  getCourses: async (user_id) => {
    try {
      const response = await axiosClient.get(`/api/instructors/${user_id}/courses`);
      const courses = response.courses || [];
      
      // Hydrate with details (Difficulty, Language)
      const detailedCourses = await Promise.all(
        courses.map(async (course) => {
          try {
            const courseId = course.CourseID || course.id || course.courseId;
            if (!courseId) return course;
            const detailResponse = await axiosClient.get(`/api/courses/id/${courseId}`);
            return detailResponse.course || detailResponse;
          } catch (err) {
            return course; 
          }
        })
      );
      return detailedCourses;
    } catch (error) {
      console.error("Failed to fetch instructor courses:", error);
      return [];
    }
  },

  getCourseDetails: async (courseId) => {
    return await axiosClient.get(`/api/courses/id/${courseId}`);
  },

  // --- RELATED DATA ---
  getModules: async (courseId) => {
    try {
      const response = await axiosClient.get(`/api/courses/${courseId}/modules`);
      return response.modules || [];
    } catch (error) {
      console.warn(`Failed to fetch modules for ${courseId}`, error);
      return [];
    }
  },

  getEnrollments: async (courseId) => {
    try {
      const response = await axiosClient.get(`/api/courses/${courseId}/enrollments`);
      return response.enrollments || [];
    } catch (error) {
      console.warn(`Failed to fetch enrollments for ${courseId}`, error);
      return [];
    }
  },

  // --- CREATE ---
  createCourse: async (courseData) => {
    const courseResponse = await axiosClient.post('/api/courses', courseData);
    const newCourseId = courseResponse.course_id || courseResponse.CourseID || courseResponse.id;

    if (!newCourseId) throw new Error("Course created but no ID returned.");

    const userResponse = await axiosClient.get('/api/users/me');
    const userObj = userResponse.user || userResponse;
    const userId = userObj.UserID || userObj.id;

    if (userId) {
      await axiosClient.post('/api/instruct', { 
        UserID: userId, 
        CourseID: newCourseId 
      });
    }
    return courseResponse;
  },

  // --- UPDATE ---
  updateCourse: async (courseId, courseData) => {
    return await axiosClient.put(`/api/courses/${courseId}`, courseData);
  },

  // --- DELETE ---
  deleteCourse: async (courseId) => {
    return await axiosClient.delete(`/api/courses/${courseId}`);
  }
};