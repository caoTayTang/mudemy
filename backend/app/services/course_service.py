from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.models import (
    Course, Module, Requires, Content, LessonRef, 
    Text, Video, Image, Category
)


class CourseService:
    """Service for Course CRUD operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_course(self, course_data: Dict[str, Any]) -> Course:
        """Create a new course"""
        with self.db_session() as session:
            try:
                course = Course(**course_data)
                session.add(course)
                session.commit()
                session.refresh(course)
                return course
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating course: {str(e)}")
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """Get course by ID"""
        with self.db_session() as session:
            return session.query(Course).filter(Course.CourseID == course_id).first()
    
    def get_all_courses(self, limit: int = 100) -> List[Course]:
        """Get all courses with pagination"""
        with self.db_session() as session:
            return session.query(Course).limit(limit).all()
    
    def update_course(self, course_id: str, update_data: Dict[str, Any]) -> Optional[Course]:
        """Update course information"""
        with self.db_session() as session:
            course = session.query(Course).filter(Course.CourseID == course_id).first()
            if not course:
                return None
            
            for key, value in update_data.items():
                if hasattr(course, key):
                    setattr(course, key, value)
            
            session.commit()
            session.refresh(course)
            return course
    
    def delete_course(self, course_id: str) -> bool:
        """Delete a course"""
        with self.db_session() as session:
            course = session.query(Course).filter(Course.CourseID == course_id).first()
            if not course:
                return False
            
            session.delete(course)
            session.commit()
            return True
    
    def search_courses_by_title(self, title: str) -> List[Course]:
        """Search courses by title"""
        with self.db_session() as session:
            return session.query(Course).filter(Course.Title.like(f'%{title}%')).all()
    
    def get_courses_by_difficulty(self, difficulty: str) -> List[Course]:
        """Get courses by difficulty level"""
        with self.db_session() as session:
            return session.query(Course).filter(Course.Difficulty == difficulty).all()


class ModuleService:
    """Service for Module CRUD operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_module(self, module_data: Dict[str, Any]) -> Module:
        """Create a new module"""
        with self.db_session() as session:
            try:
                module = Module(**module_data)
                session.add(module)
                session.commit()
                session.refresh(module)
                return module
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating module: {str(e)}")
    
    def get_module_by_id(self, module_id: str) -> Optional[Module]:
        """Get module by ID"""
        with self.db_session() as session:
            return session.query(Module).filter(Module.ModuleID == module_id).first()
    
    def get_modules_by_course(self, course_id: str) -> List[Module]:
        """Get all modules for a specific course"""
        with self.db_session() as session:
            return session.query(Module).filter(Module.CourseID == course_id).all()
    
    def update_module(self, module_id: str, update_data: Dict[str, Any]) -> Optional[Module]:
        """Update module information"""
        with self.db_session() as session:
            module = session.query(Module).filter(Module.ModuleID == module_id).first()
            if not module:
                return None
            
            for key, value in update_data.items():
                if hasattr(module, key):
                    setattr(module, key, value)
            
            session.commit()
            session.refresh(module)
            return module
    
    def delete_module(self, module_id: str) -> bool:
        """Delete a module"""
        with self.db_session() as session:
            module = session.query(Module).filter(Module.ModuleID == module_id).first()
            if not module:
                return False
            
            session.delete(module)
            session.commit()
            return True


