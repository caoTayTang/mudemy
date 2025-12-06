import axiosClient from '../api/axiosClient';

/**
 * Helper to map backend snake_case to frontend camelCase
 * This ensures the view components (HomePage, CourseDetailPage) don't break.
 */
const mapCourseToFrontend = (apiCourse) => ({
  id: apiCourse.CourseID,
  title: apiCourse.Title,
  description: apiCourse.Description || "No description available",
  // author: apiCourse.instructor_name || "MUDemy Instructor", 
  image: apiCourse.image_url || "https://lh3.googleusercontent.com/aida-public/AB6AXuAwZhaZNZcPvZguKgpvSplwjbU6avMNIxKMhfAlEXpcM72Ph19ef-qCxHCBh9fD9zBF99kAEbApneZWBEkJdv8FW0HxSjTkkHVG8obgwT9nTC-n3tVyY-XSJlT6CFldc9EXu3rM1_TGR19HI1T0xoXFnZXYBpk0k_rhUTK7MBRIPrHp1XwrzXq9L5T2D3YTSf1Ob-W6M-711iPtV8bv7YfTv6qRfikelW5LtON9h52zeLGqPsvxCbOZwZT0lcObFnXsYaMYUQSjxYc",
  level: apiCourse.Difficulty,
  language: apiCourse.Language || "Tiếng Việt",
  // category: apiCourse.category_name || "General",
  // price: apiCourse.price || 0,
  // originalPrice: apiCourse.original_price || 0,
  // Badges logic (Frontend specific)
  badgeColor: "bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200",
  // Detailed fields (often only present in getById)
  // curriculum: apiCourse.modules ? apiCourse.modules.map(mod => ({
  //   title: mod.title,
  //   lessons: mod.content ? mod.content.map(c => c.title) : [] 
  // })) : [],
  // whatYouWillLearn: apiCourse.objectives || ["Master the fundamentals", "Build real projects"],
  // rating: apiCourse.rating || 4.5,
  // ratingCount: apiCourse.rating_count || 0,
  // studentCount: apiCourse.student_count || 0,
  // lastUpdated: apiCourse.updated_at ? new Date(apiCourse.updated_at).toLocaleDateString() : "Recently"
});

export const courseService = {
  /**
   * Fetch all courses for the homepage.
   * Endpoint: GET /api/courses
   */
  getFeaturedCourses: async () => {
    try {
      const response = await axiosClient.get('/api/courses');
      // If response is an array, map it. If it's paginated { data: [] }, access .data
      const courses = response.courses || [];
      console.info("Fetched Courses:", courses);
      return courses.map(mapCourseToFrontend);
    } catch (error) {
      console.error("Failed to fetch featured courses:", error);
      return []; // Return empty array on error to prevent UI crash
    }
  },

  /**
   * Fetch a single course by ID.
   * Endpoint: GET /api/courses/id/{course_id}
   */
  getCourseById: async (id) => {
    try {
      const response = await axiosClient.get(`/api/courses/id/${id}`);
      return mapCourseToFrontend(response.course);
    } catch (error) {
      console.error(`Failed to fetch course ${id}:`, error);
      throw error;
    }
  },

  /**
   * Fetch cart items (Simulated or Real if you have a Cart endpoint)
   * Note: Your API list didn't have a specific 'Cart' endpoint, so we might need
   * to use local storage or a generic 'enrollments' check here.
   * For now, keeping it mock or simple to avoid breaking Checkout.
   */
  getCartItems: async () => {
    // If you implement a cart endpoint later: await axiosClient.get('/api/cart');
    // For now, return empty or mock to keep checkout page working visually
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