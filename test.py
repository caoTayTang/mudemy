from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey, Text, Time, Date

Base = declarative_base()
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=False)
session = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    
    #sessions = relationship("CourseSession", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(id={self.id}, title={self.title})>"
    
    
class CourseSession(Base):
    """
    Model for individual recurring sessions of a course.
    Corresponds to the 'schedule' array in the mock data.
    """
    __tablename__ = "course_sessions"

    id = Column(Integer, primary_key=True, index=True) 
    course_id = Column(Integer, ForeignKey("courses.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    session_number = Column(Integer, nullable=False)

    #course = relationship("Course", back_populates="sessions")

    def __repr__(self):
        return f"<CourseSession(course_id={self.course_id}, id={self.id}, number={self.session_number})>"

if __name__ == '__main__':  
    Base.metadata.drop_all(bind=engine, tables=[
        Course.__table__,
        CourseSession.__table__
    ])

    Base.metadata.create_all(bind=engine, tables=[
        Course.__table__,
        CourseSession.__table__
    ])
    db = session()
    course1 =  Course(title="Kinh tế lượng for noob")
    course2 =  Course(title="Test chơi")
       
    db.add_all([
       course1,
       course2
    ])
    db.commit()
    db.add_all([
         CourseSession(session_number=1, course_id=1),
         CourseSession(session_number=2, course_id=2),
         CourseSession(session_number=1, course_id=1),
    ])
    db.commit()
    

    print("Done seeding data...")

    c1 = db.query(Course).filter(Course.id == 1).first()
    db.delete(c1)
    db.commit()

    cs = db.query(CourseSession).all()

    for c in cs:
        print(f'{c} is belong to {c.course_id}')


    db.close()