import axiosClient from '../api/axiosClient';
import { courseService } from './courseService';

/**
 * Maps backend enrollment data to the frontend Dashboard structure.
 * Merges raw enrollment data with detailed course info and progress stats.
 */
const mapEnrollmentToFrontend = (enrollment, courseDetails, progressData = []) => {
  // 1. Match Progress: Find stats for this specific CourseID
  // Backend likely returns { CourseID: "...", Percent: 50 } or similar in the progress list
  // const courseProgress = progressData.find(p => p.CourseID === enrollment.CourseID);
  // const courseProgress = 
  const progressPercent = progressData.completion_rate;
  // courseProgress ? courseProgress.Percent : 0;
  return {
    id: enrollment.enrollment_id, // Corrected to match backend DB column
    courseId: enrollment.id, // Corrected to match backend DB column
    
    // 2. Hydrate Missing Data: Use details from the separate course fetch
    title: courseDetails?.title || "Loading Course...",
    instructor: courseDetails?.author || "MUDemy Instructor",
    image: courseDetails?.image || "https://lh3.googleusercontent.com/aida-public/AB6AXuCJvR2L-V_bsDptQ-El7f4IB80ZyZ-SV3qbu6Nom0Ws7UhdYu9Lna_El1veVNYZYuBt9J3loaGHH7UBMhdCeV24v7PyMrdy4vnmTV2zmdYh-93MfjFTAunJirtgwPAdtWkCH8szlG-3IuD_TYV-DExhjkKFP0Dl910ZytvCh7TzUJQL_HjnPfo0tarGFC4Ex47S1WPShmMDOOYJZSgwta3MBsPFw8xwP9rDY4fxAf_j_PucY9UX12yVfQtQaUMkhgKqKSmfYLMVZBc",
    
    // 3. Status & Progress
    status: enrollment.Status || "Active", 
    progress: progressPercent, 
    
    // 4. Curriculum Preview (Optional)
    lessons: courseDetails?.curriculum ? 
      courseDetails.curriculum.slice(0, 3).map((mod, i) => ({
        title: mod.title || `Module ${i+1}`,
        completed: false // Would require deeper 'take' data to map accurately
      })) 
      : []
  };
};

export const studentService = {
  /**
   * Fetch current user profile.
   * Endpoint: GET /api/users/me
   */
  getStudentProfile: async () => {
    const response = await axiosClient.get('/api/users/me');
    return response.user; 
  },

  /**
   * Fetch lesson progress for a specific user.
   * Endpoint: GET /api/takes/{user_id}/progress
   */
  getLessonProgress: async (userId) => {
    try {
      if (!userId) return [];
      const response = await axiosClient.get(`/api/takes/${userId}/progress`);
      console.info("Fetched Progress Data:", response);
      return response.progress || [];
    } catch (error) {
      console.warn("Failed to fetch progress:", error);
      return [];
    }
  },

  /**
   * Fetch enrolled courses and HYDRATE them with course details AND progress.
   * Performs client-side joining of Enrollment + User(for ID) + Progress + Course Details.
   */
  getEnrolledCourses: async () => {
    try {
      // Step A: Get the raw enrollments (Contains IDs only)
      const enrollmentResponse = await axiosClient.get('/api/enrollments/me');
      const rawEnrollments = enrollmentResponse.enrollments || [];
      console.info("raw Enrollments:", rawEnrollments);
      // Step B: Get User ID (Needed to fetch progress)
      // We fetch this here to ensure we have the correct ID for the progress call
      let progressData = [];
      try {
        const userProfile = await studentService.getStudentProfile();
        const userId = userProfile.UserID || userProfile.id;
        
        // Step C: Fetch Progress Stats
        if (userId) {
          progressData = await studentService.getLessonProgress(userId);
          console.info("Progess Data:", progressData);
        }
      } catch (err) {
        console.warn("Could not fetch user ID for progress lookup", err);
      }

      // Step D: Fetch details for every course (Parallel requests)
      // This fills in the missing Titles/Images that the Enrollment table lacks
      const detailedEnrollments = await Promise.all(
        rawEnrollments.map(async (enrollment) => {
          try {
            // Fetch rich course data
            const courseDetails = await courseService.getCourseById(enrollment.id);
            
            // Merge everything
            return mapEnrollmentToFrontend(enrollment, courseDetails, progressData);
          } catch (err) {
            console.warn(`Failed to hydrate course ${enrollment.id}`, err);
            return mapEnrollmentToFrontend(enrollment, {}, progressData); 
          }
        })
      );

      return detailedEnrollments;
    } catch (error) {
      console.error("Failed to fetch enrollments chain:", error);
      return []; 
    }
  }
};