from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceLogBase(BaseModel):
    device_id: int
    state: bool
    
class DeviceLogCreate(DeviceLogBase):
    action_by: Optional[int] = None
    
class DeviceLogResponse(DeviceLogBase):
    id: int
    timestamp: datetime
    action_by: Optional[int]
    
    class Config:
        orm_mode = True