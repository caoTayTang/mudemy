import axiosClient from '../api/axiosClient';

const mapCourseToFrontend = (apiCourse) => ({
  // Strictly mapping keys from your API_DOCS
  id: apiCourse.CourseID, // Key: CourseID
  title: apiCourse.Title, // Key: Title
  description: apiCourse.Description || "No description available", // Key: Description
  level: apiCourse.Difficulty, // Key: Difficulty
  // Handle Categories: API returns array of strings ["Python", "Deep Learning"] or undefined
  category: Array.isArray(apiCourse.Categories) ? apiCourse.Categories[0] : (apiCourse.Categories || "General"), 
  
  // Fields NOT in your API (using static placeholders as requested)
  author: "MUDemy Instructor", 
  image: "https://lh3.googleusercontent.com/aida-public/AB6AXuAwZhaZNZcPvZguKgpvSplwjbU6avMNIxKMhfAlEXpcM72Ph19ef-qCxHCBh9fD9zBF99kAEbApneZWBEkJdv8FW0HxSjTkkHVG8obgwT9nTC-n3tVyY-XSJlT6CFldc9EXu3rM1_TGR19HI1T0xoXFnZXYBpk0k_rhUTK7MBRIPrHp1XwrzXq9L5T2D3YTSf1Ob-W6M-711iPtV8bv7YfTv6qRfikelW5LtON9h52zeLGqPsvxCbOZwZT0lcObFnXsYaMYUQSjxYc",
  price: 0,
  originalPrice: 0,
  badgeColor: "bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200",
  rating: 4.5,
  ratingCount: 0,
  studentCount: 0,
  lastUpdated: "Recently",

  // Curriculum logic (Assuming this structure exists or defaulting to empty)
  curriculum: apiCourse.modules ? apiCourse.modules.map(mod => ({
    title: mod.title,
    lessons: mod.content ? mod.content.map(c => c.title) : [] 
  })) : [],
});

export const courseService = {
  getFeaturedCourses: async () => {
    try {
      const response = await axiosClient.get('/api/courses');
      // API returns { status: "success", count: 6, courses: [...] }
      const courses = response.courses || [];
      console.info("Fetched Featured Courses:", courses);
      return courses.map(mapCourseToFrontend);
    } catch (error) {
      console.error("Failed to fetch featured courses:", error);
      return [];
    }
  },

  getCourseById: async (id) => {
    try {
      const response = await axiosClient.get(`/api/courses/id/${id}`);
      // API returns { status: "success", course: { ... } }
      const courseData = response.course || response;
      return mapCourseToFrontend(courseData);
    } catch (error) {
      console.error(`Failed to fetch course ${id}:`, error);
      throw error;
    }
  },

  /**
   * Check if the current user meets prerequisites for a course.
   * Endpoint: GET /api/courses/{course_id}/prerequisites/f
   */
  checkPrerequisites: async (courseId) => {
    try {
      // Returns { status: "success", count: N, missing_prereqs: [{CourseID, Title}, ...] }
      const response = await axiosClient.get(`/api/courses/${courseId}/prerequisites/f`);
      return response.missing_prereqs || [];
    } catch (error) {
      console.error(`Failed to check prerequisites for ${courseId}:`, error);
      return []; 
    }
  },

  getCartItems: async () => {
    return [
      {
        id: 101,
        title: "Real API Course Placeholder",
        author: "System",
        price: 12.99,
        originalPrice: 99.99,
        image: "https://lh3.googleusercontent.com/aida-public/AB6AXuBJapRcQBAy7p4JLzZIuU2VDLFFBtB_Wk5cNWLNdJOFTo5Vv1gT9LoxxAU7epponKE60IwstY27vNbstNMDW2JDyBxLdzRGR0wwLPCma5G9exLiPcq0NcBRufzgV--GbAGDhdqKXYt5BKJa7IGyE_RdrktfxUEuBJ69uWNoLtEr3oISMI2uARFZ6K4_o0Y7ct3ZjiVXw-LSH9V624bK5R-YypbCL4J2ACc6FCyvUj4xcuzW3OTlxKvz6TnGN2y3ATWTK1clgyNH09w"
      }
    ];
  }
};