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
    group: "Auth",
    name: "Login",
    method: "POST",
    path: "/api/auth/login",
    input: {
      "username": "Đạt Phạm",
      "password": "P@ssw0rd123!",
      "role": "tutor",
    },
    output: {
      username: "Đạt Phạm",
      role: "tutor",
      status: "Login successful",
    },
  },
  {
    group: "Auth",
    name: "Logout",
    method: "POST",
    path: "/api/auth/logout",
    input: {},
    output: { status: "Logout successful" },
  },
  {
    group: "Auth",
    name: "Get Roles",
    method: "GET",
    path: "/api/auth/roles",
    input: {},
    output: [
      { id: "TUTOR", label: "tutor", description: "Dành cho giảng viên" },
      { id: "TUTEE", label: "tutee", description: "Dành cho học viên" },
      { id: "ADMIN", label: "admin", description: "Quản trị hệ thống" },
    ],
  },

  // =====================
  // USER
  // =====================
  {
    group: "User",
    name: "Get Current User",
    method: "GET",
    path: "/api/users/me",
    input: {},
    output: {
      status: "success",
      user: {
        UserID: "USR00001",
        User_name: "Đạt Phạm",
        Email: "dat.pham@mudemy.edu.vn",
        Full_name: "Phạm Lê Tiến Đạt",
        City: "TP. Hồ Chí Minh",
        Country: "Việt Nam",
        Phone: "0903123456",
        Date_of_birth: "1986-06-15",
        Last_login: "2025-11-23 19:30:00",
        IFlag: true,
        Bio_text: "Giảng viên MUdemy",
        Year_of_experience: 15,
        SFlag: false,
        Total_enrollments: 0,
      },
    },
  },
  {
    group: "User",
    name: "Create User",
    method: "POST",
    path: "/api/users",
    input: {
      "User_name": "vinhpro",
      "Email": "vinhnguyen@gmail.com",
      "Password": "P@ssw0rd123!",
      "Full_name": "Nguyễn Hữu Vinh",
      "City": "TP. Hồ Chí Minh",
      "Country": "Việt Nam",
      "Phone": "0938666777",
      "Date_of_birth": "2000-10-10",
      "IFlag": false,
      "SFlag": true,
      "Bio_text": "SV UEH"
    },
    output: {
      status: "created",
      user_id: "USR00011",
    },
  },
  {
    group: "User",
    name: "List Users",
    method: "GET",
    path: "/api/users",
    input: {},
    output: {
      status: "success",
      count: 13,
      users: [
        {
          UserID: "USR00001",
          User_name: "Đạt Phạm",
          Email: "dat.pham@mudemy.edu.vn",
          Full_name: "Phạm Lê Tiến Đạt",
          City: "TP. Hồ Chí Minh",
          Country: "Việt Nam",
          Phone: "0903123456",
          Date_of_birth: "1986-06-15",
          Last_login: "2025-11-23 19:30:00",
          IFlag: true,
          Bio_text: "Giảng viên MUdemy",
          Year_of_experience: 15,
          SFlag: false,
          Total_enrollments: 0,
        },
        // ...more users
      ],
    },
  },
  {
    group: "User",
    name: "Get User by ID",
    method: "GET",
    path: "/api/users/id/USR00001",
    input: {},
    output: {
      status: "success",
      user: {
        UserID: "USR00001",
        User_name: "Đạt Phạm",
        Email: "dat.pham@mudemy.edu.vn",
        Full_name: "Phạm Lê Tiến Đạt",
        City: "TP. Hồ Chí Minh",
        Country: "Việt Nam",
        Phone: "0903123456",
        Date_of_birth: "1986-06-15",
        Last_login: "2025-11-23 19:30:00",
        IFlag: true,
        Bio_text: "Giảng viên MUdemy",
        Year_of_experience: 15,
        SFlag: false,
        Total_enrollments: 0,
      },
    },
  },
  {
    group: "User",
    name: "Update User",
    method: "PUT",
    path: "/api/users/USR00001",
    input: {
      "Full_name": "Phạm Lê Tiến Đạt",
      "Bio_text": "Updated bio",
      "Phone": "0903999999"
    },
    output: {
      status: "updated",
      user_id: "USR00001"
    }
  },
  {
    group: "User",
    name: "Delete User",
    method: "DELETE",
    path: "/api/users/USR00011",
    input: {},
    output: {
      status: "deleted",
      user_id: "USR00011"
    }
  },
  {
    group: "User",
    name: "Search Users",
    method: "GET",
    path: "/api/users/search?name=Đạt",
    input: {},
    output: {
      status: "success",
      count: 1,
      users: [
        {
          UserID: "USR00001",
          User_name: "Đạt Phạm",
          Email: "dat.pham@mudemy.edu.vn",
          Full_name: "Phạm Lê Tiến Đạt",
          City: "TP. Hồ Chí Minh",
          Country: "Việt Nam"
        }
      ]
    }
  },
  {
    group: "User",
    name: "Add Interest",
    method: "POST",
    path: "/api/users/USR00001/interests",
    input: {
      "interest": "Python"
    },
    output: {
      status: "created",
      user_id: "USR00001",
      interest: "Python"
    }
  },
  {
    group: "User",
    name: "Get User Interests",
    method: "GET",
    path: "/api/users/USR00001/interests",
    input: {},
    output: {
      status: "success",
      count: 2,
      interests: [
        { UserID: "USR00001", Interest: "Python" },
        { UserID: "USR00001", Interest: "Web Development" }
      ]
    }
  },
  {
    group: "User",
    name: "Add Qualification",
    method: "POST",
    path: "/api/users/USR00001/qualifications",
    input: {
      "qualification": "Bachelor in Computer Science"
    },
    output: {
      status: "created",
      user_id: "USR00001"
    }
  },
  {
    group: "User",
    name: "List Instructors",
    method: "GET",
    path: "/api/users/instructors",
    input: {},
    output: {
      status: "success",
      count: 5,
      instructors: [
        {
          UserID: "USR00001",
          User_name: "Đạt Phạm",
          Email: "dat.pham@mudemy.edu.vn",
          Full_name: "Phạm Lê Tiến Đạt",
          City: "TP. Hồ Chí Minh",
          Country: "Việt Nam",
          Phone: "0903123456",
          Bio_text: "Giảng viên MUdemy",
          Year_of_experience: 15
        }
      ]
    }
  },
  {
    group: "User",
    name: "List Students",
    method: "GET",
    path: "/api/users/students",
    input: {},
    output: {
      status: "success",
      count: 8,
      students: [
        {
          UserID: "USR00006",
          User_name: "Tuấn BK",
          Email: "anhtuan@hcmut.edu.vn",
          Full_name: "Nguyễn Anh Tuấn",
          City: "TP. Hồ Chí Minh",
          Country: "Việt Nam",
          Total_enrollments: 1
        }
      ]
    }
  },
  // ... (other user endpoints: create take, mark lesson finished, etc.)

  // =====================
  // COURSE
  // =====================
  {
    group: "Course",
    name: "List Courses",
    method: "GET",
    path: "/api/courses",
    input: {},
    output: {
      status: "success",
      count: 6,
      courses: [
        {
          CourseID: "CRS00001",
          Title: "Python cho DeepLearning",
          Difficulty: "Intermediate",
          Language: "Tiếng Việt",
          Description: "Học cách xây dựng, huấn luyện và tối ưu các mô hình mạng nơ-ron phức tạp (CNN, RNN, Transformers) sử dụng TensorFlow và PyTorch."
        },
        // ...more courses
      ],
    },
  },
  {
    group: "Course",
    name: "Get Course by ID",
    method: "GET",
    path: "/api/courses/id/CRS00001",
    input: {},
    output: {
      status: "success",
      course: {
        CourseID: "CRS00001",
        Title: "Python cho DeepLearning",
        Difficulty: "Intermediate",
        Language: "Tiếng Việt",
        Description: "Học cách xây dựng, huấn luyện và tối ưu các mô hình mạng nơ-ron phức tạp (CNN, RNN, Transformers) sử dụng TensorFlow và PyTorch.",
        Categories: ["Python", "Deep Learning"],
        Prerequisites: ["CRS00005"],
      },
    },
  },
  {
    group: "Course",
    name: "Create Course",
    method: "POST",
    path: "/api/courses",
    input: {
      "Difficulty": "Intermediate",
      "Language": "Tiếng Việt",
      "Title": "Advanced Python Programming",
      "Description": "Learn advanced Python concepts and best practices"
    },
    output: {
      status: "created",
      course_id: "CRS00007",
      title: "Advanced Python Programming"
    }
  },
  {
    group: "Course",
    name: "Update Course",
    method: "PUT",
    path: "/api/courses/CRS00001",
    input: {
      "Title": "Python for Deep Learning - Updated",
      "Description": "Updated course description"
    },
    output: {
      status: "updated",
      course_id: "CRS00001"
    }
  },
  {
    group: "Course",
    name: "Delete Course",
    method: "DELETE",
    path: "/api/courses/CRS00007",
    input: {},
    output: {
      status: "deleted",
      course_id: "CRS00007"
    }
  },
  {
    group: "Course",
    name: "Search Courses",
    method: "GET",
    path: "/api/courses/search?title=Python",
    input: {},
    output: {
      status: "success",
      count: 2,
      courses: [
        {
          CourseID: "CRS00001",
          Title: "Python cho DeepLearning",
          Difficulty: "Intermediate",
          Language: "Tiếng Việt",
          Description: "..."
        }
      ]
    }
  },
  {
    group: "Course",
    name: "Add Category to Course",
    method: "POST",
    path: "/api/courses/CRS00001/categories",
    input: {
      "category": "Machine Learning"
    },
    output: {
      status: "added",
      category: "Machine Learning"
    }
  },
  {
    group: "Course",
    name: "Get Course Categories",
    method: "GET",
    path: "/api/courses/CRS00001/categories",
    input: {},
    output: {
      status: "success",
      count: 2,
      categories: ["Python", "Deep Learning"]
    }
  },
  {
    group: "Course",
    name: "Add Prerequisite",
    method: "POST",
    path: "/api/courses/CRS00001/prerequisites",
    input: {
      "required_course_id": "CRS00005"
    },
    output: {
      status: "added",
      prerequisite: "CRS00005"
    }
  },
  {
    group: "Course",
    name: "Create Module",
    method: "POST",
    path: "/api/modules",
    input: {
      "Title": "Introduction to Deep Learning",
      "CourseID": "CRS00001"
    },
    output: {
      status: "created",
      module_id: "MOD001"
    }
  },
  {
    group: "Course",
    name: "Get Course Modules",
    method: "GET",
    path: "/api/courses/CRS00001/modules",
    input: {},
    output: {
      status: "success",
      count: 1,
      modules: [
        {
          ModuleID: "MOD001",
          Title: "Introduction to Deep Learning",
          CourseID: "CRS00001"
        }
      ]
    }
  },
  {
    group: "Course",
    name: "Create Content",
    method: "POST",
    path: "/api/content",
    input: {
      "Title": "Lesson 1: Neural Networks Basics",
      "Slides": "https://example.com/slides/lesson1.pdf",
      "ModuleID": "MOD001"
    },
    output: {
      status: "created",
      content_id: "CON001"
    }
  },
  {
    group: "Course",
    name: "Add Text to Content",
    method: "POST",
    path: "/api/content/CON001/text",
    input: {
      "TextID": "TXT001",
      "Text": "Neural networks are computing systems inspired by biological networks..."
    },
    output: {
      status: "created",
      text_id: "TXT001"
    }
  },
  {
    group: "Course",
    name: "Add Video to Content",
    method: "POST",
    path: "/api/content/CON001/video",
    input: {
      "VideoID": "VID001",
      "Video": "https://example.com/videos/lesson1.mp4"
    },
    output: {
      status: "created",
      video_id: "VID001"
    }
  },
  // ... (other course endpoints: add image, update content, delete content, etc.)

  // =====================
  // ENROLLMENT
  // =====================
  {
    group: "Enrollment",
    name: "Enroll in Course",
    method: "POST",
    path: "/api/enroll",
    input: {
      "CourseID": "CRS00001",
      "PaymentID": "PAY001"
    },
    note: "StudentID is set from session",
    output: {
      status: "created",
      enrollment_id: "ENR001",
    },
  },
  {
    group: "Enrollment",
    name: "Get My Enrollments",
    method: "GET",
    path: "/api/enrollments/me",
    input: {},
    output: {
      status: "success",
      count: 2,
      enrollments: [
        {
          EnrollmentID: "ENR001",
          CourseID: "CRS00001",
          PaymentID: "PAY001",
          StudentID: "USR00013",
          Status: "Active",
          Enroll_date: "2025-11-22 07:04:07",
        },
        // ...more enrollments
      ],
    },
  },
  {
    group: "Enrollment",
    name: "Get Enrollment by ID",
    method: "GET",
    path: "/api/enrollments/ENR001",
    input: {},
    output: {
      status: "success",
      enrollment: {
        EnrollmentID: "ENR001",
        CourseID: "CRS00001",
        PaymentID: "PAY001",
        StudentID: "USR00013",
        Status: "Active",
        Enroll_date: "2025-11-22 07:04:07"
      }
    }
  },
  {
    group: "Enrollment",
    name: "Get Enrollments by Course",
    method: "GET",
    path: "/api/courses/CRS00001/enrollments",
    input: {},
    output: {
      status: "success",
      count: 5,
      enrollments: [
        {
          EnrollmentID: "ENR001",
          CourseID: "CRS00001",
          PaymentID: "PAY001",
          StudentID: "USR00013",
          Status: "Active",
          Enroll_date: "2025-11-22 07:04:07"
        }
      ]
    }
  },
  {
    group: "Enrollment",
    name: "Update Enrollment Status",
    method: "PUT",
    path: "/api/enrollments/ENR001/status",
    input: {
      "status": "Completed"
    },
    output: {
      status: "updated",
      enrollment_id: "ENR001",
      new_status: "Completed"
    }
  },
  {
    group: "Enrollment",
    name: "Create Payment",
    method: "POST",
    path: "/api/payments",
    input: {
      "Amount": 299000,
      "Payment_method": "Credit Card"
    },
    output: {
      status: "created",
      payment_id: "PAY002"
    }
  },
  {
    group: "Enrollment",
    name: "Get Payment",
    method: "GET",
    path: "/api/payments/PAY001",
    input: {},
    output: {
      status: "success",
      payment: {
        PaymentID: "PAY001",
        Amount: 299000,
        Payment_date: "2025-11-21 10:30:00",
        Payment_method: "Credit Card",
        UserID: "USR00013"
      }
    }
  },
  {
    group: "Enrollment",
    name: "Create Certificate",
    method: "POST",
    path: "/api/certificates",
    input: {
      "CourseID": "CRS00001",
      "StudentID": "USR00013",
      "Certificate_number": "CERT-2025-001",
      "Expiry_date": "2026-12-03"
    },
    output: {
      status: "created",
      certificate_id: "CERT001"
    }
  },
  // ... (other enrollment endpoints: delete, update payment, etc.)

  // =====================
  // ASSESSMENT (Assignment, Quiz, Submission)
  // =====================
  {
    group: "Assessment",
    name: "List Assignments by Module",
    method: "GET",
    path: "/api/modules/MOD007/assignments",
    input: {},
    output: {
      status: "success",
      count: 1,
      assignments: [
        {
          AssID: "ASS001",
          Deadline: "2025-12-30 23:59:00",
          Description: "React + Node",
          Title: "Xây app quản lý quán cà phê",
          ModuleID: "MOD007",
        },
      ],
    },
  },
  {
    group: "Assessment",
    name: "List Quizzes by Module",
    method: "GET",
    path: "/api/modules/MOD001/quizzes",
    input: {},
    output: {
      status: "success",
      count: 1,
      quizzes: [
        {
          QuizID: "QUI001",
          Time_limit: 1800,
          Num_attempt: 2,
          Deadline: "2025-12-25 23:59:00",
          Title: "Quiz Deep Learning Cơ bản",
          ModuleID: "MOD001",
        },
      ],
    },
  },
  {
    group: "Assessment",
    name: "Create Assignment",
    method: "POST",
    path: "/api/assignments",
    input: {
      "Title": "Xây app quản lý quán cà phê",
      "Description": "React + Node",
      "Deadline": "2025-12-30T23:59:00",
      "ModuleID": "MOD007"
    },
    output: {
      status: "created",
      assignment_id: "ASS002"
    }
  },
  {
    group: "Assessment",
    name: "Submit Assignment",
    method: "POST",
    path: "/api/assignments/ASS001/submit",
    input: {
      "Sub_content": "https://github.com/student/cafe-app"
    },
    output: {
      status: "submitted",
      submission_id: "SUB001"
    }
  },
  {
    group: "Assessment",
    name: "Grade Assignment",
    method: "PUT",
    path: "/api/submissions/assignment/SUB001/grade",
    input: {
      "grade": 9.5
    },
    output: {
      status: "graded",
      submission_id: "SUB001",
      grade: 9.5
    }
  },
  {
    group: "Assessment",
    name: "Create Quiz",
    method: "POST",
    path: "/api/quizzes",
    input: {
      "Title": "Quiz Deep Learning Cơ bản",
      "Time_limit": 1800,
      "Num_attempt": 2,
      "Deadline": "2025-12-25T23:59:00",
      "ModuleID": "MOD001"
    },
    output: {
      status: "created",
      quiz_id: "QUI002"
    }
  },
  {
    group: "Assessment",
    name: "Add Question to Quiz",
    method: "POST",
    path: "/api/quizzes/QUI001/questions",
    input: {
      "Content": "What is a convolutional neural network?",
      "Correct_answer": "A neural network designed for image processing",
      "QuizID": "QUI001"
    },
    output: {
      status: "created",
      question_id: "Q001"
    }
  },
  {
    group: "Assessment",
    name: "Add Answer Option",
    method: "POST",
    path: "/api/questions/Q001/answers",
    input: {
      "Answer": "A neural network designed for image processing"
    },
    output: {
      status: "created",
      answer_id: "ANS001"
    }
  },
  {
    group: "Assessment",
    name: "Submit Quiz",
    method: "POST",
    path: "/api/quizzes/QUI001/submit",
    input: {
      "Sub_content": "[{\"QuestionID\":\"Q001\",\"AnswerID\":\"ANS001\"}]"
    },
    output: {
      status: "submitted",
      submission_id: "QSub001"
    }
  },
  {
    group: "Assessment",
    name: "Get Quiz Stats",
    method: "GET",
    path: "/api/modules/MOD001/quiz-stats?min_submissions=1",
    input: {},
    output: {
      status: "success",
      stats: [
        {
          QuizID: "QUI001",
          QuizTitle: "Quiz Deep Learning Cơ bản",
          AverageGrade: 8.2,
          HighestGrade: 10,
          LowestGrade: 6.5,
          TotalSubmissions: 15
        }
      ]
    }
  },
  // ... (other assessment endpoints: update quiz, delete question, etc.)

  // =====================
  // RESOURCE
  // =====================
  {
    group: "Resource",
    name: "List Resources",
    method: "GET",
    path: "/api/resources",
    input: {},
    output: {
      status: "success",
      count: 4,
      resources: [
        {
          ResourceID: "RES002",
          File_Name: "React Hooks Cheatsheet",
          File_link: "/res/[RES002]react-hooks-cheat.pdf",
          External_link: null,
        },
        // ...more resources
      ],
    },
  },
  {
    group: "Resource",
    name: "Create Resource",
    method: "POST",
    path: "/api/resources",
    input: {
      "File_Name": "Python Cheatsheet",
      "File_link": "/res/[RES003]python-cheat.pdf",
      "External_link": "https://example.com/resources/python"
    },
    output: {
      status: "created",
      resource_id: "RES003"
    }
  },
  {
    group: "Resource",
    name: "Update Resource",
    method: "PUT",
    path: "/api/resources/RES002",
    input: {
      "File_Name": "Advanced React Hooks",
      "External_link": "https://example.com/react-advanced"
    },
    output: {
      status: "updated",
      resource_id: "RES002"
    }
  },
  {
    group: "Resource",
    name: "Provide Resource to Lesson",
    method: "POST",
    path: "/api/provide",
    input: {
      "ResourceID": "RES002",
      "LessonID": "LES001"
    },
    output: {
      status: "provided",
      ResourceID: "RES002",
      LessonID: "LES001"
    }
  },
  {
    group: "Resource",
    name: "Get Resources by Lesson",
    method: "GET",
    path: "/api/lessons/LES001/resources",
    input: {},
    output: {
      status: "success",
      count: 2,
      resources: [
        {
          ResourceID: "RES002",
          LessonID: "LES001"
        }
      ]
    }
  },
  {
    group: "Resource",
    name: "Bulk Provide Resources",
    method: "POST",
    path: "/api/provide/bulk",
    input: {
      "ResourceIDs": ["RES001", "RES002", "RES003"],
      "LessonID": "LES002"
    },
    output: {
      status: "success",
      provided_count: 3
    }
  },
  {
    group: "Resource",
    name: "Delete Resource",
    method: "DELETE",
    path: "/api/resources/RES003",
    input: {},
    output: {
      status: "deleted",
      resource_id: "RES003"
    }
  },
  // ... (other resource endpoints: search, resource count, etc.)

  // =====================
  // UTILS
  // =====================
  {
    group: "Utils",
    name: "Health Check",
    method: "GET",
    path: "/api/health",
    input: {},
    output: { status: "ok" },
  },
  {
    group: "Utils",
    name: "Root",
    method: "GET",
    path: "/api/",
    input: {},
    output: { message: "Backend is up and running. Navigate to ./docs for Swagger contents" },
  },
];

module.exports = API_DOCS;
