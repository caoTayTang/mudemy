from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from datetime import datetime
from ..models.models import (
    Course, Module, LessonRef, Content, Text, Video, Image,
    Assignment, Quiz, Question, Answer
)

class CourseService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, course_id: str, title: str, language: str,
               description: Optional[str] = None, difficulty: Optional[str] = None) -> Course:
        course = Course(
            CourseID=course_id,
            Title=title,
            Language=language,
            Description=description,
            Difficulty=difficulty
        )
        db = self.db_session()
        db.add(course)
        db.commit()
        db.refresh(course)
        db.close()
        return course

    def get_by_id(self, course_id: str) -> Optional[Course]:
        db = self.db_session()
        result = db.query(Course).filter(Course.CourseID == course_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Course]:
        db = self.db_session()
        result = db.query(Course).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_difficulty(self, difficulty: str) -> List[Course]:
        db = self.db_session()
        result = db.query(Course).filter(Course.Difficulty == difficulty).all()
        db.close()
        return result

    def get_by_language(self, language: str) -> List[Course]:
        db = self.db_session()
        result = db.query(Course).filter(Course.Language == language).all()
        db.close()
        return result

    def update(self, course_id: str, title: Optional[str] = None,
               description: Optional[str] = None, difficulty: Optional[str] = None,
               language: Optional[str] = None) -> Optional[Course]:
        db = self.db_session()
        course = db.query(Course).filter(Course.CourseID == course_id).first()
        if not course:
            db.close()
            return None
        
        if title is not None:
            course.Title = title
        if description is not None:
            course.Description = description
        if difficulty is not None:
            course.Difficulty = difficulty
        if language is not None:
            course.Language = language
        
        db.commit()
        db.refresh(course)
        db.close()
        return course

    def delete(self, course_id: str) -> bool:
        db = self.db_session()
        course = db.query(Course).filter(Course.CourseID == course_id).first()
        if not course:
            db.close()
            return False
        
        db.delete(course)
        db.commit()
        db.close()
        return True

    def add_category(self, course_id: str, category: str) -> bool:
        db = self.db_session()
        try:
            db.execute(category_table.insert().values(CourseID=course_id, Category=category))
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

    def remove_category(self, course_id: str, category: str) -> bool:
        db = self.db_session()
        result = db.execute(
            category_table.delete().where(
                (category_table.c.CourseID == course_id) & 
                (category_table.c.Category == category)
            )
        )
        db.commit()
        db.close()
        return result.rowcount > 0


class ModuleService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, module_id: str, title: str, course_id: str) -> Module:
        module = Module(
            ModuleID=module_id,
            Title=title,
            CourseID=course_id
        )
        db = self.db_session()
        db.add(module)
        db.commit()
        db.refresh(module)
        db.close()
        return module

    def get_by_id(self, module_id: str) -> Optional[Module]:
        db = self.db_session()
        result = db.query(Module).filter(Module.ModuleID == module_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Module]:
        db = self.db_session()
        result = db.query(Module).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_course(self, course_id: str) -> List[Module]:
        db = self.db_session()
        result = db.query(Module).filter(Module.CourseID == course_id).all()
        db.close()
        return result

    def update(self, module_id: str, title: Optional[str] = None,
               course_id: Optional[str] = None) -> Optional[Module]:
        db = self.db_session()
        module = db.query(Module).filter(Module.ModuleID == module_id).first()
        if not module:
            db.close()
            return None
        
        if title is not None:
            module.Title = title
        if course_id is not None:
            module.CourseID = course_id
        
        db.commit()
        db.refresh(module)
        db.close()
        return module

    def delete(self, module_id: str) -> bool:
        db = self.db_session()
        module = db.query(Module).filter(Module.ModuleID == module_id).first()
        if not module:
            db.close()
            return False
        
        db.delete(module)
        db.commit()
        db.close()
        return True


