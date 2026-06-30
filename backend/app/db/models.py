"""
Database models for Focus API.

Contains SQLAlchemy ORM models for:
- Users
- FocusSessions

"""
from datetime import datetime, timezone
from sqlalchemy import Column, Index, Integer, String, DateTime, ForeignKey, text, Enum, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class FocusSession(Base):
    """Focus sessions represent dedicated pomodoro time block.."""
    __tablename__ = "focus_sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    work_time = Column(Integer, nullable=True)
    break_time = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="focus_sessions")

    __table_args__ = (
        Index("idx_focus_user", "user_id", "start_time"),
    )

class User(Base):
    """Since the database is shared, users must have their own accounts. They can have multiple focus sessions. Passwords are stored as hashed values for security."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    is_verified = Column(Boolean, default=False)

    focus_sessions = relationship("FocusSession", back_populates="user", lazy="dynamic")