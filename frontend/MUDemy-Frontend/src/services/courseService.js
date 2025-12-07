import axiosClient from '../api/axiosClient';

/**
 * Maps Backend Data (PascalCase) -> Frontend UI (camelCase)
 * This ensures your React components get the data they expect.
 */
const mapCourseToFrontend = (apiCourse) => ({
  // --- DIRECT MAPPING FROM API DOCS ---
  id: apiCourse.CourseID,           // API: CourseID
  title: apiCourse.Title,           // API: Title
  description: apiCourse.Description || "No description provided.", // API: Description
  level: apiCourse.Difficulty,      // API: Difficulty
  language: apiCourse.Language,     // API: Language
  categories: apiCourse.Categories || [], // API: Categories (Array)
  prerequisites: apiCourse.Prerequisites || [], // API: Prerequisites (Array)

  // --- UI PLACEHOLDERS (Data not in current API response) ---
  // We use static defaults so the page looks good until backend adds these fields
  author: {
    name: "MUDemy Instructor",
    image: "https://lh3.googleusercontent.com/aida-public/AB6AXuCyM5V5W1caBuueUy7B-ybcmN1I-ykhwjlBERPyo41MhwSEAdpYA-UDCuE_5Zd-lt9b-KIVIU60d2NXaN_s8AhaZNjkY5C_c6b6mwjpMeUCSkfZLJoP_a5CzSTNMMzyfkedXxStQD2cZxBf1FPaOGxT_ScETx339vlXsH6e6ZB4BAiGk96H7ow8bQvbHlJqvCPC2GaVMkgVPqa_RlQIK0nrA95sK1eyulYQzRfxLOPnqcKuiuCapA17X0SJRpT6A3nplRZ9IywTO7c",
    bio: "Experienced instructor on MUDemy platform."
  },
  image: "https://lh3.googleusercontent.com/aida-public/AB6AXuBmOLsiegX7ApjwgsQJFWzwh3JEmAWOSxOnRbGvoDmhHOOHETU1-MaiY7YHhza1K1FTTExboLq8SotjKGetXmFfKdVxtKh-55P3Qqb0r_gb-Rt0sjBISLXUZXOKT86lYTalrZZmWmpDmvTZw65cXRfaaothPq5HZCNo0o-M-vvUz8mqWKg-lvO-c9UvNrJzN1aJXzCM1zEObyWDWJckwHMODBhQvAT7yNf4HFgtS2tMUARs3JwKyHaBTX1wW-h7ZojoCccC8LlwX2s",
  price: 19.99, // Default price
  originalPrice: 99.99,
  discount: "80% off",
  rating: 4.8,
  ratingCount: 120,
  studentCount: 500,
  lastUpdated: "Recently",
  
  // Curriculum Structure (Placeholder until /modules endpoint is integrated here)
  curriculum: [
    { title: "Introduction", lessons: ["Welcome to the course", "Setup Environment"] },
    { title: "Core Concepts", lessons: ["Basic Syntax", "Control Flow", "Functions"] }
  ],
  whatYouWillLearn: [
    "Master the core concepts",
    "Build real-world applications",
    "Understand best practices"
  ]
});

export const courseService = {
  /**
   * Fetch all courses for the catalog.
   * Endpoint: GET /api/courses
   */
  getFeaturedCourses: async () => {
    try {
      const response = await axiosClient.get('/api/courses');
      // API Output: { status: "success", count: 6, courses: [...] }
      const courses = response.courses || [];
      return courses.map(mapCourseToFrontend);
    } catch (error) {
      console.error("Failed to fetch featured courses:", error);
      return [];
    }
  },

  /**
   * Fetch specific course details.
   * Endpoint: GET /api/courses/id/{id}
   */
  getCourseById: async (id) => {
    try {
      const response = await axiosClient.get(`/api/courses/id/${id}`);
      // API Output: { status: "success", course: { CourseID, Title, ... } }
      // We must access response.course, NOT response directly
      if (response.course) {
        console.info("Fetched Course Data:", response.course);
        return mapCourseToFrontend(response.course);
      }
      throw new Error("Course object missing in response");
    } catch (error) {
      console.error(`Failed to fetch course ${id}:`, error);
      throw error;
    }
  },

  /**
   * Check prerequisites for a course.
   * Endpoint: GET /api/courses/{course_id}/prerequisites/f
   */
  checkPrerequisites: async (courseId) => {
    try {
      const response = await axiosClient.get(`/api/courses/${courseId}/prerequisites/f`);
      return response.missing_prereqs || [];
    } catch (error) {
      console.error(`Failed to check prerequisites for ${courseId}:`, error);
      return [];
    }
  }
};