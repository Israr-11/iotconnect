from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from config.database import Base

class Device(Base):
    __tablename__ = 'devices'
    
    id = Column(Integer, primary_key=True)
    device_uid = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    status = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # RELATIONSHIP
    owner = relationship("User", backref="devices")
    
    def __repr__(self):
        return f'<Device {self.name}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'device_uid': self.device_uid,
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }