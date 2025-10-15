from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Tuple, Any
from models.device import Device
from models.device_log import DeviceLog

class DeviceService:
    def create_device(self, db: Session, device_data: Dict[str, Any], owner_id: int) -> Tuple[Optional[Device], Optional[str]]:
        """Create a new device"""
        # CHECKING IF DEVICE_UID ALREADY EXISTS
        existing_device = db.query(Device).filter(Device.device_uid == device_data['device_uid']).first()
        if existing_device:
            return None, "Device UID already registered"
            
        # CREATING NEW DEVICE
        device = Device(
            device_uid=device_data['device_uid'],
            name=device_data['name'],
            type=device_data['type'],
            status=device_data.get('status', False),
            owner_id=owner_id
        )
        
        # SAVING TO DATABASE
        db.add(device)
        db.commit()
        db.refresh(device)
        
        return device, None
        
    def get_device_by_id(self, db: Session, device_id: int) -> Optional[Device]:
        """Get device by ID"""
        return db.query(Device).filter(Device.id == device_id).first()
    
    def get_device_by_uid(self, db: Session, device_uid: str) -> Optional[Device]:
        """Get device by UID"""
        return db.query(Device).filter(Device.device_uid == device_uid).first()
        
    def get_user_devices(self, db: Session, owner_id: int) -> List[Device]:
        """Get all devices for a specific user"""
        return db.query(Device).filter(Device.owner_id == owner_id).all()
        
    def get_all_devices(self, db: Session) -> List[Device]:
        """Get all devices (admin function)"""
        return db.query(Device).all()
        
    def update_device(self, db: Session, device_id: int, update_data: Dict[str, Any]) -> Tuple[Optional[Device], Optional[str]]:
        """Update device information"""
        device = self.get_device_by_id(db, device_id)
        if not device:
            return None, "Device not found"
            
        # UPDATING ALLOWED FIELDS
        if 'name' in update_data:
            device.name = update_data['name']
        if 'type' in update_data:
            device.type = update_data['type']
            
        db.commit()
        db.refresh(device)
        
        return device, None
        
    def toggle_device_status(self, db: Session, device_id: int, new_status: bool, user_id: Optional[int] = None) -> Tuple[Optional[Device], Optional[str]]:
        """Toggle device on/off status and log the action"""
        device = self.get_device_by_id(db, device_id)
        if not device:
            return None, "Device not found"
            
        device.status = new_status
        
        log_entry = DeviceLog(
            device_id=device.id,
            state=new_status,
            action_by=user_id
        )
        
        db.add(log_entry)
        db.commit()
        db.refresh(device)
        
        return device, None
        
    def delete_device(self, db: Session, device_id: int) -> Tuple[bool, Optional[str]]:
        """Delete a device"""
        device = self.get_device_by_id(db, device_id)
        if not device:
            return False, "Device not found"
            
        db.delete(device)
        db.commit()
        
        return True, None