class RequiresService:
    """Service for course prerequisites (Requires) operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def add_prerequisite(self, course_id: str, required_course_id: str) -> Requires:
        """Add a prerequisite for a course"""
        if course_id == required_course_id:
            raise ValueError("A course cannot be its own prerequisite")
        
        with self.db_session() as session:
            try:
                prerequisite = Requires(CourseID=course_id, Required_courseID=required_course_id)
                session.add(prerequisite)
                session.commit()
                session.refresh(prerequisite)
                return prerequisite
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error adding prerequisite: {str(e)}")
    
    def get_prerequisites(self, course_id: str) -> List[Requires]:
        """Get all prerequisites for a course"""
        with self.db_session() as session:
            return session.query(Requires).filter(Requires.CourseID == course_id).all()
    
    def remove_prerequisite(self, course_id: str, required_course_id: str) -> bool:
        """Remove a prerequisite"""
        with self.db_session() as session:
            prerequisite = session.query(Requires).filter(
                Requires.CourseID == course_id,
                Requires.Required_courseID == required_course_id
            ).first()
            
            if not prerequisite:
                return False
            
            session.delete(prerequisite)
            session.commit()
            return True


class ContentService:
    """Service for Content CRUD operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_content(self, content_data: Dict[str, Any]) -> Content:
        """Create new content"""
        with self.db_session() as session:
            try:
                content = Content(**content_data)
                session.add(content)
                session.commit()
                session.refresh(content)
                return content
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating content: {str(e)}")
    
    def get_content_by_id(self, content_id: str) -> Optional[Content]:
        """Get content by ID"""
        with self.db_session() as session:
            return session.query(Content).filter(Content.ContentID == content_id).first()
    
    def get_content_by_module(self, module_id: str) -> List[Content]:
        """Get all content for a specific module"""
        with self.db_session() as session:
            return session.query(Content).filter(Content.ModuleID == module_id).all()
    
    def update_content(self, content_id: str, update_data: Dict[str, Any]) -> Optional[Content]:
        """Update content information"""
        with self.db_session() as session:
            content = session.query(Content).filter(Content.ContentID == content_id).first()
            if not content:
                return None
            
            for key, value in update_data.items():
                if hasattr(content, key):
                    setattr(content, key, value)
            
            session.commit()
            session.refresh(content)
            return content
    
    def delete_content(self, content_id: str) -> bool:
        """Delete content"""
        with self.db_session() as session:
            content = session.query(Content).filter(Content.ContentID == content_id).first()
            if not content:
                return False
            
            session.delete(content)
            session.commit()
            return True


class LessonRefService:
    """Service for LessonRef operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_lesson_ref(self, lesson_id: str) -> LessonRef:
        """Create a new lesson reference"""
        with self.db_session() as session:
            try:
                lesson_ref = LessonRef(LessonID=lesson_id)
                session.add(lesson_ref)
                session.commit()
                session.refresh(lesson_ref)
                return lesson_ref
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating lesson reference: {str(e)}")
    
    def get_lesson_ref_by_id(self, lesson_id: str) -> Optional[LessonRef]:
        """Get lesson reference by ID"""
        with self.db_session() as session:
            return session.query(LessonRef).filter(LessonRef.LessonID == lesson_id).first()
    
    def delete_lesson_ref(self, lesson_id: str) -> bool:
        """Delete lesson reference"""
        with self.db_session() as session:
            lesson_ref = session.query(LessonRef).filter(LessonRef.LessonID == lesson_id).first()
            if not lesson_ref:
                return False
            
            session.delete(lesson_ref)
            session.commit()
            return True


class TextService:
    """Service for Text content operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_text(self, text_data: Dict[str, Any]) -> Text:
        """Create new text content"""
        with self.db_session() as session:
            try:
                text = Text(**text_data)
                session.add(text)
                session.commit()
                session.refresh(text)
                return text
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating text: {str(e)}")
    
    def get_text_by_content_id(self, content_id: str) -> Optional[Text]:
        """Get text by content ID"""
        with self.db_session() as session:
            return session.query(Text).filter(Text.ContentID == content_id).first()
    
    def update_text(self, content_id: str, text_id: str, update_data: Dict[str, Any]) -> Optional[Text]:
        """Update text content"""
        with self.db_session() as session:
            text = session.query(Text).filter(
                Text.ContentID == content_id,
                Text.TextID == text_id
            ).first()
            
            if not text:
                return None
            
            for key, value in update_data.items():
                if hasattr(text, key):
                    setattr(text, key, value)
            
            session.commit()
            session.refresh(text)
            return text
    
    def delete_text(self, content_id: str, text_id: str) -> bool:
        """Delete text content"""
        with self.db_session() as session:
            text = session.query(Text).filter(
                Text.ContentID == content_id,
                Text.TextID == text_id
            ).first()
            
            if not text:
                return False
            
            session.delete(text)
            session.commit()
            return True