class LessonRefService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, lesson_id: str) -> LessonRef:
        lesson = LessonRef(LessonID=lesson_id)
        db = self.db_session()
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        db.close()
        return lesson

    def get_by_id(self, lesson_id: str) -> Optional[LessonRef]:
        db = self.db_session()
        result = db.query(LessonRef).filter(LessonRef.LessonID == lesson_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[LessonRef]:
        db = self.db_session()
        result = db.query(LessonRef).offset(skip).limit(limit).all()
        db.close()
        return result

    def delete(self, lesson_id: str) -> bool:
        db = self.db_session()
        lesson = db.query(LessonRef).filter(LessonRef.LessonID == lesson_id).first()
        if not lesson:
            db.close()
            return False
        
        db.delete(lesson)
        db.commit()
        db.close()
        return True


class ContentService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, content_id: str, module_id: str, title: Optional[str] = None,
               slides: Optional[str] = None) -> Content:
        content = Content(
            ContentID=content_id,
            ModuleID=module_id,
            Title=title,
            Slides=slides
        )
        db = self.db_session()
        db.add(content)
        db.commit()
        db.refresh(content)
        db.close()
        return content

    def get_by_id(self, content_id: str) -> Optional[Content]:
        db = self.db_session()
        result = db.query(Content).filter(Content.ContentID == content_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Content]:
        db = self.db_session()
        result = db.query(Content).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_module(self, module_id: str) -> List[Content]:
        db = self.db_session()
        result = db.query(Content).filter(Content.ModuleID == module_id).all()
        db.close()
        return result

    def update(self, content_id: str, title: Optional[str] = None,
               slides: Optional[str] = None, module_id: Optional[str] = None) -> Optional[Content]:
        db = self.db_session()
        content = db.query(Content).filter(Content.ContentID == content_id).first()
        if not content:
            db.close()
            return None
        
        if title is not None:
            content.Title = title
        if slides is not None:
            content.Slides = slides
        if module_id is not None:
            content.ModuleID = module_id
        
        db.commit()
        db.refresh(content)
        db.close()
        return content

    def delete(self, content_id: str) -> bool:
        db = self.db_session()
        content = db.query(Content).filter(Content.ContentID == content_id).first()
        if not content:
            db.close()
            return False
        
        db.delete(content)
        db.commit()
        db.close()
        return True


class TextService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, text_id: str, content_id: str, text: Optional[str] = None) -> Text:
        text_obj = Text(
            TextID=text_id,
            ContentID=content_id,
            Text=text
        )
        db = self.db_session()
        db.add(text_obj)
        db.commit()
        db.refresh(text_obj)
        db.close()
        return text_obj

    def get_by_id(self, text_id: str) -> Optional[Text]:
        db = self.db_session()
        result = db.query(Text).filter(Text.TextID == text_id).first()
        db.close()
        return result

    def get_by_content_id(self, content_id: str) -> Optional[Text]:
        db = self.db_session()
        result = db.query(Text).filter(Text.ContentID == content_id).first()
        db.close()
        return result

    def update(self, text_id: str, text: Optional[str] = None) -> Optional[Text]:
        db = self.db_session()
        text_obj = db.query(Text).filter(Text.TextID == text_id).first()
        if not text_obj:
            db.close()
            return None
        
        if text is not None:
            text_obj.Text = text
        
        db.commit()
        db.refresh(text_obj)
        db.close()
        return text_obj

    def delete(self, text_id: str) -> bool:
        db = self.db_session()
        text_obj = db.query(Text).filter(Text.TextID == text_id).first()
        if not text_obj:
            db.close()
            return False
        
        db.delete(text_obj)
        db.commit()
        db.close()
        return True


class VideoService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, video_id: str, content_id: str, video: Optional[str] = None) -> Video:
        video_obj = Video(
            VideoID=video_id,
            ContentID=content_id,
            Video=video
        )
        db = self.db_session()
        db.add(video_obj)
        db.commit()
        db.refresh(video_obj)
        db.close()
        return video_obj

    def get_by_id(self, video_id: str) -> Optional[Video]:
        db = self.db_session()
        result = db.query(Video).filter(Video.VideoID == video_id).first()
        db.close()
        return result

    def get_by_content_id(self, content_id: str) -> Optional[Video]:
        db = self.db_session()
        result = db.query(Video).filter(Video.ContentID == content_id).first()
        db.close()
        return result

    def update(self, video_id: str, video: Optional[str] = None) -> Optional[Video]:
        db = self.db_session()
        video_obj = db.query(Video).filter(Video.VideoID == video_id).first()
        if not video_obj:
            db.close()
            return None
        
        if video is not None:
            video_obj.Video = video
        
        db.commit()
        db.refresh(video_obj)
        db.close()
        return video_obj

    def delete(self, video_id: str) -> bool:
        db = self.db_session()
        video_obj = db.query(Video).filter(Video.VideoID == video_id).first()
        if not video_obj:
            db.close()
            return False
        
        db.delete(video_obj)
        db.commit()
        db.close()
        return True


