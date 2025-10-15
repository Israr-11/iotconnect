from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from config.database import Base

class DeviceLog(Base):
    __tablename__ = 'device_logs'
    
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id', ondelete='CASCADE'))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    state = Column(Boolean, nullable=False)
    action_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    # RELATIONSHIPS
    device = relationship("Device", backref="logs")
    user = relationship("User", backref="actions")
    
    def __repr__(self):
        return f'<DeviceLog {self.id}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'state': self.state,
            'action_by': self.action_by
        }