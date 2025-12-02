/**
 * Mudemy API Documentation
 *
 * This file documents the main API routes grouped by feature.
 * For each route: group, name, input example, output example.
 * Sample data is based on the database schema and sample SQL data.
 */

const API_DOCS = [
  // =====================
  // AUTH & LOGIN
  // =====================
  {
    group: 'Auth',
    name: 'Login',
    method: 'POST',
    path: '/api/auth/login',
    input: {
      username: 'dat.pham@mudemy.edu.vn',
      password: 'P@ssw0rd123!',
      role: 'tutor',
    },
    output: {
      username: 'dat.pham@mudemy.edu.vn',
      role: 'tutor',
      status: 'Login successful',
    },
  },
  {
    group: 'Auth',
    name: 'Logout',
    method: 'POST',
    path: '/api/auth/logout',
    input: {},
    output: { status: 'Logout successful' },
  },
  {
    group: 'Auth',
    name: 'Get Roles',
    method: 'GET',
    path: '/api/auth/roles',
    input: {},
    output: [
      { id: 'TUTOR', label: 'tutor', description: 'Dành cho giảng viên' },
      { id: 'TUTEE', label: 'tutee', description: 'Dành cho học viên' },
      { id: 'ADMIN', label: 'admin', description: 'Quản trị hệ thống' },
    ],
  },

  // =====================
  // USER
  // =====================
  {
    group: 'User',
    name: 'Get Current User',
    method: 'GET',
    path: '/api/users/me',
    input: {},
    output: {
      status: 'success',
      user: {
        UserID: 'USR00001',
        User_name: 'Đạt Phạm',
        Email: 'dat.pham@mudemy.edu.vn',
        Full_name: 'Phạm Lê Tiến Đạt',
        City: 'TP. Hồ Chí Minh',
        Country: 'Việt Nam',
        Phone: '0903123456',
        Date_of_birth: '1986-06-15',
        Last_login: '2025-11-23 19:30:00',
        IFlag: true,
        Bio_text: 'Giảng viên MUdemy',
        Year_of_experience: 15,
        SFlag: false,
        Total_enrollments: 0,
      },
    },
  },
  {
    group: 'User',
    name: 'Create User',
    method: 'POST',
    path: '/api/users',
    input: {
      User_name: 'vinhpro',
      Email: 'vinhnguyen@gmail.com',
      Password: 'P@ssw0rd123!',
      Full_name: 'Nguyễn Hữu Vinh',
      City: 'TP. Hồ Chí Minh',
      Country: 'Việt Nam',
      Phone: '0938666777',
      Date_of_birth: '2000-10-10',
      IFlag: false,
      SFlag: true,
      Bio_text: 'SV UEH',
    },
    output: {
      status: 'created',
      user_id: 'USR00011',
    },
  },
  {
    group: 'User',
    name: 'List Users',
    method: 'GET',
    path: '/api/users',
    input: {},
    output: {
      status: 'success',
      count: 13,
      users: [
        {
          UserID: 'USR00001',
          User_name: 'Đạt Phạm',
          Email: 'dat.pham@mudemy.edu.vn',
          Full_name: 'Phạm Lê Tiến Đạt',
          City: 'TP. Hồ Chí Minh',
          Country: 'Việt Nam',
          Phone: '0903123456',
          Date_of_birth: '1986-06-15',
          Last_login: '2025-11-23 19:30:00',
          IFlag: true,
          Bio_text: 'Giảng viên MUdemy',
          Year_of_experience: 15,
          SFlag: false,
          Total_enrollments: 0,
        },
        // ...more users
      ],
    },
  },
  {
    group: 'User',
    name: 'Get User by ID',
    method: 'GET',
    path: '/api/users/id/USR00001',
    input: {},
    output: {
      status: 'success',
      user: {
        UserID: 'USR00001',
        User_name: 'Đạt Phạm',
        Email: 'dat.pham@mudemy.edu.vn',
        Full_name: 'Phạm Lê Tiến Đạt',
        City: 'TP. Hồ Chí Minh',
        Country: 'Việt Nam',
        Phone: '0903123456',
        Date_of_birth: '1986-06-15',
        Last_login: '2025-11-23 19:30:00',
        IFlag: true,
        Bio_text: 'Giảng viên MUdemy',
        Year_of_experience: 15,
        SFlag: false,
        Total_enrollments: 0,
      },
    },
  },
  // ... (other user endpoints: update, delete, search, interests, qualifications, etc.)

  // =====================
  // COURSE
  // =====================
  {
    group: 'Course',
    name: 'List Courses',
    method: 'GET',
    path: '/api/courses',
    input: {},
    output: {
      status: 'success',
      count: 6,
      courses: [
        {
          CourseID: 'CRS00001',
          Title: 'Python cho DeepLearning',
          Difficulty: 'Intermediate',
          Language: 'Tiếng Việt',
          Description: 'Học cách xây dựng, huấn luyện và tối ưu các mô hình mạng nơ-ron phức tạp (CNN, RNN, Transformers) sử dụng TensorFlow và PyTorch.'
        },
        // ...more courses
      ],
    },
  },
  {
    group: 'Course',
    name: 'Get Course by ID',
    method: 'GET',
    path: '/api/courses/id/CRS00001',
    input: {},
    output: {
      status: 'success',
      course: {
        CourseID: 'CRS00001',
        Title: 'Python cho DeepLearning',
        Difficulty: 'Intermediate',
        Language: 'Tiếng Việt',
        Description: 'Học cách xây dựng, huấn luyện và tối ưu các mô hình mạng nơ-ron phức tạp (CNN, RNN, Transformers) sử dụng TensorFlow và PyTorch.',
        Categories: ['Python', 'Deep Learning'],
        Prerequisites: ['CRS00005'],
      },
    },
  },
  // ... (other course endpoints: create, update, delete, search, modules, content, etc.)

  // =====================
  // ENROLLMENT
  // =====================
  {
    group: 'Enrollment',
    name: 'Enroll in Course',
    method: 'POST',
    path: '/api/enroll',
    input: {
      CourseID: 'CRS00001',
      PaymentID: 'PAY001',
      // StudentID is set from session
    },
    output: {
      status: 'created',
      enrollment_id: 'ENR001',
    },
  },
  {
    group: 'Enrollment',
    name: 'Get My Enrollments',
    method: 'GET',
    path: '/api/enrollments/me',
    input: {},
    output: {
      status: 'success',
      count: 2,
      enrollments: [
        {
          EnrollmentID: 'ENR001',
          CourseID: 'CRS00001',
          PaymentID: 'PAY001',
          StudentID: 'USR00013',
          Status: 'Active',
          Enroll_date: '2025-11-22 07:04:07',
        },
        // ...more enrollments
      ],
    },
  },
  // ... (other enrollment endpoints: delete, update, stats, etc.)

  // =====================
  // ASSESSMENT (Assignment, Quiz, Submission)
  // =====================
  {
    group: 'Assessment',
    name: 'List Assignments by Module',
    method: 'GET',
    path: '/api/modules/MOD007/assignments',
    input: {},
    output: {
      status: 'success',
      count: 1,
      assignments: [
        {
          AssID: 'ASS001',
          Deadline: '2025-12-30 23:59:00',
          Description: 'React + Node',
          Title: 'Xây app quản lý quán cà phê',
          ModuleID: 'MOD007',
        },
      ],
    },
  },
  {
    group: 'Assessment',
    name: 'List Quizzes by Module',
    method: 'GET',
    path: '/api/modules/MOD001/quizzes',
    input: {},
    output: {
      status: 'success',
      count: 1,
      quizzes: [
        {
          QuizID: 'QUI001',
          Time_limit: 1800,
          Num_attempt: 2,
          Deadline: '2025-12-25 23:59:00',
          Title: 'Quiz Deep Learning Cơ bản',
          ModuleID: 'MOD001',
        },
      ],
    },
  },
  // ... (other assessment endpoints: create, submit, grade, etc.)

  // =====================
  // RESOURCE
  // =====================
  {
    group: 'Resource',
    name: 'List Resources',
    method: 'GET',
    path: '/api/resources',
    input: {},
    output: {
      status: 'success',
      count: 4,
      resources: [
        {
          ResourceID: 'RES002',
          File_Name: 'React Hooks Cheatsheet',
          File_link: '/res/[RES002]react-hooks-cheat.pdf',
          External_link: null,
        },
        // ...more resources
      ],
    },
  },
  // ... (other resource endpoints)

  // =====================
  // UTILS
  // =====================
  {
    group: 'Utils',
    name: 'Health Check',
    method: 'GET',
    path: '/api/health',
    input: {},
    output: { status: 'ok' },
  },
  {
    group: 'Utils',
    name: 'Root',
    method: 'GET',
    path: '/api/',
    input: {},
    output: { message: 'Backend is up and running. Navigate to ./docs for Swagger contents' },
  },
];

module.exports = API_DOCS;