class ImageService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, image_id: str, content_id: str, image: Optional[str] = None) -> Image:
        image_obj = Image(
            ImageID=image_id,
            ContentID=content_id,
            Image=image
        )
        db = self.db_session()
        db.add(image_obj)
        db.commit()
        db.refresh(image_obj)
        db.close()
        return image_obj

    def get_by_id(self, image_id: str) -> Optional[Image]:
        db = self.db_session()
        result = db.query(Image).filter(Image.ImageID == image_id).first()
        db.close()
        return result

    def get_by_content_id(self, content_id: str) -> Optional[Image]:
        db = self.db_session()
        result = db.query(Image).filter(Image.ContentID == content_id).first()
        db.close()
        return result

    def update(self, image_id: str, image: Optional[str] = None) -> Optional[Image]:
        db = self.db_session()
        image_obj = db.query(Image).filter(Image.ImageID == image_id).first()
        if not image_obj:
            db.close()
            return None
        
        if image is not None:
            image_obj.Image = image
        
        db.commit()
        db.refresh(image_obj)
        db.close()
        return image_obj

    def delete(self, image_id: str) -> bool:
        db = self.db_session()
        image_obj = db.query(Image).filter(Image.ImageID == image_id).first()
        if not image_obj:
            db.close()
            return False
        
        db.delete(image_obj)
        db.commit()
        db.close()
        return True


class AssignmentService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, ass_id: str, module_id: str, title: str,
               description: Optional[str] = None, deadline: Optional[datetime] = None) -> Assignment:
        assignment = Assignment(
            AssID=ass_id,
            ModuleID=module_id,
            Title=title,
            Description=description,
            Deadline=deadline or datetime.utcnow()
        )
        db = self.db_session()
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        db.close()
        return assignment

    def get_by_id(self, ass_id: str) -> Optional[Assignment]:
        db = self.db_session()
        result = db.query(Assignment).filter(Assignment.AssID == ass_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Assignment]:
        db = self.db_session()
        result = db.query(Assignment).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_module(self, module_id: str) -> List[Assignment]:
        db = self.db_session()
        result = db.query(Assignment).filter(Assignment.ModuleID == module_id).all()
        db.close()
        return result

    def update(self, ass_id: str, title: Optional[str] = None,
               description: Optional[str] = None, deadline: Optional[datetime] = None) -> Optional[Assignment]:
        db = self.db_session()
        assignment = db.query(Assignment).filter(Assignment.AssID == ass_id).first()
        if not assignment:
            db.close()
            return None
        
        if title is not None:
            assignment.Title = title
        if description is not None:
            assignment.Description = description
        if deadline is not None:
            assignment.Deadline = deadline
        
        db.commit()
        db.refresh(assignment)
        db.close()
        return assignment

    def delete(self, ass_id: str) -> bool:
        db = self.db_session()
        assignment = db.query(Assignment).filter(Assignment.AssID == ass_id).first()
        if not assignment:
            db.close()
            return False
        
        db.delete(assignment)
        db.commit()
        db.close()
        return True


