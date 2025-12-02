from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, date
from app.models import User, Course, Module, Payment, Enrollment, mudemy_session
from app.services import UserService, CourseService, EnrollmentService

import warnings
warnings.filterwarnings('ignore', message='.*Unrecognized server version info.*')

# Database configuration
SERVER_NAME = 'DESKTOP-IM92AEE\\SQLEXPRESS' 
DATABASE_NAME = 'MUDemy'
CONNECTION_STRING = f'mssql+pyodbc://@{SERVER_NAME}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'

# engine = create_engine(CONNECTION_STRING, echo=True)
# mudemy_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize services
user_service = UserService(mudemy_session)
course_service = CourseService(mudemy_session)
enrollment_service = EnrollmentService(mudemy_session)


def test_queries():    
    # Test 1: Get user by username (from your INSERT_DATA.sql)
    print("1. Testing get_by_username...")
    user = user_service.get_by_username("Thuận Lương")  # First user from your SQL
    if user:
        print(f"Found user: {user.SFlag} ({user.Password})")
    else:
        print("User not found")
    
    # Test 2: Get user by ID
    # print("\n2. Testing get_by_id...")
    # user = user_service.get_by_id("USR00001")
    # if user:
    #     print(f"   ✓ Found user: {user.Full_name} - {user.Email}")
    # else:
    #     print("   ✗ User not found")
    
    # # Test 3: Get all students
    # print("\n3. Testing get_students...")
    # students = user_service.get_students(limit=5)
    # print(f"   ✓ Found {len(students)} students:")
    # for student in students:
    #     print(f"      - {student.User_name} ({student.UserID})")
    
    # # Test 4: Get all instructors
    # print("\n4. Testing get_instructors...")
    # instructors = user_service.get_instructors()
    # print(f"   ✓ Found {len(instructors)} instructors:")
    # for instructor in instructors:
    #     print(f"      - {instructor.User_name} ({instructor.UserID})")
    
    # Test 5: Get course by ID
    # print("\n5. Testing get_course_by_id...")
    # course = course_service.get_by_id("CRS00001")
    # if course:
    #     print(f"   ✓ Found course: {course.Title}")
    #     print(f"      Difficulty: {course.Difficulty}")
    #     print(f"      Language: {course.Language}")
    # else:
    #     print("   ✗ Course not found")
    
    # # Test 6: Get all courses
    # print("\n6. Testing get_all_courses...")
    # courses = course_service.get_all()
    # print(f"   ✓ Found {len(courses)} courses:")
    # for course in courses:
    #     print(f"      - {course.Title} ({course.CourseID})")
    
    # # Test 7: Get enrollments by student
    # print("\n7. Testing get_enrollments_by_student...")
    # enrollments = enrollment_service.get_by_student("USR00013")
    # print(f"   ✓ Found {len(enrollments)} enrollments for USR00013:")
    # for enrollment in enrollments:
    #     print(f"      - Course: {enrollment.CourseID}, Status: {enrollment.Status}")
    
    # # Test 8: Get user qualifications
    # print("\n8. Testing get_qualifications...")
    # qualifications = user_service.get_qualifications("USR00001")
    # print(f"   ✓ Found {len(qualifications)} qualifications:")
    # for qual in qualifications:
    #     print(f"      - {qual}")
    
    # # Test 9: Get user interests
    # print("\n9. Testing get_interests...")
    # interests = user_service.get_interests("USR00006")
    # print(f"   ✓ Found {len(interests)} interests:")
    # for interest in interests:
    #     print(f"      - {interest}")
    
    # # Test 10: Get course categories
    # print("\n10. Testing get_categories...")
    # categories = course_service.get_categories("CRS00001")
    # print(f"   ✓ Found {len(categories)} categories for CRS00001:")
    # for category in categories:
    #     print(f"      - {category}")
    
    # print("\n" + "="*50)
    # print("ALL TESTS COMPLETED")
    # print("="*50 + "\n")


def seed_additional_data():
    """Add some additional test data"""
    print("\n" + "="*50)
    print("SEEDING ADDITIONAL DATA")
    print("="*50 + "\n")
    
    try:
        # Add a new user
        print("1. Creating new user...")
        new_user = user_service.create(
            user_id="USR00014",
            username="TestUser",
            email="testuser@example.com",
            password="Test@123",
            full_name="Test User",
            city="Hanoi",
            country="Vietnam",
            is_student=True
        )
        print(f"   ✓ Created user: {new_user.User_name}")
        
        # Add interests to the new user
        print("\n2. Adding interests to new user...")
        user_service.add_interest("USR00014", "Python")
        user_service.add_interest("USR00014", "Machine Learning")
        print("   ✓ Added interests")
        
        # Create a new course
        print("\n3. Creating new course...")
        new_course = course_service.create(
            course_id="CRS00007",
            title="Introduction to Machine Learning",
            language="English",
            description="Learn the basics of ML",
            difficulty="Intermediate"
        )
        print(f"   ✓ Created course: {new_course.Title}")
        
        # Add categories to the course
        print("\n4. Adding categories to new course...")
        course_service.add_category("CRS00007", "Machine Learning")
        course_service.add_category("CRS00007", "AI")
        print("   ✓ Added categories")
        
        print("\n" + "="*50)
        print("SEEDING COMPLETED SUCCESSFULLY")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n   ✗ Error: {e}")


if __name__ == "__main__":    
    try:
        # Test existing data
        #test_queries()
        users = user_service.get_all_users()
        for user in users:
            print(user.User_name, user.Password)
        # Optionally seed additional data
        # Uncomment the line below to add test data
        # seed_additional_data()
        
    except Exception as e:
        print(f"\n✗ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
