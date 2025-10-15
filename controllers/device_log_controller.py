from fastapi import Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from services.device_log_service import DeviceLogService
from config.database import get_db

class DeviceLogController:
    def __init__(self):
        self.device_log_service = DeviceLogService()
    
    async def get_device_logs(
        self,
        device_id: int,
        limit: int,
        db: Session
    ):
        """Get logs for a specific device"""
        logs = self.device_log_service.get_device_logs(db, device_id, limit)
        return {"logs": [log.to_dict() for log in logs]}
    
    async def get_user_device_logs(
        self,
        user_id: int,
        limit: int,
        db: Session
    ):
        """Get logs for all devices owned by a user"""
        logs = self.device_log_service.get_user_device_logs(db, user_id, limit)
        return {"logs": [log.to_dict() for log in logs]}
    
    async def get_logs_by_timeframe(
        self,
        device_id: int,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        db: Session
    ):
        """Get device logs within a specific timeframe"""
        logs = self.device_log_service.get_logs_by_timeframe(db, device_id, start_date, end_date)
        return {"logs": [log.to_dict() for log in logs]}