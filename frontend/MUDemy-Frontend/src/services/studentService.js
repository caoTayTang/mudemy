import axiosClient from '../api/axiosClient';
import { courseService } from './courseService';

/**
 * Maps backend enrollment data to the frontend Dashboard structure.
 */
const mapEnrollmentToFrontend = (enrollment, courseDetails, progressValue) => {
  // Robust ID extraction
  const enrollmentId = enrollment.EnrollmentID || enrollment.enrollment_id || enrollment.id;
  const courseId = enrollment.CourseID || enrollment.course_id || enrollment.courseId || enrollment.id;

  return {
    id: enrollmentId, 
    courseId: courseId, 
    
    // Hydrate Missing Data from Course Details
    title: courseDetails?.title || "Unknown Course",
    instructor: "MUDemy Instructor", 
    image: courseDetails?.image || "https://lh3.googleusercontent.com/aida-public/AB6AXuCJvR2L-V_bsDptQ-El7f4IB80ZyZ-SV3qbu6Nom0Ws7UhdYu9Lna_El1veVNYZYuBt9J3loaGHH7UBMhdCeV24v7PyMrdy4vnmTV2zmdYh-93MfjFTAunJirtgwPAdtWkCH8szlG-3IuD_TYV-DExhjkKFP0Dl910ZytvCh7TzUJQL_HjnPfo0tarGFC4Ex47S1WPShmMDOOYJZSgwta3MBsPFw8xwP9rDY4fxAf_j_PucY9UX12yVfQtQaUMkhgKqKSmfYLMVZBc",
    description: courseDetails?.description || "No description available",
    
    // Status & Progress
    status: enrollment.Status || enrollment.status || "Active", 
    progress: progressValue || 0, 
    
    lessons: [] 
  };
};

export const studentService = {
  /**
   * Fetch current user profile.
   */
  getStudentProfile: async () => {
    const response = await axiosClient.get('/api/users/me');
    return response.user || response; 
  },

  /**
   * Call the SQL Function endpoint: GET /api/courses/{id}/progress
   */
  getCourseProgress: async (courseId) => {
    if (!courseId) return 0;
    try {
      const response = await axiosClient.get(`/api/courses/${courseId}/progress`);
      return response.progress || 0;
    } catch (error) {
      console.warn(`Failed to fetch progress for course ${courseId}`, error);
      return 0;
    }
  },

  /**
   * Fetch enrolled courses and hydrate with Details + Progress.
   */
  getEnrolledCourses: async () => {
    try {
      // Step A: Get raw enrollments
      const enrollmentResponse = await axiosClient.get('/api/enrollments/me');
      const rawEnrollments = enrollmentResponse.enrollments || enrollmentResponse || [];
      
      console.log("Raw Enrollments from Backend:", rawEnrollments);

      // Step B: Process in parallel
      const detailedEnrollments = await Promise.all(
        rawEnrollments.map(async (enrollment) => {
          // Robust ID Extraction
          const courseId = enrollment.CourseID || enrollment.course_id || enrollment.courseId || enrollment.id;

          if (!courseId) {
            console.error("Critical: Enrollment record missing CourseID", enrollment);
            return null; 
          }

          try {
            // Fetch Details & Progress simultaneously
            const [courseDetails, progressValue] = await Promise.all([
              courseService.getCourseById(courseId),
              studentService.getCourseProgress(courseId)
            ]);
            
            return mapEnrollmentToFrontend(enrollment, courseDetails, progressValue);
          } catch (err) {
            console.warn(`Failed to hydrate course ${courseId}`, err);
            return mapEnrollmentToFrontend(enrollment, {}, 0); 
          }
        })
      );

      // Filter out any nulls
      return detailedEnrollments.filter(item => item !== null);
    } catch (error) {
      console.error("Failed to fetch enrollments chain:", error);
      return []; 
    }
  }
};