from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

from config.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(20), nullable=False, default='user')  # 'user' or 'admin'
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # SPECIAL METHOD TO REPRESENT THE OBJECT AS A STRING
    def __repr__(self):
        return f'<User {self.email}>'
        
    # METHOD TO CONVERT THE OBJECT TO A DICTIONARY
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }