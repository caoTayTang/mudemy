from models import*
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime, time, date, timedelta

def seed_user(engine, db):
    Base.metadata.drop_all(bind=engine, tables=[
        MututorUser.__table__,])
    Base.metadata.create_all(bind=engine, tables=[
        MututorUser.__table__,])


    mock_users = [
        {"username": "a.nguyen21", "role": UserRole.TUTOR, "id": "2210001"},
        {"username": "c.levan", "role": UserRole.TUTOR, "id": "1235"},
        {"username": "e.hoang21", "role": UserRole.TUTOR, "id": "2310003"},
        {"username": "d.phamthi", "role": UserRole.ADMIN, "id": "0102"},
    ]

    print(f"--- Populating '{DATABASE_URL}' with mock data ---")

    try:
        for u in mock_users:

            existing = db.query(MututorUser).filter_by(username=u["username"]).first()
            if existing:
                print(f"User '{u['username']}' already exists, skipping.")
                continue

            new_user = MututorUser(**u)
            db.add(new_user)
            print(f"Added: {new_user}")

        db.commit()
        print("\n--- Data committed successfully ---")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

    finally:
        db.close()
        print("\n--- Database session closed ---")

def seed_notification(engine, db):
    Base.metadata.drop_all(bind=engine, tables=[
        Notification.__table__,])
    Base.metadata.create_all(bind=engine, tables=[
        Notification.__table__,])
    
    print("Seeding data...")

    try:
        print("Seeding Notifications...")

        TUTEE_ID_1 = '2010002'
        TUTOR_ID_1 = '2310003'
        now = datetime.utcnow()

        notifications_data = [
            {
                "id": 1,
                "user_id": TUTEE_ID_1,
                "type": NotificationType.SESSION_REMINDER,
                "title": "Nhắc nhở sự kiện",
                "content": "Khóa học Kinh tế lượng sắp bắt đầu",
                "is_read": False,
                "related_id": 1, 
                "created_at": now - timedelta(hours=2) 
            },
            {
                "id": 2,
                "user_id": TUTEE_ID_1,
                "type": NotificationType.ENROLLMENT_SUCCESS,
                "title": "Đăng ký thành công",
                "content": "Bạn đã được thêm vào lớp Lập trình C++",
                "is_read": False, 
                "related_id": 2, 
                "created_at": now - timedelta(days=1)
            },
            {
                "id": 3,
                "user_id": TUTOR_ID_1,
                "type": NotificationType.FEEDBACK_REQUEST,
                "title": "Có feedback",
                "content": "Thầy đẹp trai quá",
                "is_read": True, 
                "related_id": None,
                "created_at": now - timedelta(days=3) 
            }
        ]

        for data in notifications_data:
            notification = db.query(Notification).filter_by(id=data['id']).first()
            if not notification:
                db.add(Notification(**data))
                print(f"Added Notification: id={data['id']} (User: {data['user_id']}, Title: {data['title']})")
        
        db.commit()
        print("Committed Notifications.")
    except Exception as e:
        print(f"\n--- An error occurred during seeding ---")
        print(e)
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

