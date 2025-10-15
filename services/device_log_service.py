from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from models.device_log import DeviceLog
from models.device import Device

class DeviceLogService:
    def get_device_logs(self, db: Session, device_id: int, limit: int = 100) -> List[DeviceLog]:
        """Get logs for a specific device"""
        return db.query(DeviceLog).filter(DeviceLog.device_id == device_id).order_by(DeviceLog.timestamp.desc()).limit(limit).all()
    
    def get_user_device_logs(self, db: Session, user_id: int, limit: int = 100) -> List[DeviceLog]:
        """Get logs for all devices owned by a user"""
        return db.query(DeviceLog).join(Device, DeviceLog.device_id == Device.id)\
                .filter(Device.owner_id == user_id)\
                .order_by(DeviceLog.timestamp.desc())\
                .limit(limit).all()
    
    def get_logs_by_timeframe(self, db: Session, device_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[DeviceLog]:
        """Get device logs within a specific timeframe"""
        query = db.query(DeviceLog).filter(DeviceLog.device_id == device_id)
        
        if start_date:
            query = query.filter(DeviceLog.timestamp >= start_date)
        if end_date:
            query = query.filter(DeviceLog.timestamp <= end_date)
            
        return query.order_by(DeviceLog.timestamp.desc()).all()