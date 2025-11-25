from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import enum
from .base import Base
import uuid
from datetime import datetime, timedelta, timezone

class UserRole(str, enum.Enum):
    """Các vai trò cơ bản trong hệ thống."""
    TUTOR = "tutor"
    ADMIN = "admin"
    TUTEE = "tutee"


class MututorUser(Base):
    """Phân quyền cho MuChat."""
    __tablename__ = "users"

    #id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, primary_key=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False, index=True)
      

    def __repr__(self):
        return f"<MututorUser(id={self.id}, username='{self.username}', role='{self.role.value}')>"
    

class MuSession(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, unique=True)
    role = Column(Enum(UserRole), nullable=False, index=True)
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(hours=1))