def seed_course(engine,db):
    Base.metadata.drop_all(bind=engine, tables=[
        Course.__table__,
        CourseSession.__table__,
        CourseResource.__table__
    ])

    Base.metadata.create_all(bind=engine, tables=[
        Course.__table__,
        CourseSession.__table__,
        CourseResource.__table__
    ])

    print("Seeding Courses and Sessions...")
    try: 
        # Course 1
        course1 = db.query(Course).filter_by(id=1).first()
        if not course1:
            course1 = Course(
                id=1, tutor_id="2210001", subject_id=366, level=Level.BEGINNER,
                title="Kinh tế lượng for noob",
                description="Khóa học Kinh tế lượng dành cho sinh viên năm nhất",
                status=CourseStatus.OPEN, max_students=20,
                created_at=datetime.fromisoformat("2025-10-01T10:00:00Z")
            )
            db.add(course1)
            db.add_all([
                CourseSession(session_number=1, course=course1, session_date=date(2025, 11, 13), start_time=time(18, 0), end_time=time(20, 0), location="H1-201", format=CourseFormat.OFFLINE),
                CourseSession(session_number=2, course=course1, session_date=date(2025, 11, 20), start_time=time(18, 0), end_time=time(20, 0), location="H1-201", format=CourseFormat.OFFLINE),
                CourseSession(session_number=3, course=course1, session_date=date(2025, 11, 27), start_time=time(18, 0), end_time=time(20, 0), location="https://meet.google.com/toi-yeu-mu", format=CourseFormat.ONLINE),
                CourseResource(course_id=1,resource_id=3),
                CourseResource(course_id=1,resource_id=4)
            ])
            print("Added Course: Kinh tế lượng for noob")

        # Course 2
        course2 = db.query(Course).filter_by(id=2).first()
        if not course2:
            course2 = Course(
                id=2, tutor_id="1235", subject_id=102, level=Level.BEGINNER,
                title="Lập trình C++",
                description="Học lập trình C++ từ cơ bản đến nâng cao",
                status=CourseStatus.OPEN, max_students=15,
                created_at=datetime.fromisoformat("2025-09-20T08:00:00Z")
            )
            db.add(course2)
            db.add_all([
                CourseSession(session_number=1, course=course2, session_date=date(2025, 11, 11), start_time=time(19, 0), end_time=time(21, 0), location="https://meet.google.com/toi-yeu-mu", format=CourseFormat.ONLINE),
                CourseSession(session_number=2, course=course2, session_date=date(2025, 11, 18), start_time=time(19, 0), end_time=time(21, 0), location="B4-Lab1", format=CourseFormat.OFFLINE),
                CourseResource(course_id=2,resource_id=1),
                CourseResource(course_id=2,resource_id=2)
            ])
            print("Added Course: Lập trình C++")
    
        db.commit()
        print("Committed Courses and Sessions.")
    except Exception as e:
        print(f"\n--- An error occurred during seeding ---")
        print(e)
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

def seed_subject(engine, db):
    Base.metadata.drop_all(bind=engine, tables=[
        Subject.__table__,
    ])

    Base.metadata.create_all(bind=engine, tables=[
        Subject.__table__,
    ])

    try:
        print("Seeding Subjects...")
        subjects_data = [
            { "id": 101, "name": "Toán cao cấp" },
            { "id": 102, "name": "Lập trình" },
            { "id": 103, "name": "Vật lý" },
            { "id": 104, "name": "Triết học" },
            { "id": 666, "name": "7 day lên cao thủ" },
            { "id": 336, "name": "Seminar"},
            { "id": 366, "name": "Miscellaneous"}
        ]
        for sub_data in subjects_data:
            if not db.query(Subject).filter_by(id=sub_data['id']).first():
                db.add(Subject(**sub_data))
        db.commit()
        print("Committed Subjects.")
    except Exception as e:
        print(f"\n--- An error occurred during seeding ---")
        print(e)
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

def seed_enrollment(engine,db):
    Base.metadata.drop_all(bind=engine, tables=[
        Enrollment.__table__,
    ])

    Base.metadata.create_all(bind=engine, tables=[
        Enrollment.__table__,
    ])
    try:
        print("Seeding Enrollments...")
        TUTEE_ID_1 = "2010002"
        enrollments_data = [
            { "id": 1, "tuteeId": TUTEE_ID_1, "courseId": 1, "enrolledAt": "2025-10-02T15:00:00Z" },
            { "id": 2, "tuteeId": TUTEE_ID_1, "courseId": 3, "enrolledAt": "2025-10-03T16:00:00Z" },
            { "id": 3, "tuteeId": TUTEE_ID_1, "courseId": 4, "enrolledAt": "2025-10-04T09:00:00Z" },
        ]
        for data in enrollments_data:
            if not db.query(Enrollment).filter_by(id=data['id']).first():
                if db.query(Course).filter_by(id=data['courseId']).first():
                    db.add(Enrollment(
                        id=data['id'], tutee_id=data['tuteeId'], course_id=data['courseId'],
                        enrollment_date=datetime.fromisoformat(data['enrolledAt']),
                        status=EnrollmentStatus.ENROLLED
                    ))
                    print(f"Added Enrollment: id={data['id']}")
        db.commit()
        print("Committed Enrollments.")
    except Exception as e:
        print(f"\n--- An error occurred during seeding ---")
        print(e)
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

