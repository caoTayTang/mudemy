from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional
from ..models.user import MututorUser, UserRole


class UserService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, id: str, username: str, role: UserRole) -> MututorUser:
        user = MututorUser(id=id, username=username, role=role)
        db = self.db_session()
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        return user

    def get_by_id(self, user_id: str) -> Optional[MututorUser]:
        db = self.db_session()
        result = db.query(MututorUser).filter(MututorUser.id == user_id).first()
        db.close()
        return result

    def get_by_username(self, username: str) -> Optional[MututorUser]:
        db = self.db_session()
        result = db.query(MututorUser).filter(MututorUser.username == username).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[MututorUser]:
        db = self.db_session()
        result = db.query(MututorUser).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_role(self, role: UserRole) -> List[MututorUser]:
        db = self.db_session()
        result = db.query(MututorUser).filter(MututorUser.role == role).all()
        db.close()
        return result

    def update(self, user_id: str, username: Optional[str] = None, role: Optional[UserRole] = None) -> Optional[MututorUser]:
        db = self.db_session()
        user = db.query(MututorUser).filter(MututorUser.id == user_id).first()
        if not user:
            db.close()
            return None
        
        if username is not None:
            user.username = username
        if role is not None:
            user.role = role
        
        db.commit()
        db.refresh(user)
        db.close()
        return user

    def delete(self, user_id: str) -> bool:
        db = self.db_session()
        user = db.query(MututorUser).filter(MututorUser.id == user_id).first()
        if not user:
            db.close()
            return False
        
        db.delete(user)
        db.commit()
        db.close()
        return True