from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional
from datetime import datetime, timezone
from ..models.record import MeetingRecord, MeetingRecordStatus


class MeetingRecordService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, course_id: int, tutor_id: str, 
               attendees: Optional[str] = None, discussion_points: Optional[str] = None,
               status: MeetingRecordStatus = MeetingRecordStatus.PENDING) -> MeetingRecord:
        record = MeetingRecord(
            course_id=course_id,
            tutor_id=tutor_id,
            attendees=attendees,
            discussion_points=discussion_points,
            status=status
        )
        db = self.db_session()
        db.add(record)
        db.commit()
        db.refresh(record)
        db.close()
        return record

    def get_by_id(self, record_id: int) -> Optional[MeetingRecord]:
        db = self.db_session()
        result = db.query(MeetingRecord).filter(MeetingRecord.id == record_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[MeetingRecord]:
        db = self.db_session()
        result = db.query(MeetingRecord).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_course(self, course_id: int) -> List[MeetingRecord]:
        db = self.db_session()
        result = db.query(MeetingRecord).filter(MeetingRecord.course_id == course_id).all()
        db.close()
        return result

    def get_by_tutor(self, tutor_id: str) -> List[MeetingRecord]:
        db = self.db_session()
        result = db.query(MeetingRecord).filter(MeetingRecord.tutor_id == tutor_id).all()
        db.close()
        return result

    def get_by_status(self, status: MeetingRecordStatus) -> List[MeetingRecord]:
        db = self.db_session()
        result = db.query(MeetingRecord).filter(MeetingRecord.status == status).all()
        db.close()
        return result

    def update(self, record_id: int, attendees: Optional[str] = None,
               discussion_points: Optional[str] = None, 
               status: Optional[MeetingRecordStatus] = None) -> Optional[MeetingRecord]:
        db = self.db_session()
        record = db.query(MeetingRecord).filter(MeetingRecord.id == record_id).first()
        if not record:
            db.close()
            return None
        
        if attendees is not None:
            record.attendees = attendees
        if discussion_points is not None:
            record.discussion_points = discussion_points
        if status is not None:
            record.status = status
        
        record.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(record)
        db.close()
        return record

    def approve(self, record_id: int) -> Optional[MeetingRecord]:
        return self.update(record_id, status=MeetingRecordStatus.APPROVED)

    def reject(self, record_id: int) -> Optional[MeetingRecord]:
        return self.update(record_id, status=MeetingRecordStatus.REJECTED)

    def delete(self, record_id: int) -> bool:
        db = self.db_session()
        record = db.query(MeetingRecord).filter(MeetingRecord.id == record_id).first()
        if not record:
            db.close()
            return False
        
        db.delete(record)
        db.commit()
        db.close()
        return True