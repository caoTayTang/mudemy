const apiSpec = {
  title: 'MUDemy API Complete Documentation',
  version: '1.0.0',
  baseURL: 'http://localhost:8000/api',
  authentication: 'Cookie-based (session_id). Set automatically on POST /login',
  roles: {
    tutor: 'Instructor - can create/manage courses, assessments, resources',
    tutee: 'Student - can enroll, submit assignments/quizzes, view content',
    admin: 'System administrator (only username: sManager can login as admin)'
  },
  notes: 'Auth uses httponly cookie "session_id" set by POST /login. All timestamps in ISO format. IDs are VARCHAR(10).',

  groups: [

    /* =====================================================
       AUTHENTICATION (routes_login.py)
       ===================================================== */
    {
      group: 'Authentication',
      basePath: '',
      description: 'Login/logout endpoints. Successful login sets httponly cookie "session_id".',
      endpoints: [
        {
          name: 'Get Available Roles',
          method: 'GET',
          path: '/roles',
          auth: false,
          description: 'List all available system roles',
          input: null,
          output: {
            type: 'array',
            items: {
              id: 'string (TUTOR|TUTEE|ADMIN)',
              label: 'string (tutor|tutee|admin)',
              description: 'string'
            }
          },
          example: {
            response: [
              { id: 'TUTOR', label: 'tutor', description: 'Dành cho giảng viên' },
              { id: 'TUTEE', label: 'tutee', description: 'Dành cho học viên' },
              { id: 'ADMIN', label: 'admin', description: 'Quản trị hệ thống' }
            ]
          }
        },
        {
          name: 'Login',
          method: 'POST',
          path: '/login',
          auth: false,
          description: 'Authenticate user and set session cookie. Password stored as plaintext in DB.',
          input: {
            body: {
              username: 'string - User_name from USER table (required)',
              password: 'string - plaintext password (required)',
              role: "string - 'tutor' | 'tutee' | 'admin' (required, case-insensitive)"
            }
          },
          output: {
            username: 'string',
            role: 'string',
            status: 'string'
          },
          example: {
            request: {
              username: 'Tuấn BK',
              password: 't@ssw0r123!',
              role: 'tutee'
            },
            response: {
              username: 'Tuấn BK',
              role: 'tutee',
              status: 'Login successful'
            }
          },
          errors: [
            '401: Incorrect username or password',
            '403: You don\'t have permission to login as {role}',
            '403: You don\'t have permission to login as admin (only sManager can be admin)'
          ]
        },
        {
          name: 'Logout',
          method: 'POST',
          path: '/logout',
          auth: true,
          roles: ['any'],
          description: 'Clear session cookie and logout',
          input: null,
          output: { status: 'Logout successful' },
          example: { response: { status: 'Logout successful' } }
        }
      ]
    },

    /* =====================================================
       USERS (routes_user.py)
       ===================================================== */
    {
      group: 'Users',
      basePath: '/users',
      description: 'User CRUD operations, interests, instructors, qualifications, and lesson progress tracking.',
      endpoints: [
        {
          name: 'Get Current User',
          method: 'GET',
          path: '/me',
          auth: true,
          roles: ['any'],
          description: 'Get authenticated user\'s profile',
          input: null,
          output: {
            status: 'string',
            user: {
              UserID: 'string(10)',
              User_name: 'string(100) - unique',
              Full_name: 'string(100) nullable',
              Email: 'string(100) - unique, validated format'
            }
          },
          example: {
            response: {
              status: 'success',
              user: {
                UserID: 'USR00006',
                User_name: 'Tuấn BK',
                Full_name: 'Nguyễn Anh Tuấn',
                Email: 'anhtuan@hcmut.edu.vn'
              }
            }
          }
        },
        {
          name: 'Create User (Register)',
          method: 'POST',
          path: '',
          auth: false,
          description: 'Register new user account. UserID auto-generated if not provided.',
          input: {
            body: {
              User_name: 'string(100) - required, unique, NVARCHAR',
              Email: 'string(100) - required, unique, must match format *@*.*',
              Password: 'string(255) - required, min 6 chars, must contain: lowercase, uppercase, digit, special char',
              Full_name: 'string(100) - optional, NVARCHAR',
              City: 'string(100) - optional, NVARCHAR',
              Country: 'string(100) - optional, NVARCHAR',
              Phone: 'string(10) - optional',
              Date_of_birth: 'date (YYYY-MM-DD) - optional',
              IFlag: 'boolean - optional, instructor flag (default false)',
              SFlag: 'boolean - optional, student flag (default false)',
              Bio_text: 'string(MAX) - optional, NVARCHAR',
              Year_of_experience: 'integer - optional, >= 0'
            }
          },
          output: {
            status: 'created',
            user_id: 'string(10) - auto-generated format USR#####'
          },
          example: {
            request: {
              User_name: 'alice_new',
              Email: 'alice@example.com',
              Password: 'StrongP@ss123',
              Full_name: 'Alice Example',
              Country: 'Vietnam',
              SFlag: true
            },
            response: { status: 'created', user_id: 'USR00014' }
          },
          errors: [
            '400: Email must match format check',
            '400: Password requirements not met',
            '400: Duplicate username or email'
          ]
        },
        {
          name: 'List All Users',
          method: 'GET',
          path: '',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Get all users (instructors and admins only)',
          input: {
            query: {
              limit: 'integer - default 100, max 100 (pagination)'
            }
          },
          output: {
            status: 'success',
            count: 'integer',
            user: 'array of { UserID, User_name, Full_name }'
          },
          example: {
            response: {
              status: 'success',
              count: 13,
              user: [
                { UserID: 'USR00001', User_name: 'Đạt Phạm', Full_name: 'Phạm Lê Tiến Đạt' }
              ]
            }
          }
        },
        {
          name: 'Get User by ID',
          method: 'GET',
          path: '/{user_id}',
          auth: true,
          roles: ['any'],
          description: 'Get specific user profile. Students can only view their own profile.',
          input: { path: { user_id: 'string(10)' } },
          output: {
            status: 'success',
            user: {
              UserID: 'string(10)',
              User_name: 'string(100)',
              Email: 'string(100)',
              Full_name: 'string(100)',
              City: 'string(100) nullable',
              Country: 'string(100) nullable'
            }
          },
          errors: ['404: User not found', '403: Not authorized to view this user']
        },
        {
          name: 'Update User',
          method: 'PUT',
          path: '/{user_id}',
          auth: true,
          roles: ['any'],
          description: 'Update user profile. Students can only update their own profile.',
          input: {
            path: { user_id: 'string(10)' },
            body: {
              Full_name: 'string(100) - optional',
              City: 'string(100) - optional',
              Country: 'string(100) - optional',
              Phone: 'string(10) - optional',
              Bio_text: 'string(MAX) - optional',
              Year_of_experience: 'integer - optional'
            }
          },
          output: { status: 'updated', user_id: 'string(10)' },
          errors: ['404: User not found', '403: Not authorized to update this user']
        },
        {
          name: 'Delete User',
          method: 'DELETE',
          path: '/{user_id}',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Delete user account and all related data (cascading)',
          input: { path: { user_id: 'string(10)' } },
          output: { status: 'deleted', user_id: 'string(10)' },
          errors: ['404: User not found']
        },
        {
          name: 'List Instructors',
          method: 'GET',
          path: '/instructors',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Get all users with instructor flag (IFlag = true)',
          input: null,
          output: { status: 'success', count: 'integer' }
        },
        {
          name: 'List Students',
          method: 'GET',
          path: '/students',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Get all users with student flag (SFlag = true)',
          input: null,
          output: { status: 'success', count: 'integer' }
        },
        {
          name: 'Search Users',
          method: 'GET',
          path: '/search',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Search users by full name (LIKE query)',
          input: { query: { name: 'string - search term (required)' } },
          output: { status: 'success', count: 'integer', users: 'array' }
        },

        /* Takes (Lesson Progress) */
        {
          name: 'Create Take (Start Lesson)',
          method: 'POST',
          path: '',
          subPath: '/takes',
          auth: true,
          roles: ['any'],
          description: 'Record that user is taking/has taken a lesson. Auto-sets UserID to current user if not provided.',
          input: {
            body: {
              UserID: 'string(10) - optional, defaults to current user',
              LessonID: 'string(10) - required, references LESSON_REF',
              is_finished: 'boolean - optional, default false'
            }
          },
          output: { status: 'created', UserID: 'string(10)', LessonID: 'string(10)' },
          example: {
            request: { LessonID: 'CON001', is_finished: false },
            response: { status: 'created', UserID: 'USR00006', LessonID: 'CON001' }
          },
          errors: [
            '403: Not authorized to create take for another user (students)',
            '400: Duplicate entry (user already taking this lesson)'
          ]
        },
        {
          name: 'Get Take (User + Lesson)',
          method: 'GET',
          path: '',
          subPath: '/takes/{user_id}/{lesson_id}',
          auth: true,
          roles: ['any'],
          description: 'Get specific lesson progress for user',
          input: {
            path: {
              user_id: 'string(10)',
              lesson_id: 'string(10)'
            }
          },
          output: {
            status: 'success',
            take: {
              UserID: 'string(10)',
              LessonID: 'string(10)',
              is_finished: 'boolean'
            }
          },
          errors: ['404: Take not found', '403: Not authorized']
        },
        {
          name: 'Get User Lessons',
          method: 'GET',
          path: '',
          subPath: '/takes/user/{user_id}',
          auth: true,
          roles: ['any'],
          description: 'Get all lessons taken by user (with completion status)',
          input: { path: { user_id: 'string(10)' } },
          output: { status: 'success', count: 'integer' }
        },
        {
          name: 'Mark Lesson Finished',
          method: 'POST',
          path: '',
          subPath: '/takes/{user_id}/{lesson_id}/finish',
          auth: true,
          roles: ['any'],
          description: 'Mark lesson as completed (is_finished = true)',
          input: { path: { user_id: 'string(10)', lesson_id: 'string(10)' } },
          output: { status: 'updated', UserID: 'string(10)', LessonID: 'string(10)' },
          errors: ['404: Take not found', '403: Not authorized']
        },
        {
          name: 'Mark Lesson Unfinished',
          method: 'POST',
          path: '',
          subPath: '/takes/{user_id}/{lesson_id}/unfinished',
          auth: true,
          roles: ['any'],
          description: 'Mark lesson as incomplete (is_finished = false)',
          input: { path: { user_id: 'string(10)', lesson_id: 'string(10)' } },
          output: { status: 'updated', UserID: 'string(10)', LessonID: 'string(10)' }
        },
        {
          name: 'Delete Take',
          method: 'DELETE',
          path: '',
          subPath: '/takes/{user_id}/{lesson_id}',
          auth: true,
          roles: ['any'],
          description: 'Remove lesson progress record',
          input: { path: { user_id: 'string(10)', lesson_id: 'string(10)' } },
          output: { status: 'deleted' }
        },
        {
          name: 'Get Lesson Progress (Summary)',
          method: 'GET',
          path: '',
          subPath: '/takes/{user_id}/progress',
          auth: true,
          roles: ['any'],
          description: 'Get user\'s lesson completion statistics',
          input: { path: { user_id: 'string(10)' } },
          output: {
            status: 'success',
            progress: {
              total_lessons: 'integer',
              completed_lessons: 'integer',
              incomplete_lessons: 'integer',
              completion_rate: 'float - percentage (0-100)'
            }
          },
          example: {
            response: {
              status: 'success',
              progress: {
                total_lessons: 10,
                completed_lessons: 6,
                incomplete_lessons: 4,
                completion_rate: 60.0
              }
            }
          }
        },

        /* Interests */
        {
          name: 'Add Interest',
          method: 'POST',
          path: '',
          subPath: '/{user_id}/interests',
          auth: true,
          roles: ['any'],
          description: 'Add learning interest for student (composite key: UserID + Interest)',
          input: {
            path: { user_id: 'string(10)' },
            body: {
              interest: 'string(100) - NVARCHAR, e.g. "Python", "Web Development"'
            }
          },
          output: { status: 'created', user_id: 'string(10)', interest: 'string(100)' },
          errors: ['403: Not authorized', '400: Duplicate interest for user']
        },
        {
          name: 'Get User Interests',
          method: 'GET',
          path: '',
          subPath: '/{user_id}/interests',
          auth: true,
          roles: ['any'],
          description: 'List all interests for user',
          input: { path: { user_id: 'string(10)' } },
          output: { status: 'success', count: 'integer', interests: 'array of strings' }
        },
        {
          name: 'Clear User Interests',
          method: 'DELETE',
          path: '',
          subPath: '/{user_id}/interests',
          auth: true,
          roles: ['any'],
          description: 'Remove all interests for user',
          input: { path: { user_id: 'string(10)' } },
          output: { status: 'deleted' },
          errors: ['404: No interests to clear', '403: Not authorized']
        },

        /* Qualifications */
        {
          name: 'Add Qualification',
          method: 'POST',
          path: '',
          subPath: '/{user_id}/qualifications',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Add professional qualification for instructor (composite key: UserID + Qualification)',
          input: {
            path: { user_id: 'string(10)' },
            body: {
              qualification: 'string(200) - e.g. "PhD in Computer Science"'
            }
          },
          output: { status: 'created', user_id: 'string(10)' },
          errors: ['400: Duplicate qualification']
        },
        {
          name: 'Get User Qualifications',
          method: 'GET',
          path: '',
          subPath: '/{user_id}/qualifications',
          auth: true,
          roles: ['any'],
          description: 'List qualifications for instructor',
          input: { path: { user_id: 'string(10)' } },
          output: { status: 'success', count: 'integer' }
        },
        {
          name: 'Remove Qualification',
          method: 'DELETE',
          path: '',
          subPath: '/{user_id}/qualifications/{qualification}',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Remove specific qualification',
          input: {
            path: {
              user_id: 'string(10)',
              qualification: 'string(200) - must match exactly'
            }
          },
          output: { status: 'deleted' },
          errors: ['404: Qualification not found']
        },
        {
          name: 'Clear All Qualifications',
          method: 'DELETE',
          path: '',
          subPath: '/{user_id}/qualifications',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Remove all qualifications for instructor',
          input: { path: { user_id: 'string(10)' } },
          output: { status: 'deleted' }
        },

        /* Instructor-Course Assignment */
        {
          name: 'Assign Instructor to Course',
          method: 'POST',
          path: '',
          subPath: '/instruct',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Assign instructor to teach course (composite key: UserID + CourseID)',
          input: {
            body: {
              UserID: 'string(10) - instructor user ID',
              CourseID: 'string(10) - course ID'
            }
          },
          output: { status: 'assigned', UserID: 'string(10)', CourseID: 'string(10)' },
          example: {
            request: { UserID: 'USR00001', CourseID: 'CRS00001' },
            response: { status: 'assigned', UserID: 'USR00001', CourseID: 'CRS00001' }
          },
          errors: ['400: Duplicate assignment']
        },
        {
          name: 'Get Instructor Courses',
          method: 'GET',
          path: '',
          subPath: '/instructors/{user_id}/courses',
          auth: true,
          roles: ['any'],
          description: 'Get all courses taught by instructor',
          input: { path: { user_id: 'string(10)' } },
          output: { status: 'success', count: 'integer' }
        },
        {
          name: 'Get Course Instructors',
          method: 'GET',
          path: '',
          subPath: '/courses/{course_id}/instructors',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Get all instructors teaching course',
          input: { path: { course_id: 'string(10)' } },
          output: { status: 'success', count: 'integer' }
        },
        {
          name: 'Remove Instructor',
          method: 'DELETE',
          path: '',
          subPath: '/instruct/{user_id}/{course_id}',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Unassign instructor from course',
          input: {
            path: { user_id: 'string(10)', course_id: 'string(10)' }
          },
          output: { status: 'deleted' },
          errors: ['404: Instructor assignment not found']
        },
        {
          name: 'Check is Instructor of Course',
          method: 'GET',
          path: '',
          subPath: '/instruct/is/{user_id}/{course_id}',
          auth: true,
          roles: ['any'],
          description: 'Verify if user is instructor for specific course',
          input: { path: { user_id: 'string(10)', course_id: 'string(10)' } },
          output: { status: 'success', is_instructor: 'boolean' }
        }
      ]
    },

    /* =====================================================
       COURSES & CONTENT (routes_course.py)
       ===================================================== */
    {
      group: 'Courses & Content',
      basePath: '/courses',
      description: 'Course management, modules, content (text/video/image), categories, and prerequisites.',
      endpoints: [
        {
          name: 'List All Courses',
          method: 'GET',
          path: '',
          auth: true,
          roles: ['any'],
          description: 'Get all courses with optional filtering',
          input: {
            query: {
              limit: 'integer - default 100, max 100',
              difficulty: "string - optional filter: 'Beginner' | 'Intermediate' | 'Advanced'"
            }
          },
          output: {
            status: 'success',
            count: 'integer',
            courses: 'array of { CourseID, Title, Difficulty, Language, Description }'
          },
          example: {
            response: {
              status: 'success',
              count: 6,
              courses: [
                {
                  CourseID: 'CRS00001',
                  Title: 'Python cho DeepLearning',
                  Difficulty: 'Intermediate',
                  Language: 'Tiếng Việt',
                  Description: 'Học cách xây dựng, huấn luyện...'
                }
              ]
            }
          }
        },
        {
          name: 'Create Course',
          method: 'POST',
          path: '',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Create new course. CourseID auto-generated if not provided.',
          input: {
            body: {
              Title: 'string(200) - required, min 5 chars, NVARCHAR',
              Language: 'string(50) - required, e.g. "Tiếng Việt", "English"',
              Difficulty: "string(20) - optional: 'Beginner' | 'Intermediate' | 'Advanced'",
              Description: 'string(MAX) - optional, NVARCHAR'
            }
          },
          output: { status: 'created', course_id: 'string(10)', title: 'string(200)' },
          example: {
            request: {
              Title: 'Machine Learning Advanced',
              Language: 'English',
              Difficulty: 'Advanced'
            },
            response: { status: 'created', course_id: 'CRS00007', title: 'Machine Learning Advanced' }
          },
          errors: ['400: Title must be at least 5 characters']
        },
        {
          name: 'Get Course by ID',
          method: 'GET',
          path: '',
          subPath: '/id/{course_id}',
          auth: true,
          roles: ['any'],
          description: 'Get course details with categories and prerequisites',
          input: { path: { course_id: 'string(10)' } },
          output: {
            status: 'success',
            course: {
              CourseID: 'string(10)',
              Title: 'string(200)',
              Difficulty: 'string(20)',
              Language: 'string(50)',
              Description: 'string(MAX)',
              Categories: 'array of strings',
              Prerequisites: 'array of CourseIDs'
            }
          },
          errors: ['404: Course not found']
        },
        {
          name: 'Update Course',
          method: 'PUT',
          path: '',
          subPath: '/{course_id}',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Update course information',
          input: {
            path: { course_id: 'string(10)' },
            body: {
              Title: 'string(200) - optional',
              Description: 'string(MAX) - optional',
              Difficulty: 'string(20) - optional',
              Language: 'string(50) - optional'
            }
          },
          output: { status: 'updated', course_id: 'string(10)' }
        },
        {
          name: 'Delete Course',
          method: 'DELETE',
          path: '',
          subPath: '/{course_id}',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Delete course and all related data (cascading)',
          input: { path: { course_id: 'string(10)' } },
          output: { status: 'deleted', course_id: 'string(10)' }
        },
        {
          name: 'Search Courses by Title',
          method: 'GET',
          path: '',
          subPath: '/search',
          auth: true,
          roles: ['any'],
          description: 'Search courses by title (LIKE query)',
          input: {
            query: {
              title: 'string - search term (required, min 1 char)'
            }
          },
          output: {
            status: 'success',
            count: 'integer',
            courses: 'array of { CourseID, Title }'
          }
        },

        /* Categories */
        {
          name: 'Add Category to Course',
          method: 'POST',
          path: '',
          subPath: '/{course_id}/categories',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Add category tag to course (composite key: CourseID + Category)',
          input: {
            path: { course_id: 'string(10)' },
            body: {
              category: 'string(100) - e.g. "Python", "Web Development", NVARCHAR'
            }
          },
          output: { status: 'added', category: 'string(100)' },
          errors: ['400: Duplicate category']
        },
        {
          name: 'Get Course Categories',
          method: 'GET',
          path: '',
          subPath: '/{course_id}/categories',
          auth: true,
          roles: ['any'],
          description: 'List all categories for course',
          input: { path: { course_id: 'string(10)' } },
          output: { status: 'success', categories: 'array of strings' }
        },
        {
          name: 'Remove Category',
          method: 'DELETE',
          path: '',
          subPath: '/{course_id}/categories/{category}',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Remove category from course',
          input: {
            path: { course_id: 'string(10)', category: 'string(100)' }
          },
          output: { status: 'deleted' },
          errors: ['404: Category not found']
        },

        /* Prerequisites */
        {
          name: 'Add Prerequisite',
          method: 'POST',
          path: '',
          subPath: '/{course_id}/prerequisites',
          auth: true,
          roles: ['tutor', 'admin'],
          description: 'Require another course to be completed before taking this course',
          input: {
            path: { course_id: 'string(10)' },
            body: {
              required_course_id: 'string(10) - prerequisite course ID'
            }
          },
          output: { status: 'added', prerequisite: 'string(10)' },
          example: {
            request: { required_course_id: 'CRS00005' },
            response: { status: 'added', prerequisite: 'CRS00005' }
          },
          errors: [
            '400: A course cannot be its own prerequisite',
            '400: Duplicate prerequisite'
          ]
        },
        {
          name: 'Get Prerequisites',
          method: 'GET',
          path: '',
          subPath: '/{course_id}/prerequisites',
          auth: true,
          roles: ['any'],
          description: 'List all prerequisite courses',
          input: { path: { course_id: 'string(10)' } },
          output: {
            status: 'success',
            prerequisites: 'array of CourseIDs'
          }
        },
        {
          name: 'Check Prerequisites Completion',
          method: 'GET',
          path: '',
          subPath: '/{course_id}/prerequisites/f',
          auth: true,
          roles: ['tutee'],
          description: 'Check if student has completed all prerequisites for course (uses CheckPrerequisiteCompletion procedure)',
          input: { path: { course_id: 'string(10)' } },
          output: {
            status: 'success',
            count: 'integer',
            missing_prereqs: 'array of missing prerequisite CourseIDs'
          },
          note: 'Empty array means all prerequisites are satisfied'
        },
        {
          name: 'Remove Prerequisite',
          method: 'DELETE',
          path: '',
          subPath: '/{course_id}/prerequisites/{required_course_id}',
          auth: true,