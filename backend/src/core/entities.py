import uuid 

from sqlalchemy import func, Column, DateTime, ForeignKey, Text, String, Integer, text
from sqlalchemy.dialects.postgresql import UUID, JSONB      # JSONB is for storing JSON data as binary within the database
from sqlalchemy.orm import relationship

from src.database.core import Base

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    university = Column(String(255), nullable=True)
    token_version = Column(Integer, nullable=False, server_default=text("1"), default=1)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id='{self.id}', first_name='{self.first_name}', last_name='{self.last_name}'), email='{self.email}')>"
