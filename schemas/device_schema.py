from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class DeviceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Device name")
    type: str = Field(..., min_length=1, max_length=100, description="Type of device (e.g., 'switch', 'light')")
    
class DeviceCreate(DeviceBase):
    device_uid: str = Field(..., min_length=1, max_length=255, description="Unique identifier of the physical device")
    status: Optional[bool] = Field(False, description="Device status (on/off)")
    
class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Device name")
    type: Optional[str] = Field(None, min_length=1, max_length=100, description="Type of device")
    
class DeviceToggle(BaseModel):
    status: bool = Field(..., description="New device status (true=on, false=off)")

class DeviceResponse(DeviceBase):
    id: int
    device_uid: str
    status: bool
    owner_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True