from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.device_controller import DeviceController
from schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceToggle

router = APIRouter()
device_controller = DeviceController()

@router.post("/", response_model=dict)
async def create_device(device_data: DeviceCreate, db: Session = Depends(get_db)):
    """Create a new device"""
    return await device_controller.create_device(device_data, db)

@router.get("/{device_id}", response_model=dict)
async def get_device(device_id: int, db: Session = Depends(get_db)):
    """Get a device by ID"""
    return await device_controller.get_device(device_id, db)

@router.get("/user/{user_id}", response_model=dict)
async def get_user_devices(user_id: int, db: Session = Depends(get_db)):
    """Get all devices for a specific user"""
    return await device_controller.get_user_devices(user_id, db)

@router.get("/", response_model=dict)
async def get_all_devices(db: Session = Depends(get_db)):
    """Get all devices (admin function)"""
    return await device_controller.get_all_devices(db)

@router.patch("/{device_id}", response_model=dict)
async def update_device(device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_db)):
    """Update a device"""
    return await device_controller.update_device(device_id, device_data, db)

@router.post("/{device_id}/toggle", response_model=dict)
async def toggle_device(device_id: int, toggle_data: DeviceToggle, db: Session = Depends(get_db)):
    """Toggle device status"""
    return await device_controller.toggle_device(device_id, toggle_data, db)

@router.delete("/{device_id}", response_model=dict)
async def delete_device(device_id: int, db: Session = Depends(get_db)):
    """Delete a device"""
    return await device_controller.delete_device(device_id, db)