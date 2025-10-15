from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from services.device_service import DeviceService
from config.database import get_db
from schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceToggle

class DeviceController:
    def __init__(self):
        self.device_service = DeviceService()
    
    async def create_device(
        self, 
        device_data: DeviceCreate,
        db: Session,
        owner_id: int = 2  
    ):
        """Create a new device"""
        device, error = self.device_service.create_device(db, device_data.dict(), owner_id)
        
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        return {"message": "Device created successfully", "device": device.to_dict()}
    
    async def get_device(
        self, 
        device_id: int,
        db: Session 
    ):
        """Get a device by ID"""
        device = self.device_service.get_device_by_id(db, device_id)
        
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        
        return {"device": device.to_dict()}
    
    async def get_user_devices(
        self, 
        user_id: int,
        db: Session
    ):
        """Get all devices for a specific user"""
        devices = self.device_service.get_user_devices(db, user_id)
        return {"devices": [device.to_dict() for device in devices]}
    
    async def get_all_devices(
        self,
        db: Session 
    ):
        """Get all devices (admin function)"""
        devices = self.device_service.get_all_devices(db)
        return {"devices": [device.to_dict() for device in devices]}
    
    async def update_device(
        self, 
        device_id: int,
        device_data: DeviceUpdate,
        db: Session
    ):
        """Update a device"""
        device, error = self.device_service.update_device(db, device_id, device_data.dict(exclude_unset=True))
        
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        return {"message": "Device updated successfully", "device": device.to_dict()}
    
    async def toggle_device(
        self, 
        device_id: int,
        toggle_data: DeviceToggle,
        db: Session,
        user_id: int = 2
    ):
        """Toggle device status"""
        device, error = self.device_service.toggle_device_status(
            db, 
            device_id, 
            toggle_data.status, 
            user_id
        )
        
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        return {"message": "Device status updated", "device": device.to_dict()}
    
    async def delete_device(
        self, 
        device_id: int,
        db: Session
    ):
        """Delete a device"""
        success, error = self.device_service.delete_device(db, device_id)
        
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        return {"message": "Device deleted successfully"}