def seed_feeback_eval(engine,db):
    Base.metadata.drop_all(bind=engine, tables=[
        Feedback.__table__,
        SessionEvaluation.__table__,
    ])

    Base.metadata.create_all(bind=engine, tables=[
        Feedback.__table__,
        SessionEvaluation.__table__,
    ])
    TUTEE_ID_1 = "2010002"
    print("Seeding Feedbacks...")
    try:
        feedback_data = [
            {
                "id": 1, "user_id": TUTEE_ID_1,
                "topic": "Góp ý về nội dung khóa học",
                "content": "Nội dung khóa học Kinh tế lượng (ID: 1) rất hay nhưng cần thêm ví dụ thực tế về R.",
                "is_anonymous": False
            },
            {
                "id": 2, "user_id": TUTEE_ID_1,
                "topic": "Báo lỗi hệ thống",
                "content": "Nút 'Xem chi tiết' ở trang danh sách khóa học bị vỡ giao diện trên điện thoại.",
                
            },
            {
                "id": 3, "user_id": "2210001", 
                "topic": "Yêu cầu tính năng mới",
                "content": "Nên có tính năng chat realtime với giáo viên.",
                "is_anonymous": True
            },
            {
                "id": 4, "user_id": TUTEE_ID_1,
                "topic": "Khác",
                "content": "Làm thế nào để xem lại các buổi học đã qua?",
            }
        ]
        
        for data in feedback_data:
            if not db.query(Feedback).filter_by(id=data['id']).first():
                db.add(Feedback(**data))
                print(f"Added Feedback: id={data['id']} (Topic: {data['topic']})")
        
        db.commit()
        print("Committed Feedbacks.")


        print("Seeding Session Evaluations...")

        session_to_eval = db.query(CourseSession).filter_by(course_id=1, session_number=1).first()

        enrollment_to_eval = db.query(Enrollment).filter_by(id=1).first()

        if session_to_eval and enrollment_to_eval:
            eval1 = db.query(SessionEvaluation).filter_by(id=1).first()
            if not eval1:
                db.add(SessionEvaluation(
                    id=1,
                    session_id=session_to_eval.id,
                    enrollment_id=enrollment_to_eval.id,
                    rating=5,
                    comment="Buổi học rất tuyệt!"
                ))
                print("Added SessionEvaluation: id=1")
            db.commit()
            print("Committed Session Evaluations.")
    except Exception as e:
        print(f"\n--- An error occurred during seeding ---")
        print(e)
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

def seed_record(engine, db):
    Base.metadata.drop_all(bind=engine, tables=[
        MeetingRecord.__table__ ,
    ])

    Base.metadata.create_all(bind=engine, tables=[
        MeetingRecord.__table__,
    ])
    try:
        print("Seeding Meeting Record...")
        course1 = db.query(Course).filter_by(id=1).first()
        tutor1 = db.query(MututorUser).filter_by(id="2210001").first()
        
        if course1 and tutor1:
            record1 = db.query(MeetingRecord).filter_by(id=1).first()
            if not record1:
                db.add(MeetingRecord(
                    id=1, 
                    course_id=course1.id,
                    tutor_id=tutor1.id,
                    attendees="Tutor (2210001), 5 students",
                    discussion_points="Reviewed chapter 3 quiz results.",
                    status=MeetingRecordStatus.PENDING
                ))
                db.commit()
                print("Committed sample MeetingRecord.")

    except Exception as e:
        print(f"\n--- An error occurred during seeding ---")
        print(e)
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

def seed_session(engine, db):
    Base.metadata.drop_all(bind=engine, tables=[
        MuSession.__table__,])
    Base.metadata.create_all(bind=engine, tables=[
        MuSession.__table__,])

def seed_all(engine, db):
    seed_user(engine,db)
    seed_subject(engine,db)
    seed_course(engine,db)
    seed_enrollment(engine,db)
    seed_feeback_eval(engine,db)
    seed_record(engine,db)
    seed_notification(engine,db)
    #seed_session(engine,db)

if __name__ == "__main__":
    DATABASE_URL = "sqlite:///./app/models/mututor.db"

    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # seed_enrollment(engine,db)
    # seed_feeback_eval(engine,db)
    # seed_notification(engine,db)
    print("Seeding data...")

    seed_session(engine,db)
    #a= UserRole("tutor")



    