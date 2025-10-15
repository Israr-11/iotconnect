from fastapi import APIRouter, Query, Depends
from typing import Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from controllers.device_log_controller import DeviceLogController
from config.database import get_db

router = APIRouter()
device_log_controller = DeviceLogController()

@router.get("/device/{device_id}", response_model=Dict)
async def get_device_logs(
    device_id: int,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get logs for a specific device"""
    return await device_log_controller.get_device_logs(device_id, limit, db)

@router.get("/user/{user_id}", response_model=Dict)
async def get_user_device_logs(
    user_id: int,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get logs for all devices owned by a user"""
    return await device_log_controller.get_user_device_logs(user_id, limit, db)

@router.get("/device/{device_id}/timeframe", response_model=Dict)
async def get_logs_by_timeframe(
    device_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get device logs within a specific timeframe"""
    return await device_log_controller.get_logs_by_timeframe(
        device_id, start_date, end_date, db
    )