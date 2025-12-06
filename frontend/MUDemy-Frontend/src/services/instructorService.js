import axiosClient from '../api/axiosClient';

/**
 * Instructor Service (Model)
 * Performs CRUD operations for Courses.
 */
export const instructorService = {
  // --- READ ---
  getProfile: async () => {
    // Re-using the /me endpoint as it returns the instructor info
    const response = await axiosClient.get('/api/users/me');
    return response.user || response;
  },

  getCourses: async (user_id) => {
    // Assuming backend has an endpoint to get courses for the current instructor
    // If not, we might filter /api/courses. For now, using the instructor specific endpoint from your checklist
    // GET /api/instructors/{user_id}/courses
    // Note: We need the userID first. This might require a two-step call in the controller 
    // or a specialized endpoint like /api/courses/my-courses if it existed.
    // Fallback: Get ALL courses and filter (not ideal for prod but works for assignment)
    const response = await axiosClient.get(`/api/instructors/${user_id}/courses`);
    const courses = response.courses || [];
    console.log("Instructor courses response:", courses);
    
    const detailedCourses = await Promise.all(
    courses.map(async (course) => {
      try {
        // Handle different ID casing from backend
        const courseId = course.CourseID;
        const detailResponse = await axiosClient.get(`/api/courses/id/${courseId}`);
        return detailResponse.course;
      } catch (err) {
        console.warn(`Failed to hydrate course ${course.id || 'unknown'}`, err);
        return course; 
      }
    })
  );

  return detailedCourses;

  },

  getCourseDetails: async (courseId) => {
    return await axiosClient.get(`/api/courses/id/${courseId}`);
  },

  // --- CREATE ---
  createCourse: async (courseData) => {
    // 1. Create the Course entry first
    // Expected Output: { status: "created", course_id: "..." }
    const courseResponse = await axiosClient.post('/api/courses', courseData);
    // Normalize the ID (Backend might return course_id, CourseID, or id)
    if (!courseResponse.course_id) {
      throw new Error("Course created but no ID returned from backend.");
    }

    // 2. Fetch User Info to get ID for the INSTRUCT table
    // (We fetch fresh here to ensure we have the correct UserID for the transaction)
    const userResponse = await axiosClient.get('/api/users/me');
    console.log("User response for course creation:", userResponse);
    const userObj = userResponse.user;
    const userId = userObj.UserID;

    // 3. Insert into INSTRUCT table (Link User -> Course)
    if (userId) {
      const resp = await axiosClient.post('/api/instruct', { 
        UserID: userId, 
        CourseID: courseResponse.course_id 
      });
      
      if (resp.status !== "assigned") {
        console.error("Failed to link instructor to course:", resp);
        throw new Error(`${resp.detail}`);
      }

    }

    return courseResponse;
  },


  // --- UPDATE ---
  updateCourse: async (courseId, courseData) => {
    // PUT /api/courses/{course_id}
    return await axiosClient.put(`/api/courses/${courseId}`, courseData);
  },

  // --- DELETE ---
  deleteCourse: async (courseId) => {
    // DELETE /api/courses/{course_id}
    return await axiosClient.delete(`/api/courses/${courseId}`);
  }
};