class VideoService:
    """Service for Video content operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_video(self, video_data: Dict[str, Any]) -> Video:
        """Create new video content"""
        with self.db_session() as session:
            try:
                video = Video(**video_data)
                session.add(video)
                session.commit()
                session.refresh(video)
                return video
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating video: {str(e)}")
    
    def get_video_by_content_id(self, content_id: str) -> Optional[Video]:
        """Get video by content ID"""
        with self.db_session() as session:
            return session.query(Video).filter(Video.ContentID == content_id).first()
    
    def update_video(self, content_id: str, video_id: str, update_data: Dict[str, Any]) -> Optional[Video]:
        """Update video content"""
        with self.db_session() as session:
            video = session.query(Video).filter(
                Video.ContentID == content_id,
                Video.VideoID == video_id
            ).first()
            
            if not video:
                return None
            
            for key, value in update_data.items():
                if hasattr(video, key):
                    setattr(video, key, value)
            
            session.commit()
            session.refresh(video)
            return video
    
    def delete_video(self, content_id: str, video_id: str) -> bool:
        """Delete video content"""
        with self.db_session() as session:
            video = session.query(Video).filter(
                Video.ContentID == content_id,
                Video.VideoID == video_id
            ).first()
            
            if not video:
                return False
            
            session.delete(video)
            session.commit()
            return True


class ImageService:
    """Service for Image content operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_image(self, image_data: Dict[str, Any]) -> Image:
        """Create new image content"""
        with self.db_session() as session:
            try:
                image = Image(**image_data)
                session.add(image)
                session.commit()
                session.refresh(image)
                return image
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating image: {str(e)}")
    
    def get_image_by_content_id(self, content_id: str) -> Optional[Image]:
        """Get image by content ID"""
        with self.db_session() as session:
            return session.query(Image).filter(Image.ContentID == content_id).first()
    
    def update_image(self, content_id: str, image_id: str, update_data: Dict[str, Any]) -> Optional[Image]:
        """Update image content"""
        with self.db_session() as session:
            image = session.query(Image).filter(
                Image.ContentID == content_id,
                Image.ImageID == image_id
            ).first()
            
            if not image:
                return None
            
            for key, value in update_data.items():
                if hasattr(image, key):
                    setattr(image, key, value)
            
            session.commit()
            session.refresh(image)
            return image
    
    def delete_image(self, content_id: str, image_id: str) -> bool:
        """Delete image content"""
        with self.db_session() as session:
            image = session.query(Image).filter(
                Image.ContentID == content_id,
                Image.ImageID == image_id
            ).first()
            
            if not image:
                return False
            
            session.delete(image)
            session.commit()
            return True


class CategoryService:
    """Service for Category operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def add_category(self, course_id: str, category: str) -> Category:
        """Add a category to a course"""
        with self.db_session() as session:
            try:
                cat = Category(CourseID=course_id, Category=category)
                session.add(cat)
                session.commit()
                session.refresh(cat)
                return cat
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error adding category: {str(e)}")
    
    def get_categories_by_course(self, course_id: str) -> List[Category]:
        """Get all categories for a course"""
        with self.db_session() as session:
            return session.query(Category).filter(Category.CourseID == course_id).all()
    
    def get_courses_by_category(self, category: str) -> List[Category]:
        """Get all courses in a specific category"""
        with self.db_session() as session:
            return session.query(Category).filter(Category.Category == category).all()
    
    def remove_category(self, course_id: str, category: str) -> bool:
        """Remove a category from a course"""
        with self.db_session() as session:
            cat = session.query(Category).filter(
                Category.CourseID == course_id,
                Category.Category == category
            ).first()
            
            if not cat:
                return False
            
            session.delete(cat)
            session.commit()
            return True