class QuizService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, quiz_id: str, module_id: str, title: str,
               time_limit: Optional[int] = None, num_attempt: int = 1) -> Quiz:
        quiz = Quiz(
            QuizID=quiz_id,
            ModuleID=module_id,
            Title=title,
            Time_limit=time_limit,
            Num_attempt=num_attempt
        )
        db = self.db_session()
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        db.close()
        return quiz

    def get_by_id(self, quiz_id: str) -> Optional[Quiz]:
        db = self.db_session()
        result = db.query(Quiz).filter(Quiz.QuizID == quiz_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Quiz]:
        db = self.db_session()
        result = db.query(Quiz).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_module(self, module_id: str) -> List[Quiz]:
        db = self.db_session()
        result = db.query(Quiz).filter(Quiz.ModuleID == module_id).all()
        db.close()
        return result

    def update(self, quiz_id: str, title: Optional[str] = None,
               time_limit: Optional[int] = None, num_attempt: Optional[int] = None) -> Optional[Quiz]:
        db = self.db_session()
        quiz = db.query(Quiz).filter(Quiz.QuizID == quiz_id).first()
        if not quiz:
            db.close()
            return None
        
        if title is not None:
            quiz.Title = title
        if time_limit is not None:
            quiz.Time_limit = time_limit
        if num_attempt is not None:
            quiz.Num_attempt = num_attempt
        
        db.commit()
        db.refresh(quiz)
        db.close()
        return quiz

    def delete(self, quiz_id: str) -> bool:
        db = self.db_session()
        quiz = db.query(Quiz).filter(Quiz.QuizID == quiz_id).first()
        if not quiz:
            db.close()
            return False
        
        db.delete(quiz)
        db.commit()
        db.close()
        return True


class QuestionService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, question_id: str, quiz_id: str, content: str,
               correct_answer: str) -> Question:
        question = Question(
            QuestionID=question_id,
            QuizID=quiz_id,
            Content=content,
            Correct_answer=correct_answer
        )
        db = self.db_session()
        db.add(question)
        db.commit()
        db.refresh(question)
        db.close()
        return question

    def get_by_id(self, question_id: str) -> Optional[Question]:
        db = self.db_session()
        result = db.query(Question).filter(Question.QuestionID == question_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Question]:
        db = self.db_session()
        result = db.query(Question).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_quiz(self, quiz_id: str) -> List[Question]:
        db = self.db_session()
        result = db.query(Question).filter(Question.QuizID == quiz_id).all()
        db.close()
        return result

    def update(self, question_id: str, content: Optional[str] = None,
               correct_answer: Optional[str] = None) -> Optional[Question]:
        db = self.db_session()
        question = db.query(Question).filter(Question.QuestionID == question_id).first()
        if not question:
            db.close()
            return None
        
        if content is not None:
            question.Content = content
        if correct_answer is not None:
            question.Correct_answer = correct_answer
        
        db.commit()
        db.refresh(question)
        db.close()
        return question

    def delete(self, question_id: str) -> bool:
        db = self.db_session()
        question = db.query(Question).filter(Question.QuestionID == question_id).first()
        if not question:
            db.close()
            return False
        
        db.delete(question)
        db.commit()
        db.close()
        return True


class AnswerService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, answer_id: str, question_id: str, quiz_id: str, answer: str) -> Answer:
        answer_obj = Answer(
            AnswerID=answer_id,
            QuestionID=question_id,
            QuizID=quiz_id,
            Answer=answer
        )
        db = self.db_session()
        db.add(answer_obj)
        db.commit()
        db.refresh(answer_obj)
        db.close()
        return answer_obj

    def get_by_id(self, answer_id: str) -> Optional[Answer]:
        db = self.db_session()
        result = db.query(Answer).filter(Answer.AnswerID == answer_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Answer]:
        db = self.db_session()
        result = db.query(Answer).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_question(self, question_id: str) -> List[Answer]:
        db = self.db_session()
        result = db.query(Answer).filter(Answer.QuestionID == question_id).all()
        db.close()
        return result

    def update(self, answer_id: str, answer: Optional[str] = None) -> Optional[Answer]:
        db = self.db_session()
        answer_obj = db.query(Answer).filter(Answer.AnswerID == answer_id).first()
        if not answer_obj:
            db.close()
            return None
        
        if answer is not None:
            answer_obj.Answer = answer
        
        db.commit()
        db.refresh(answer_obj)
        db.close()
        return answer_obj

    def delete(self, answer_id: str) -> bool:
        db = self.db_session()
        answer_obj = db.query(Answer).filter(Answer.AnswerID == answer_id).first()
        if not answer_obj:
            db.close()
            return False
        
        db.delete(answer_obj)
        db.commit()
        db.close()
        return True